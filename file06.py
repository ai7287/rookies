import os
import re

dir_path = "uploads"
all_files = os.listdir(dir_path)

txt_files = []

for file in all_files:
    if file.endswith(".txt"):
        txt_files.append(file)

#1.txt, 2.txt /uploads/1.txt
for filename in txt_files:
    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if line.startswith("#") or line.startswith("//"):
                print(f"{file_path} {index+1}라인 : 탐지: {line.strip()}")