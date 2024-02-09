from halo import Halo
from natsort import natsorted

from translation import translate
from utils import *

file_list = getFiles('./files/raw')

print_comic_list(file_list)

comicNumber = getUserInput("Enter the comic number: ")
comicName = file_list[int(comicNumber) - 1]

createFolder(f'./files/output/{comicName}')
isComplexBG = (getUserInput("Is there complex text background? (y/n): ") == 'y')

ocr_engine = 'paddle'

spinner = Halo(text='Creating Necessary Folders', spinner='dots')
spinner.start()

# Create the output folder if it doesn't exist
os.makedirs('./files/output', exist_ok=True)
createFolder('./files/temp')
createFolder('./files/steps')

spinner.succeed('Folders Created')

spinner = Halo(text='Extracting Comic', spinner='dots')
spinner.start()

extract_comic(comicName)
spinner.succeed('Comic Extracted')
comicLanguage = 'korean'
chapterImages = getFiles(f'./files/temp/{comicName}')

lang = comicLanguage

comicFile = chapterImages

spinner = Halo(text='Sorting Chapter Images', spinner='dots')
spinner.start()
comicFile = natsorted(comicFile)
spinner.succeed('Chapter Images Sorted')
images = [
    "./files/temp/" + comicName + "/" + x for x in comicFile]
spinner = Halo(text='Loading Images', spinner='dots')
spinner.start()
img_array = read_images(images)
spinner.succeed('Images Loaded')
spinner = Halo(text='Concatenating Images', spinner='dots')
spinner.start()
image = cv.vconcat(img_array)
spinner.succeed('Images Concatenated')
row = image.shape[0]
col = image.shape[1]
spinner = Halo(text='Detecting Blank Areas', spinner='dots')
spinner.start()
crop_array = get_crop_coordinates(image, row, col)
spinner.succeed('Blank Areas Detected')

spinner = Halo(text='Crop Images Along Blank Areas', spinner='dots')
spinner.start()
croppedImages = crop_image(crop_array, image, col)
spinner.succeed('Images Cropped')
spinner = Halo(text='Detecting Text Boxes', spinner='dots')
spinner.start()
texts, cords = ocr_images(croppedImages, lang, ocr_engine)
print(texts)
spinner.succeed('Text Boxes And Text Detected')
spinner = Halo(text='Translating Text', spinner='dots')
spinner.start()
trans = translate(*texts)
spinner.succeed('Texts Translated')

spinner = Halo(text='Cleaning Raw Text', spinner='dots')
spinner.start()
colors = clean_raw_text(croppedImages, *cords, isComplexBG=isComplexBG)
spinner.succeed('Raw Text Cleaned')

spinner = Halo(text='Printing Translated Text', spinner='dots')
spinner.start()
print_comic_text(croppedImages, cords, comicName, colors, isComplexBG, trans)
spinner.succeed('Translated Text Printed')
spinner = Halo(text='Creating Zip File', spinner='dots')
zip_files(comicName)
spinner.succeed('Zip File Created')
