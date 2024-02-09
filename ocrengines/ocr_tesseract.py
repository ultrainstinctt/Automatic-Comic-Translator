import pytesseract
import cv2 as cv


def preprocess_image(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.threshold(image, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    # dialate image
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    image = cv.dilate(image, kernel, iterations=1)
    return image


def main(region_of_interest, areas, lang):
    extracted_text = []
    temp = []
    for i in range(len(region_of_interest)):
        # print(f'Number of ROIs inside OCR: {len(ROIs)}')

        text = pytesseract.image_to_string(preprocess_image(region_of_interest[i]), lang=lang)
        lh = text.strip()
        lh = lh.replace("\n", " ")
        if lh != '':
            extracted_text.append(lh)
        else:
            print(f"area {i} is empty")
            temp.append(i)

    # print(areas)
    for i in range(len(temp)):
        areas.pop(temp[i] - i)
    print(f"areas inside: {areas}")
    return areas, extracted_text


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
