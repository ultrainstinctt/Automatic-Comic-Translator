import cv2 as cv
import textwrap
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def putText(image, textArray, cordArray, fileNumber, comicNmae, colors, isComplexBG):
    """
    The putText function takes in an image, a list of strings to be written on the image,
    a list of Array containing the coordinates for where each string should be written on the image,
    the number of the file being processed (for naming purposes), and a boolean value indicating whether or not
    the background is complex. The function then writes each string onto its specified location on the given image.

    :param image: Draw the text on
    :param textArray: Store the array text String that is to be printed on the image
    :param cordArray: Store the array of cordinates of the text that is to be printed on image
    :param fileNumber: Keep track of the file number
    :param comicNmae: To store the images in the correct folder
    :param colors: Determine the color of the text
    :param isComplexBG: Determine if the background is complex or not
    :doc-author: Trelent
    """

    b, g, r, a = 0, 0, 0, 0
    fontpath = "./fonts/Atma-Regular.ttf"
    font = ImageFont.truetype(fontpath, 32)
    # print("putText called")
    # print(textArray)
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    for i in range(len(cordArray)):
        if len(cordArray) == 0:
            return image
        x, y, w, h = cordArray[i]
        # print(x, y, w, h)
        text_width, text_height = draw.textsize(textArray[i], font)

        # print("text_width", text_width)
        # print(text_width, text_height)

        charwidth = text_width / len(textArray[i])
        charLength = int(w / charwidth)
        # print(charLength, w, charwidth)
        # Draw the text on the image
        lines = textwrap.wrap(textArray[i], charLength)
        # print(lines)
        k = y
        if isComplexBG:
            b, g, r = 255 - colors[i][0], 255 - colors[i][1], 255 - colors[i][2]
        for line in lines:
            # print(line)
            # cv.putText(image, line, (x, k), font, size, color, 1, cv.LINE_AA)
            draw.text((x, k), line, font=font, fill=(b, g, r, a))
            k += text_height
        image = np.array(img_pil)
    cv.imwrite(f"files/output/{comicNmae}/{fileNumber}.jpg", image)
