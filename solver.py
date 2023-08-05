#!/usr/bin/python3


import os
import subprocess
import re
import cv2
import numpy as np
from tesserocr import PyTessBaseAPI, PSM
from PIL import Image

#TODO
"""
implement logging

testing:
	name jpg correctly
	create function to compare results to file
	evaluate results

imagemagick docs
https://github.com/ImageMagick/ImageMagick
https://imagemagick.org/Usage/transform/#vision
https://imagemagick.org/Usage/morphology/#edge-in


tesserocr
https://github.com/sirfz/tesserocr/
https://tesseract-ocr.github.io/tessdoc/APIExample.html
https://github.com/search?q=repo%3Atesseract-ocr%2Ftesseract+PSM_&type=code
https://github.com/tesseract-ocr/tesseract/blob/0768e4ff4c21aaf0b9beb297e6bb79ad8cb301b0/include/tesseract/capi.h#L72

"""

def transform_image(image):
    if not os.path.exists(image):
        print("the file doesnt exist")
        return
    cmd = f"convert {image} -density 300 -colorspace gray -alpha off -crop +0+20 -bordercolor White -border 10x10 -morphology Dilate FreiChen {image}_transform.jpg"
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR from executed shell command: {e}")

def bw_image(image):
    if not os.path.exists(image):
        print("the file doesnt exist")
        return
    cmd = f"convert {image} -threshold 60% {image}_bw.jpg"
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR from executed shell command: {e}")

    
def ocr_image(image_transform, set_psm):
    if not os.path.exists(image_transform):
        print("the file doesnt exist")
        return
    #initialize API
    with PyTessBaseAPI(psm=set_psm) as api:
#TODO
#        api.SetPageSegMode("PSM_SINGLE_BLOCK")          #PSM_SINGLE_BLOCK
# SET CONFIG PARAMETER
        api.SetVariable("tessedit_char_whitelist",  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-&!")
        """ 
        useless
        api.SetVariable("crunch_early_convert_bad_unlv_chs", "1")
        api.SetVariable("edges_use_new_outline_complexity", "1")
        api.SetVariable("tessedit_unrej_any_wd", "1")
        api.SetVariable("textord_heavy_nr", "1")
        api.SetVariable("words_default_fixed_limit", "3")
        api.SetVariable("tessedit_enable_dict_correction", "1")
        """
        api.SetImageFile(image_transform)
        result = remove_line_breaks(api.GetUTF8Text())
        print_final_result(result)
        # compare result
        compare_result("heart break", result)
#        print(api.AllWordConfidences())


def remove_line_breaks(raw_text):
    return re.sub(r'\s+', ' ', raw_text)


def print_final_result(result):
    print(result)

def compare_result(solution, result):
    result = solution.lower() == result.lower()
    if result:
        print("IT WORKS")
    return result


# OPENCV TESTS
def denoise_image(input_image):
    image = cv2.imread(input_image)
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    cv2.imwrite(input_image + "_final.jpg", denoised_image)
    return denoised_image


# Get the home directory path
home_path = os.path.expanduser("~")

image = home_path + "/captcha/solver/sample.jpg"
image_transform = image + "_transform.jpg"
image_final = image_transform + "_final.jpg"
image_bw = image_transform + "_bw.jpg"

#start
transform_image(image)
bw_image(image_transform)


#modify image
denoise_image(image_transform)



for psm_type in [PSM.OSD_ONLY, PSM.AUTO_OSD, PSM.AUTO_ONLY, PSM.AUTO, PSM.SINGLE_COLUMN, PSM.SINGLE_BLOCK_VERT_TEXT, PSM.SINGLE_BLOCK, PSM.SINGLE_LINE, PSM.SINGLE_WORD, PSM.CIRCLE_WORD, PSM.SINGLE_CHAR, PSM.SPARSE_TEXT, PSM.SPARSE_TEXT_OSD, PSM.RAW_LINE, PSM.COUNT]:
    print(psm_type)
#original image
    print("ORIGINAL")
    ocr_image(image, psm_type)
#transformed image
    print("TRANSFORMED")
    ocr_image(image_transform, psm_type)
#final image
    print("FINAL")
    ocr_image(image_final, psm_type)
#bw image
    print("BW")
    ocr_image(image_bw, psm_type)
    print("-----------END-----------")


#print("PSM_OSD_ONLY,")
#ocr_image(image_transform, PSM.OSD_ONLY)



"""
psm types
  PSM_OSD_ONLY,
  PSM_AUTO_OSD,
  PSM_AUTO_ONLY,
  PSM_AUTO,
  PSM_SINGLE_COLUMN,
  PSM_SINGLE_BLOCK_VERT_TEXT,
  PSM_SINGLE_BLOCK,
  PSM_SINGLE_LINE,
  PSM_SINGLE_WORD,
  PSM_CIRCLE_WORD,
  PSM_SINGLE_CHAR,
  PSM_SPARSE_TEXT,
  PSM_SPARSE_TEXT_OSD,
  PSM_RAW_LINE,
  PSM_COUNT
"""
