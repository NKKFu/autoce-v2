# Merge every PDF document on this folder

from PyPDF2 import PdfFileMerger, PdfFileReader
from os import listdir
import os
from os import path

input_dir = f"{path.join(path.dirname (path.abspath(__file__)), 'backup-pdf')}"
print(input_dir)
merge_list = []

for x in listdir(input_dir):
    if not x.endswith('.pdf'):
        continue
    merge_list.append(PdfFileReader(open(path.join(input_dir, x), 'rb')))

merger = PdfFileMerger()

for pdf in merge_list:
    merger.append(pdf)

merger.write(path.join(input_dir, 'merded_pdf.pdf')) #your output directory
merger.close()