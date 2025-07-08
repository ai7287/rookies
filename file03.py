import os

dir_path = "uploads"
all_files = os.listdir(dir_path)

txt_files =[]

for file in all_files:
    if file.endswith(".txt"):
        txt_files.append(file) 

# 1.txt, 2.txt /uploads/1.txt
for filename in txt_files:
    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'r', encoding="utf-8") as file:
        print(f"{filename} 내용:")
        print(file.read())
        print("-" * 40)