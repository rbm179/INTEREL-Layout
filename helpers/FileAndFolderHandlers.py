# Python module.
from shutil import *
import csv
import os
from pathlib import *

# Calling Logging package
import logging_package as logstream
logger = logstream.GetLogger().get_logger()

'''Class to enable creation of folder trees and deletion.'''


class FolderTreeManage:
    def __init__(self, folder_list):
        self.folder_list = folder_list

    def remove_directory(self):
        for folder in self.folder_list:
            try:
                logger.info(f"Removing folder(s) {folder}.")
                rmtree(Path(folder))
                logger.info(f"Folder {folder} removal is complete !!!")
            except FileNotFoundError:
                pass

    def add_directory(self):
        for folder in self.folder_list:
            logger.info(f"Creating new folder(s) {folder}.")
            Path(folder).mkdir()
            logger.info(f"Folder(s) {folder} has been created !!!")


'''Class to enable writing csv file(s) into a folder'''


class WriteCSVFile:
    def __init__(self, file_path, data):
        self.file_path = Path(file_path)
        self.data = data

    def write_into_csv_file(self):
        with open(self.file_path, "a", newline='') as file_csv:
            csv_writer = csv.writer(file_csv)
            csv_writer.writerow(self.data)

    # This method can be used to remove .csv / .zip files.
    def remove_file(self):
        try:
            os.remove(self.file_path)
        except Exception as e:
            logger.info(e)


'''Class to enable appending contents to .txt file'''


class WriteTxtFile:
    def __init__(self, file_path, contents):
        self.file_path = Path(file_path)
        self.contents = contents

    def append_contents_to_text_file(self):
        with open(self.file_path, "a") as file_append:
            file_append.write(self.contents)


''' Get file size using OS module'''


class GetFileSize:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_size(self):
        global file_size_in_mb
        global file_size_in_gb

        # Getting file size in MB.
        try:
            file_size_in_mb = int(os.stat(self.file_path).st_size / (1024 * 1024))
            logger.info(f"[FILE_SIZE_IN_MB] : {file_size_in_mb} MB")
        except FileNotFoundError as e:
            logger.error(e)
            logger.error("[FILE_SIZE_IN_MB] : Application Launching for first time !!!")
            logger.error("[FILE_SIZE_IN_MB] : Assuming file size as 0 MB")
            file_size_in_mb = 0

        # Getting File size in GB
        try:
            file_size_in_gb = int(os.stat(self.file_path).st_size / (1024 * 1024 * 1024))
            logger.info(f"[FILE_SIZE_IN_GB] : {file_size_in_gb} MB")
        except FileNotFoundError as e:
            logger.error(e)
            logger.error("[FILE_SIZE_IN_GB] : Application Launching for first time !!!")
            logger.error("[FILE_SIZE_IN_GB] : Assuming file size as 0 GB")
            file_size_in_gb = 0
        return file_size_in_mb, file_size_in_gb



