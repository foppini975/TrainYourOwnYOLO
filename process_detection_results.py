import sys
import csv
from PIL import Image
import io
import os
import make_ppt
import argparse
import re
import pdb

# python process_detection_results.py -d -l 2 ./Data/Source_Images/Test_Image_Detection_Results/Detection_Results.csv

def get_max_height_annotation(texts):
    max_height = 0
    for text in texts:
        height = abs(text.bounding_poly.vertices[0].y - text.bounding_poly.vertices[2].y)
        if height > max_height:
            max_height = height
    return max_height

def detect_text(path, content = None):
    """Detects text in the file."""
    from google.cloud import vision
    
    client = vision.ImageAnnotatorClient()

    if path is not None:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    max_height = get_max_height_annotation(texts)
    print("Max height = {}".format(max_height))
    texts.sort(key=lambda x: x.bounding_poly.vertices[2].y-x.bounding_poly.vertices[0].y, reverse=True)

    for text in texts:
        print('{} --> "{}"'.format(text.bounding_poly.vertices[2].y-text.bounding_poly.vertices[0].y, text.description))
        """
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
        """

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    pdb.set_trace()
    return texts

def get_price(texts):
    for text in texts:
        try:
            float(text.description)
            return text.description
        except ValueError:
            pass
    return None

parser = argparse.ArgumentParser()
parser.add_argument("csv_result", type=str, help="Detection results csv file")
parser.add_argument("-l", "--label", type=int, help="label")
parser.add_argument("-d", "--details", action='store_true', help="detailed powerpoint")
parser.add_argument("-o", "--ocr", action='store_true', help="OCR execution")

args = parser.parse_args()

DETECTION_RESULT_CSV = args.csv_result

with open(DETECTION_RESULT_CSV, newline='') as csv_file:
    csv_data = list(csv.reader(csv_file))

# ['image', 'image_path', 'xmin', 'ymin', 'xmax', 'ymax', 'label', 'confidence', 'x_size', 'y_size']
[IMAGE_PATH] = [i for i,x in enumerate(csv_data[0]) if x=='image_path']
[LABEL] = [i for i,x in enumerate(csv_data[0]) if x=='label']
[XMIN] = [i for i,x in enumerate(csv_data[0]) if x=='xmin']
[YMIN] = [i for i,x in enumerate(csv_data[0]) if x=='ymin']
[XMAX] = [i for i,x in enumerate(csv_data[0]) if x=='xmax']
[YMAX] = [i for i,x in enumerate(csv_data[0]) if x=='ymax']

image_results_list = []

if args.details is True:
    ppt_details = make_ppt.create_presentation()
title_font_size = 18
body_font_size = 18

for row_index, csv_row in enumerate(csv_data[1:]):
    if args.label is not None and str(args.label) != csv_row[LABEL]:
        continue
    print("{} --> {}: Label {}".format(row_index, csv_row[IMAGE_PATH], csv_row[LABEL]))
    if csv_row[IMAGE_PATH] not in image_results_list:
        image_results_list.append(csv_row[IMAGE_PATH])
    if args.details is True:
        filename, file_extension = os.path.splitext(csv_row[IMAGE_PATH])
        image = Image.open(csv_row[IMAGE_PATH])
        cropped_image = image.crop((int(csv_row[XMIN]), int(csv_row[YMIN]), int(csv_row[XMAX]), int(csv_row[YMAX]))) 
        # conversion of cropped_image to byte array
        imgByteArr = io.BytesIO()
        cropped_image.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        new_image_filename = filename + "_temp" + file_extension
        cropped_image.save(new_image_filename)
        if args.ocr is True:
            print("Detecting text")
            texts = detect_text(path = None, content = imgByteArr)
            title_string = get_price(texts)
            body_string = texts[0].description
        else:
            title_string = os.path.basename(csv_row[IMAGE_PATH])
            body_string = ""
        make_ppt.add_slide(ppt_details, title_string, new_image_filename, body_string, title_font_size, body_font_size)
        os.remove(new_image_filename)
if args.details is True:
    make_ppt.save_presentation(ppt_details, "details.pptx")
    print("Saved presentation details.pptx")
    
# summary
ppt_summary = make_ppt.create_presentation()
image_results_list.sort()
for image_file in image_results_list:
#texts.sort(key=lambda x: x.bounding_poly.vertices[2].y-x.bounding_poly.vertices[0].y, reverse=True)
    filename, file_extension = os.path.splitext(re.sub("/Test_Images/", "/Test_Image_Detection_Results/", image_file))
    result_image = filename + "_promo" + file_extension
    make_ppt.add_slide(ppt_summary, os.path.basename(image_file), result_image, "", 18, 18)
make_ppt.save_presentation(ppt_summary, "summary.pptx")
print("Saved presentation summary.pptx")

print("Done! Exiting...")
