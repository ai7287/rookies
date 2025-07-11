import zipfile
import os

RESULT_DIR = 'uploads'

zip_file = zipfile.ZipFile('results.zip','w')

for root, dirs, files in os.walk(RESULT_DIR):
    for file in files:
        zip_file.write(os.path.join(root,file))
        
zip_file.close()
