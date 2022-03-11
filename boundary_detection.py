import cv2, statistics
import Frame
import numpy as np

def read_frames():
    """
    Reads the video soccer.avi and grabs frames 1000-4999 and basic data about
    each frame (the frame number, the timestamp of the frame, and the image
    data of the frame). This data is stored in the Frame class.

    Returns
    --------
    list:
        The list of Frame objects from the video
    """
    # ONLY LOOKING AT FRAMES 1000 - 4999
    vidcap = cv2.VideoCapture('soccer.avi')
    frame_exists, frame_img = vidcap.read()
    frame_num = 0
    frames = list()
    while frame_exists:
        if frame_num >= 1000 and frame_num <= 4999:
            # get timestamp of frame
            timestamp = vidcap.get(cv2.CAP_PROP_POS_MSEC)

            # convert the frame to RGB colorspace
            frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)

            # append the frame to the frames data
            frames.append(Frame.Frame(frame_num, timestamp, frame_img))

        # get the next frame    
        frame_exists, frame_img = vidcap.read()
        frame_num += 1
    # with open('frames_data.json', 'w') as file:
    #     json.dump(frames, file, default=lambda x: x.to_dict())

    return frames

def calculate_manhattan(img1, img2):
        """
        Calculates the Manhattan Distance between the two given lists. The lists
        must be of the same length.

        Parameters
        ----------
        img1 : list
            The histogram for the first image
        img2 : list
            The histogram for the second image

        Returns
        -------
        float:
            The calculated Manhattan Distance
        
        """

        if len(img1) != len(img2):
            print("Error, lengths don't match up")
            return -1
        
        result = 0
        # for j in range(len(img1)):
        #     h_i = img1[j]
        #     h_k = img2[j]
        #     result += abs(h_i - h_k)
        result = np.sum(np.absolute(img1 - img2))
        return result



def compute_SD(frames):
    # frames = list of frame objects
    sd = list()
    for i in range(len(frames) - 1):
        frame_i = frames[i].get_histogram()
        frame_k = frames[i + 1].get_histogram()
        difference = calculate_manhattan(frame_i, frame_k)
        sd.append(difference)
    return sd

def average(list):
    """
    Returns the average value of the given list.
    """
    return sum(list) / len(list)


def find_boundaries(sd):
    TB = average(sd) + np.std(sd) * 11
    TS = average(sd) * 2

    cuts = list()
    gradual_trans = list()
    fs_candi = -1
    lower_than_ts = 0
    fs_candi_set = False
    fe_candi_set = False
    cut_found = False

    for i in range(len(sd)):

        # if greater than TB, it's a cut
        if sd[i] >= TB:
            # Cs = i, Ce = i+1
            cuts.append((i + 1000, i + 1001))
            cut_found = True
        
        # if we didn't find a cut on this iter
        if not cut_found:
            # if greater that TS and less than TB, it's possibly a gt
            if sd[i] >= TS and sd[i] < TB:
                # if we haven't set a start candi
                if not fs_candi_set:
                    # set it
                    fs_candi = i
                    fs_candi_set = True
                    print('fs_candi:', fs_candi)
                else:
                    # fs is already set and we're trying to find the end
                    # set fe
                    fe_candi = i
                    fe_candi_set = True
                    print('fe_candi:', fe_candi)
            else:
                # sd[i] < TS so we need to track that
                if fs_candi_set:
                    lower_than_ts += 1

        # if we've hit the Tos or a cut boundary
        if lower_than_ts > 2 or i in [Cs for Cs, Ce in cuts]:
            if fs_candi_set and fe_candi_set:
                # get the sum of sds from fs to fe
                gt_sum = sum([sd[i] for i in range(fs_candi, fe_candi + 1, 1)])
                
                # if this sum is bigger than TB
                if gt_sum >= TB:
                    # we found a gt!
                    gradual_trans.append((fs_candi + 1000, fe_candi + 1000))
                
            # reset all vales
            fs_candi_set = False
            fe_candi_set = False
            cut_found = False
            lower_than_ts = 0
        
    return cuts, gradual_trans

        




frames = read_frames()
sd = compute_SD(frames)
# TB = average(sd) + np.std(sd) * 11
# TS = average(sd) * 2
# print("TB:", TB)
# print("TS:", TS)
cuts, gts = find_boundaries(sd)
print("cuts:", cuts)
print("gts:", gts)

# print(frames[0].get_histogram())
# print(frames[1].get_histogram())
# print(calculate_manhattan(frames[0].get_histogram(), frames[1].get_histogram()))