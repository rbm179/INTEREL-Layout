# Python modules.
import os
from tqdm import tqdm
import shutil
from pathlib import *
import logging_package as logstream
logger = logstream.GetLogger().get_logger()


class FileCopySourceDestination:
    def __init__(self, src_folder=None, dest_folder=None, ext_file_name=None):
        self.src_folder = src_folder
        self.dest_folder = dest_folder
        self.ext_file_name = ext_file_name

    # This method show file copy progress using TQDM and is slower.
    def file_copy_source_destination(self):

        try:
            # Get the total size of the source folder
            total_size = sum(f.stat().st_size for f in Path(self.src_folder).glob('**/*') if f.is_file())
            # Copy the contents of the source folder to the destination folder
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
                for file in Path(self.src_folder).glob('**/*'):
                    if file.is_file():
                        shutil.copy2(str(file), str(self.dest_folder / file.relative_to(self.src_folder)))
                        progress_bar.update(file.stat().st_size)
            return 0

        except Exception as e:
            logger.exception(e)
            logger.error(e)
            return 1

    # This method does not show progress of file copy and is faster.
    def copy_selected_files(self):

        try:
            # List files
            files = os.listdir(self.src_folder)

            # Iterate over the files and move only the .txt files
            for file in files:
                if file.endswith(self.ext_file_name):
                    source_path = os.path.join(self.src_folder, file)
                    destination_path = os.path.join(self.dest_folder, file)
                    logger.info(f"Source folder to copy {self.src_folder}")
                    logger.info(f"Destination folder to copy {self.dest_folder}")
                    logger.info(f"Source File path to copy : {source_path}")
                    logger.info(f"Destination File path to copy : {destination_path}")
                    shutil.copy(source_path, destination_path)
            logger.info(f"Return code when copying : {0}")
            return 0

        except Exception as e:
            logger.error(e)
            logger.exception(e)
            logger.error(f"Return code when copying : {1}")
            return 1

