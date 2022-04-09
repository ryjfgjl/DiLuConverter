dir = r'D:/Projects/ExcelToDatabase/test'
import os
from collections import defaultdict

excels_dict = defaultdict()
files_list = []
for root,dirs,files in os.walk(dir):
    root = root.replace(dir,'')[1:]
    if len(root) > 1:
        root = root + '\\'
    for file in files:
        file = root+file
        print(file)
        files_list.append(file)

