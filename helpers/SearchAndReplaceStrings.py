import logging_package as logstream
logger = logstream.GetLogger().get_logger()


class SearchAndReplaceStrings:
    def __init__(self,
                 file_path=None,
                 search_string=None,
                 replace_string=None):
        self.file_path = file_path
        self.search_string = search_string
        self.replace_string = replace_string

    def search_and_replace_strings(self):

        logger.info(f"Search string - '{self.search_string}'")

        # Define Global variable for parsing the Text:
        temp = ""

        # Opening the cursor
        with open(self.file_path, "r") as file_temp:

            for line in file_temp:
                line = line.strip()
                if self.search_string in line:
                    logger.info(f"Search string '{self.search_string}' has been found !!!")
                    temp = line

        # Reading the file using read method.
        with open(self.file_path, "r") as file_temp:
            contents = file_temp.read()

        # Replacing the parsed string with new string:
        contents = contents.replace(temp, self.replace_string)

        # Writing the File:
        logger.info(f"Replacing string OLD '{self.search_string}' string with NEW '{self.replace_string}' string.")
        try:
            with open(self.file_path, "w") as file_write:
                file_write.write(contents)
        except PermissionError:
            exit()
