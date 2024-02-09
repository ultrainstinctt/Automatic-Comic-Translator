import cv2 as cv
import numpy as np
from paddleocr import PaddleOCR
from ocrengines import ocr_paddle, ocr_tesseract


def ocr(image, lang, imageNumber, ocr_engine):
    """
    The ocrengines function takes in an image and a language, runs the PaddleOCR engine on it,
    and returns the bounding boxes of each character in the image.Then uses Tessaract to extract the text.
    
    
    :param image: Pass the image to be used for ocrengines
    :param lang: Specify the language of the text in the image
    :param imageNumber: To keep track of the image number
    :return: The areas and extracted text
    :doc-author: Trelent
    """
    image3 = np.copy(image)
    # need to run only once to download and load model into memory
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, show_log=False)
    # need to run only once to download and load model into memory
    result = ocr.ocr(image, rec=False)
    X = np.array(result)
    X = np.asarray(X, dtype='int')
    # print("value of x")
    # print(X)
    external_poly = np.array(X[0], dtype=np.int32)

    blankImage = np.zeros((image.shape[0], image.shape[1], 1), np.uint8)

    cv.fillPoly(blankImage, external_poly, 255)

    cv.imwrite(f"files/steps/blank{imageNumber}.jpg", blankImage)
    #    Create rectangular structuring element and dilate
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 5))
    dilate = cv.dilate(blankImage, kernel, iterations=5)
    cv.imwrite(f"files/steps/dilate{imageNumber}.jpg", dilate)

    # Find contours and draw rectangle
    if (lang == 'korean'):
        lang = 'kor'
    elif (lang == 'japanese'):
        lang = 'jpn'
    elif (lang == 'en'):
        lang = 'eng'
    elif (lang == 'ch'):
        lang = 'chi_sim'
    ROIs = []
    areas = []
    cnts = cv.findContours(dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    mask = np.zeros(image.shape, dtype=np.uint8)

    for c in cnts:
        if len(c) < 5:
            continue
        ec = cv.fitEllipse(c)
        cv.ellipse(mask, ec, (255, 255, 255), -1)
        cv.bitwise_and(image, mask)

    for c in cnts:
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(image3, (x, y), (x + w, y + h), (150, 80, 255), 2)
        crop = image[y:y + h, x:x + w]

        gray = cv.cvtColor(crop, cv.COLOR_BGR2GRAY)
        ROIs.append(crop)
        areas.append([x, y, w, h])
        # print(x, y, w, h)
    print(f"printing areas {areas}")
    cv.imwrite(f"files/steps/outline{imageNumber}.jpg", image3)
    if ocr_engine == 'paddle':
        return ocr_paddle.main(ROIs, areas, 'en')
    elif ocr_engine == 'tesseract':
        return ocr_tesseract.main(ROIs, areas, lang)
