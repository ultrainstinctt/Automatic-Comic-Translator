import numpy as np


def dominantColor(image):
    """
    The dominantColor function takes an image as input and returns the most frequent color in that image.
    The function is useful for determining what color a sign should be painted.

    :param image: Reshape the image into a 2d array
    :return: The most dominant color in an image
    """
    a2D = image.reshape(-1, image.shape[-1])
    col_range = (256, 256, 256)  # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)
