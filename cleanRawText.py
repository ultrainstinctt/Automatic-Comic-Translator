import cv2 as cv
from dominantColor import dominantColor


def cleanRaw(image, cords, isComplexBG):
    """
    The cleanRaw function takes an image and a list of bounding boxes (cords) as arguments.
    It then iterates through the list of bounding boxes, drawing a rectangle with color white
    or most dominant color depending on isComplexBG variableover each box in the image.
    The function returns an image with all of the specified boxes covered in white.

    :param image: Pass the image to be processed
    :param cords: Specify the coordinates of the bounding boxes
    :param isComplexBG: Determine whether or not the color of the bounding box should be determined by most dominant color
    :return: The image with the text removed
    :doc-author: Trelent
    """
    colors = []
    for i in range(len(cords)):
        if len(cords) == 0:
            return image
        x, y, w, h = cords[i]
        if isComplexBG:
            tempimg = image[y:y + h, x:x + w]
            colorz = dominantColor(tempimg)
            color = tuple(map(int, colorz))
            colors.append(colorz)
        else:
            color = (255, 255, 255)
            colors.append(color)
        # print(f'color: {color}')
        cv.rectangle(image, (x, y), (x + w, y + h), color, -1)
    return image, colors
