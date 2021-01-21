# Merge every PDF document on this folder

from PyPDF2 import PdfFileMerger
from os import listdir
import os
from os import path

input_dir = f"{path.dirname (path.abspath(__file__))}/"

merge_list = []

for x in listdir(input_dir):
    if not x.endswith('.pdf'):
        continue
    merge_list.append(input_dir + x)

merger = PdfFileMerger()

for pdf in merge_list:
    merger.append(pdf)

merger.write(f"{input_dir}merged_pdf.pdf") #your output directory
merger.close()
