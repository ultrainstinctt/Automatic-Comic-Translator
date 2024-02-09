import cv2 as cv
import textwrap


def putText(image, text, cords, font, size, color, thickness, fileNumber):
    print("putText called")
    print(text)
    for i in range(len(cords)):
        if len(cords) == 0:
            continue
        x, y, w, h = cords[i]
        print(x, y, w, h)

        # characterWidth = cv.getTextSize(text[i], font, size, 1)
        (text_width, text_height), baseline = cv.getTextSize(text[i], font, size, thickness)
        print("text_width", text_width)
        print(text_width, text_height)

        cv.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)
        charwidth = text_width / len(text[i])
        charLength = int(w / charwidth)
        print(charLength, w, charwidth)
        # Draw the text on the image
        lines = textwrap.wrap(text[i], charLength)
        print(lines)
        k = y
        for line in lines:
            print(line)
            cv.putText(image, line, (x, k), font, size, color, 1, cv.LINE_AA)
            cv.imwrite(f"files/output/{fileNumber}.jpg", image)
            k += text_height
    return image
