import os
import zipfile
from pathlib import *
from os.path import basename


class ZipFolderAndFiles:
    def __init__(self, dest_file_name, source_file_name):
        self.dest_file_name = dest_file_name
        self.source_file_name = source_file_name

    @staticmethod
    def zip_dir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, '..')))

    # Destination file name MUST have a ZIP extension.
    # This method MUST be used if you want to ZIP folders and NOT files.
    def zip_folder_and_files(self):
        with zipfile.ZipFile(self.dest_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            self.zip_dir(self.source_file_name, zipf)

    # This method can zip only files and NOT folders.
    # Base name method is invoked to ensure that when files are zipped, full relative path is
    # not taken in consideration. source file path cannot be a folder.
    def zip_only_files(self):
        zip_obj = zipfile.ZipFile(Path(self.dest_file_name), "w", zipfile.ZIP_DEFLATED)
        zip_obj.write(Path(self.source_file_name), basename(self.source_file_name))
        zip_obj.close()



