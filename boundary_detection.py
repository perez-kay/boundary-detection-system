import cv2, json
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

def calculate_distance(img1, img2):
        """
        Calculates the frame-to-frame distance between the two given images.
        The arrays must be of the same length.

        Parameters
        ----------
        img1 : np.array
            The histogram for the first image
        img2 : np.array
            The histogram for the second image

        Returns
        -------
        int:
            The calculated frame-to-frame distance
        
        """

        if len(img1) != len(img2):
            print("Error, lengths don't match up")
            return -1
        return np.sum(np.absolute(img1 - img2))



def compute_SD(frames):
    """
    Computes the 
    """
    sd = list()
    for i in range(len(frames) - 1):
        frame_i = frames[i].get_histogram()
        frame_k = frames[i + 1].get_histogram()
        difference = calculate_distance(frame_i, frame_k)
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

    for i in range(len(sd)):
        # if greater than TB, it's a cut
        if sd[i] >= TB:
            # Cs = i, Ce = i+1
            cuts.append((i + 1001, i + 1002))
        
        # if we didn't find a cut on this iter
        # if greater that TS and less than TB, it's possibly a gt
        if sd[i] >= TS and sd[i] < TB:
            # if we haven't set a start candi
            if not fs_candi_set:
                # set it
                fs_candi = i
                fs_candi_set = True
                # print('fs_candi:', fs_candi)
            else:
                # fs is already set and we're trying to find the end
                # set fe
                fe_candi = i
                fe_candi_set = True
                # print('fe_candi:', fe_candi)
        else:
            # sd[i] < TS so we need to track that
            if fs_candi_set:
                lower_than_ts += 1

        # if we've hit the Tos or a cut boundary
        if lower_than_ts > 2 or (i - 1) in [Cs for Cs, Ce in cuts]:
            if fs_candi_set and fe_candi_set:
                # get the sum of sds from fs to fe
                gt_sum = sum([sd[i] for i in range(fs_candi, fe_candi + 1, 1)])
                
                # if this sum is bigger than TB
                if gt_sum >= TB:
                    # we found a gt!
                    gradual_trans.append((fs_candi + 1001, fe_candi + 1001))

            # reset all vales
            fs_candi_set = False
            fe_candi_set = False
            # cut_found = False
            lower_than_ts = 0
    return cuts, gradual_trans


def dump_shots_and_timestamps(frames, gts):


    # get the list of fs + 1
    shot_frames = [fs + 1 for fs, fe in gts]
    timestamps = dict()
    for frame in frames:
        frame_num = frame.get_frame_num()
        if frame_num in shot_frames:
            img_path = "frames/" + str(frame_num) + ".jpg"
            img = cv2.cvtColor(frame.get_img_data(), cv2.COLOR_RGB2BGR)
            cv2.imwrite(img_path, img)
            # save the timestamp
            timestamp = frame.get_timestamp() / 1000
            timestamps[img_path] = timestamp
    
    with open('timestamps.json', 'w') as file:
        json.dump(timestamps, file)
    



frames = read_frames()
sd = compute_SD(frames)
cuts, gts = find_boundaries(sd)
dump_shots_and_timestamps(frames, gts)
