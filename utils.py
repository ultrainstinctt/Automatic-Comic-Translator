import shutil
import os
import zipfile
import cv2 as cv
from ocr import ocr
from cleanRawText import cleanRaw
from printRegional import putText


def getUserInput(text):
    """
    The getUserInput function prompts the user for input and returns it as a string.
        It is used to prompt the user for their input, which will be stored in a variable called 'userInput'.


    :param text: Display a message to the user
    :return: The user input
    :doc-author: Trelent
    """
    userInput = input(text)
    return userInput


def createFolder(folderPath):
    """
    The createFolder function creates a folder at the specified path if it does not already exist.
    If exist it will delete the contents of the folder.

    :param folderPath: Specify the path to the folder that is being created
    :return: A boolean value
    :doc-author: Trelent
    """
    if os.path.exists(folderPath):
        shutil.rmtree(folderPath)
    os.mkdir(folderPath)


def getFiles(directory='./files/raw'):
    """
    The getFiles function returns a list of all the files in the specified directory.
    The default directory is ./files/raw, but this can be changed by passing an argument.

    :param directory='./files/raw': Tell the function where to look for files
    :return: A list of all the files in the specified directory
    :doc-author: Trelent
    """
    return os.listdir(directory)


def print_comic_list(comic_list):
    """
    The print_comic_list function prints out a list of comics in the comic_list.
    It takes one argument, comic_list, which is a list of strings.

    :param comic_list: Pass a list of comic files to the print_comic_list function
    :return: A list of comic files
    :doc-author: Trelent
    """
    for i, file in enumerate(comic_list):
        print(f'{i + 1}. {file}')


def extract_comic(comic_name):
    """
    The extract_comic function extracts the comic from its zip file and places it in a temporary folder.
    The function takes one argument, which is the name of the comic.

    :param comic_name: Tell the function which comic to extract
    :doc-author: Trelent
    """
    with zipfile.ZipFile(f'./files/raw/{comic_name}', 'r') as zip_ref:
        zip_ref.extractall(f'./files/temp/{comic_name}')


def read_images(images):
    """
    The read_images function reads in the images from the list of image paths using cv.imread
     and returns a list of images.

    :return: A list of images
    :doc-author: Trelent
    """
    img = []
    for i in images:
        # print(i)
        img.append(cv.imread(i))
    return img


def get_crop_coordinates(image, row, col):
    """
    The get_crop_coordinates function takes in an image and returns a list of coordinates that indicate the start
    and end of each crop. The function first converts the image to grayscale, then blurs it using a Gaussian blur,
    then thresholds it using Otsu's method. It then iterates through every row in the thresholded image until it finds
    a row where all pixels are black (indicating that this is a blank space). Once such a row is found, we know that this
    is the top boundary for our crop. We increment i by 600 pixels and continue searching for rows with no black pixels until


    :param image: Pass the image to be cropped
    :return: An array of the coordinates where each row is cropped
    :doc-author: Trelent
    """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7, 7), 0)
    thresh = cv.threshold(
        blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    crop_array = [0]
    i = 600
    while i < row:
        flag = 0
        for j in range(1, col, 1):
            if thresh[i][j] == thresh[i][0]:
                continue
            else:
                flag = 1
                break
        if flag == 0:
            crop_array.append(i)
            i += 600
        else:
            i += 3
    crop_array.append(row)
    return crop_array


def crop_image(crop_array, image, col):
    """
    The crop_image function takes an image and crops it into a smaller image based on the crop_array.
    It then saves each cropped image to a file called &quot;crop#.jpg&quot; where # is the number of that specific
    image in the array, and returns an array of all cropped images as well as their coordinates.

    :param crop_array: Define the start and end of each row
    :param image: Specify the image to be processed
    :param col: Specify the width of the image
    :param lang: Specify the language of the text in the image
    :return: The cropped images, the text in those images and the coordinates of each image
    :doc-author: Trelent
    """
    texts = []
    cords = []
    croppedImages = []
    imageNumber = 0
    for i in range(len(crop_array) - 1):
        crop = image[crop_array[i]:crop_array[i + 1], 0:col]
        cv.imwrite(f"files/steps/crop{i}.jpg", crop)
        croppedImages.append(crop)
    return croppedImages


def ocr_images(croppedImages, lang, ocr_engine):
    """
    The ocr_images function takes in a list of cropped images and returns a list of the text in each image.

    :param croppedImages: Specify the images to be processed
    :param lang: Specify the language of the text in the image
    :return: A list of the text in each image
    """
    texts = []
    cords = []
    imageNumber = 0
    for i in croppedImages:
        cord, text = ocr(i, lang, imageNumber, ocr_engine)
        imageNumber += 1
        if len(text) != 0:
            texts.append(text)
        cords.append(cord)
    return texts, cords


def clean_raw_text(croppedImages, *cords, isComplexBG):
    """
    The clean_raw_text function takes in a list of cropped images and the coordinates
    of the bounding box for each image. It then returns a list of cleaned images,
    where each image is just the text within its respective bounding box.

    :param croppedImages: Store the images that are cropped from the original image
    :param *cords: Pass in the coordinates of the bounding box that we want to crop
    :param isComplexBG: Determine whether the background is complex or not
    :return: A list of the colors of each image
    :doc-author: Trelent
    """
    colors = []
    for i in range(len(croppedImages)):
        croppedImages[i], tempColor = cleanRaw(croppedImages[i], cords[i], isComplexBG)
        colors.append(tempColor)
    return colors


def zip_files(comicName):
    """
    The zip_files function creates a zip file of the translated images.
    The function takes one argument, comicName, which is the name of the comic folder.

    :param comicName: Create a zip file with the translated images
    :return: The zip file
    :doc-author: Trelent
    """
    translatedImages = getFiles(f'./files/output/{comicName}')
    with zipfile.ZipFile(f'./files/output/Tanslated- {comicName}', mode='w') as archive:
        for file in translatedImages:
            archive.write(f'./files/output/{comicName}/{file}',
                          arcname=os.path.basename(f'./files/output/{comicName}/{file}'))


def print_comic_text(croppedImages, cords, comicName, colors, isComplexBG, trans):
    """
    The print_comic_text function takes in the cropped images, their corresponding text
    coordinates, and the comic name. It then iterates through each image and draws a box around
    the text with its corresponding color. The function also writes out the text to each image.

    :param croppedImages: Store the cropped images of each panel
    :param cords: Store the coordinates of the text that is to be printed on each image
    :param comicName: Name the comic
    :param colors: Determine the color of the text
    :param isComplexBG: Determine whether the background is complex or not
    :param trans: Store the text that will be printed on each panel
    :return: The text of the comic
    :doc-author: Trelent
    """
    j = 0
    for i in range(len(croppedImages)):
        if len(cords[i]) == 0:
            cv.imwrite(f"files/output/{comicName}/{i}.jpg", croppedImages[i])
        else:
            putText(croppedImages[i], trans[j], cords[i], i, comicName, colors[i], isComplexBG)
            j += 1
