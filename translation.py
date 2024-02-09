from googletrans import Translator

translator = Translator()


def translate(*text):
    """
    The translate function takes a list of lists as an argument.
    It then iterates over the inner lists and concatenates each string in the inner list.
    The result is saved in a variable called 'result'.
    Then, using Google Translate API, it translates 'result' into Bengali language and saves it to another variable called translatedText.
    Finally, it splits translatedText by newline character ('\n') and stores each line into an array inside translatedTextArray.

    :param *text: Pass a variable number of arguments to the function
    :return: A list of lists containing the translated text
    :doc-author: Trelent
    """
    # print(len(text))
    result = ''
    # iterate over the inner lists and concatenate each string
    for inner_list in text:
        for string in inner_list:
            result += string
            result += ' \n '
    # print(result)

    translated = translator.translate(result, dest='en')
    # print(translated.text)
    # save result in output.txt
    translatedText = translated.text.split('\n')
    print(translatedText)
    print(len(translatedText))
    translatedTextArray = []

    counter = 0
    for i in range(len(text)):
        tempArray = []
        # print(f'length of inner list {i} is {len(text[i])}')
        for j in range(len(text[i])):
            # print(f'counter is {counter}')
            # print(f'j is {j}')
            # translatedTextArray[i][j] = translatedText[counter]
            tempArray.append(translatedText[counter])
            counter += 1
        translatedTextArray.append(tempArray)
    return translatedTextArray
