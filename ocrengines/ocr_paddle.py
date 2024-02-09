from paddleocr import PaddleOCR


def extract_last_level(arr):
    if isinstance(arr, list) and arr:
        if all(isinstance(subarr, list) for subarr in arr):
            return [extract_last_level(subarr) for subarr in arr]
        else:
            return arr[-1]
    else:
        return arr


def extract_text_string(array):
    text_string = ''
    if len(array) > 0:
        for item in array:
            if len(item) > 0:
                arr = extract_last_level(item)
                print(f'text: {arr[0]}')
                for i in range(len(arr)):
                    text_string += arr[i][0] + ' '
        print(f'OCR result: {text_string}')
        return text_string
    else:
        return text_string


def main(region_of_interest, areas, lang):
    ocr = PaddleOCR(use_angle_cls=True, lang='korean',
                    show_log=False)  # need to run only once to load model into memory
    extracted_text = []
    temp = []
    for i in range(len(region_of_interest)):
        # print(f'Number of ROIs inside OCR: {len(ROIs)}')
        result = ocr.ocr(region_of_interest[i], cls=True, )
        print(result)
        text = extract_text_string(result)
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
