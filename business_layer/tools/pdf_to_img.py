import os
from pdf2image import convert_from_path

def pdf_to_img(pdf_path,output_path):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(output_path)