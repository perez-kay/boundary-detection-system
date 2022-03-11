import numpy as np

class Frame:

    def __init__(self, frame_num, timestamp, img_data):
        self.frame_num = frame_num
        self.timestamp = timestamp
        self.img = img_data
        self.histogram = self.compute_histogram()

    def get_frame_num(self):
        return self.frame_num
    
    def get_timestamp(self):
        return self.timestamp

    def get_img_data(self):
        return self.img

    def get_histogram(self):
        return self.histogram

    def to_dict(self):
        self.img = self.img.tolist()
        self.histogram = self.histogram.tolist()
        return self.__dict__


    def get_intensity(self, RGB_vals):
        """
        Calculates the intesity for the given RGB values.

        Parameters
        ----------
        vals : tuple
            The RGB values, in RGB order

        Returns
        -------
        float
            The intensity value
        """

        return (.299*RGB_vals[0]) + (.587*RGB_vals[1]) + (.114 * RGB_vals[2])    

    def compute_histogram(self):
        """
        Calculates the intensity for each pixel of the given image and creates
        a histogram.
        
        Returns
        -------
        np.array
            The intensity histogram
        """
        # if self.frame_num % 100 == 0:
        #     print("computing frame #", self.frame_num)

        width, height, channels = self.img.shape
        intensities = list()
        bins = list(range(0,250,10))
        bins.append(255)

        # for i in range(width):
        #     for j in range(height):
        #         intensities.append(self.get_intensity(self.img[i, j]))
        reds = self.img[:, :, 0] * 0.299
        greens = self.img[:, :, 1] * 0.587
        blues = self.img[:, :, 2] * 0.114
        r_and_g = np.add(reds, greens)
        intensities.append(np.add(r_and_g, blues))

        hist, bin_edges = np.histogram(intensities, bins=bins)
        return hist


    