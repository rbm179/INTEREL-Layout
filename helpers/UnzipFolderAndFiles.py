from zipfile import ZipFile
from pathlib import *


class UnzipFolderAndFiles:
    def __init__(self, zip_file_path, extracted_folder_path):
        self.zip_file_path = Path(zip_file_path)
        self.extracted_folder_path = Path(extracted_folder_path)

    def unzip_folder_and_files(self):
        with ZipFile(self.zip_file_path, 'r') as zObject:
            zObject.extractall(path=self.extracted_folder_path)
