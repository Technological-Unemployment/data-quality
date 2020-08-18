import os
import tempfile
import pandas as pd
from PIL import Image
from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError)
import pytesseract
import time
import nltk
import re
import numpy as np
from io import StringIO
from nltk.tokenize import word_tokenize
import polyleven
PdfPath = r'C:\Users\Computer\Desktop\NLP_Resume'
OutputPath = r"C:\\Users\\Computer\\Desktop\\output\\"

def poly_ratio(s1, s2):
        dist = polyleven.levenshtein(s1, s2)
        lensum = len(s1) + len(s2)
        return int((lensum - dist) / lensum * 100)
match=80  
result1=[]

with open("C:\\Users\\Computer\\Desktop\\doorway_project\\dedup1.csv") as file1:
    list_names=file1.read()
    plist = list_names.split('\n')
### http://blog.alivate.com.au/poppler-windows/ to add poppler if need be
########### https://stackoverflow.com/questions/14640509/python-error-when-importing-image-to-string-from-tesseract
def convert_pdf(PdfPath, OutputPath):
    for pdf_file in os.listdir(PdfPath):
        # save temp image files in temp dir, delete them after we are finished  fmt="jpeg", jpegopt={"quality": 100,"progressive": True,"optimize": True}
        with tempfile.TemporaryDirectory() as temp_dir:
            # print('created temporary directory', temp_dir)
            # convert pdf to multiple image
            joined = os.path.join(PdfPath, pdf_file)
            imgs = convert_from_path(joined, dpi=400, thread_count=1, output_folder=temp_dir) ##, poppler_path=r"C:\\Users\\Computer\\poppler-0.68.0_x86\\poppler-0.68.0/bin"
            # find minimum width of images
            min_img_width = min(i.width for i in imgs)
            # find total height of all images
            total_height = 0
            for i, img in enumerate(imgs):
                total_height += imgs[i].height
            # create new image object with width and total height
            merged_image = Image.new(imgs[0].mode, (min_img_width, total_height))
            # paste images together one by one
            y = 0
            for img in imgs:
                merged_image.paste(img, (0, y))
                y += img.height
            # save merged image
            newfilename = pdf_file[:-4] + str(i + 1) + '.jpg'
            output_file_name = os.path.join(OutputPath, newfilename)
            merged_image.save(output_file_name)
convert_pdf(PdfPath, OutputPath)
# Text extraction from multiple image files using Python
# Path is given for for 64 bit installer
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
f = []
t = []
document = []
#input_dir = OutputPath
for root, dirs, filenames in os.walk(OutputPath):
    for filename in filenames:
        try:
            print(filename)
            f.append(filename)
            img = Image.open(OutputPath + filename)
            document = pytesseract.image_to_string(img, lang='eng')
            t.append(document)
            word_tokens = list(nltk.word_tokenize(document))
        except:
            continue
#df = pd.DataFrame()
#df = pd.DataFrame(list(zip(f, t)), columns=['file_Name', 'Text'])
#df.to_excel('file2.xlsx',index=False)

     #t[0]
        for feature in plist:
            lenfeature = len(feature.split(" "))
            for i in range (len(word_tokens)-lenfeature+1):
                wordtocompare = ""
                j=0
                for j in range(i, i+lenfeature):
                    if re.search(r'[,!?{}\[\]\"\"\'\']',word_tokens[j]):
                        break
                    wordtocompare = wordtocompare+" "+word_tokens[j].lower()
                if wordtocompare != "":
                    if(poly_ratio(wordtocompare,feature.lower())>match):
                        result1.append([filename,wordtocompare,feature,i,j])
            print(result1)
            
            

# match_df = titlematch.match()
