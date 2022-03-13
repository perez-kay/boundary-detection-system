import numpy as np

class Frame:
    """
    The Frame class stores important information about a frame of a video.

    Attributes
    ----------
    frame_num : int
        The number of this frame in the video
    timestamp : float
        The timestamp that this frame appears in the video (in milliseconds)
    img_data : np.array
        The image data representing the frame
    histogram : np.array
        The intensity histogram data for the frame

    Methods
    --------
    get_frame_num()
        Returns the frame's number
    get_timestamp()
        Returns the frame's timestamp
    get_img_data()
        Returns the frame's image data
    get_histogram()
        Returns the frame's histogram data
    calculate_histogram()
        Calculates the histogram for the frame

    """

    def __init__(self, frame_num, timestamp, img_data):
        self.frame_num = frame_num
        self.timestamp = timestamp
        self.img = img_data
        self.histogram = self.compute_histogram()

    def get_frame_num(self):
        """
        Returns the frame's number.

        Returns
        -------
        int
            The frame number
        """

        return self.frame_num
    
    def get_timestamp(self):
        """
        Returns the frame's timestamp in milliseconds.

        Returns
        --------
        float
            The timestamp
        """
        
        return self.timestamp

    def get_img_data(self):
        """
        Returns the frame's image data.

        Returns
        -------
        np.array
            The image data for the frame
        """
        
        return self.img

    def get_histogram(self):
        """
        Returns the intensity histogram for the frame

        Returns
        -------
        np.array
            The intensity histogram
        """

        return self.histogram

    def compute_histogram(self):
        """
        Calculates the intensity for each pixel of the given image and creates
        a histogram.
        
        Returns
        -------
        np.array
            The intensity histogram
        """

        intensities = list()
        bins = list(range(0,250,10))
        bins.append(255)

        reds = self.img[:, :, 0] * 0.299
        greens = self.img[:, :, 1] * 0.587
        blues = self.img[:, :, 2] * 0.114
        r_and_g = np.add(reds, greens)
        intensities.append(np.add(r_and_g, blues))

        hist, bin_edges = np.histogram(intensities, bins=bins)
        return hist


    