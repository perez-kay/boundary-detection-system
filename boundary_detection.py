import cv2, json
import numpy as np
import Frame

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

    return frames

def compute_SD(frames):
    """
    Computes SD for each frame-to-frame difference.

    Parameters
    ----------
    frames : list
        The list containing all of the Frame objects for the video

    Returns
    -------
    list
        The SD value for each frame-to-frame difference
    """

    sd = list()
    for i in range(len(frames) - 1):
        frame_i = frames[i].get_histogram()
        frame_k = frames[i + 1].get_histogram()
        difference = np.sum(np.absolute(frame_i - frame_k))
        sd.append(difference)
    return sd

def average(list):
    """
    Returns the average value of the given list.

    Parameters
    ----------
    list : list
        The list to take the average of
    
    Returns
    -------
    float
        The average of the list
    """

    return sum(list) / len(list)


def find_boundaries(sd):
    """
    Finds all of the cut and gradual transition boundaries within the video.

    Parameters
    ----------
    sd : list
        The list of SD values for each frame-to-frame difference
    
    Returns
    -------
    cuts : list
        List of cut boundaries. The list contains tuples which consists of
        (Cs, Ce)
    gradual_trans : list
        List of gradual transition boundaries. The list contains tuples which
        consist of (Fs, Fe)
    """

    TB = average(sd) + np.std(sd) * 11
    TS = average(sd) * 2

    cuts = list()
    gradual_trans = list()
    lower_than_ts = 0
    fs_candi_set = False
    fe_candi_set = False

    for i in range(len(sd)):
        # if greater than TB, it's a cut
        if sd[i] >= TB:
            # Cs = i, Ce = i + 1
            # we add 1001 to each value to offset the fact that we started our
            # initial frame count at 0
            cuts.append((i + 1001, i + 1002))
        
        # if greater that TS and less than TB, it's possibly a gt
        if sd[i] >= TS and sd[i] < TB:
            # if we haven't set a start candidate
            if not fs_candi_set:
                # set it
                fs_candi = i
                fs_candi_set = True
            else:
                # Fs is already set and we're trying to find the end
                # set Fe
                fe_candi = i
                fe_candi_set = True
        else:
            # sd[i] < TS so we need to track that
            if fs_candi_set:
                lower_than_ts += 1

        # if we've hit the Tos or a cut boundary
        if lower_than_ts > 2 or (i - 1) in [Cs for Cs, Ce in cuts]:
            
            # if we have values for both Fs and Fe
            if fs_candi_set and fe_candi_set:
                
                # get the sum of SDs from Fs to Fe
                gt_sum = sum([sd[i] for i in range(fs_candi, fe_candi + 1, 1)])
                
                # if this sum is bigger than TB
                if gt_sum >= TB:
                    # we found a gt!
                    gradual_trans.append((fs_candi + 1001, fe_candi + 1001))

            # reset all values
            fs_candi_set = False
            fe_candi_set = False
            lower_than_ts = 0

    return cuts, gradual_trans


def dump_shots_and_timestamps(frames, gts):
    """
    Saves the first frame of each shot as a JPG file and dumps the
    file path and timestamp of the first frame of each shot to a JSON file.

    This was used to preprocess the data so it could be displayed with
    Streamlit.

    Parameters
    ----------
    frames : list
        The list containing all of the Frame objects for the video
    gts : list
        The list containing all of the boundaries for gradual transitions

    """

    shot_frames = [fs + 1 for fs, fe in gts]
    timestamps = dict()
    for frame in frames:
        frame_num = frame.get_frame_num()
        if frame_num in shot_frames:
            img_path = str(frame_num) + ".jpg"
            img = cv2.cvtColor(frame.get_img_data(), cv2.COLOR_RGB2BGR)
            cv2.imwrite("frames/" + img_path, img)
            # save the timestamp
            timestamp = frame.get_timestamp() / 1000
            timestamps[img_path] = timestamp
    
    with open('timestamps.json', 'w') as file:
        json.dump(timestamps, file)
    


if __name__ == "__main__":
    print("Generating output for video: 20020924_juve_dk_02a.avi...")
    print()
    frames = read_frames()
    sd = compute_SD(frames)
    cuts, gts = find_boundaries(sd)
    print("Detected cuts:")
    print("      Cs         Ce")
    print("----------------------------")
    for cut in cuts:
        print("    ", cut[0], "     ", cut[1])
    print()
    print("Detected transitions:")
    print("      Fs         Fe")
    print("----------------------------")
    for trans in gts:
        print("    ", trans[0], "     ", trans[1])

