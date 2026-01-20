"""
Author : Mohammed Hisham
Function : This class is used to get generic / reusable logger, which can be used for logging in other project
modules.
"""
# Python modules.
from configparser import ConfigParser
import os

# User defined module.
import logging_package


class GetLogger:
    @staticmethod
    def get_logger():
        config = ConfigParser()
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        config_path = os.path.join(script_dir, 'LOGGING_LEVELS.config')
        # print(config_path)
        config.read(config_path)
        """
        1) back_up_count :
           keyword refers to max number of files which can be accounted for; after this threshold, files will simply be
           overwritten.

        2) rotating interval : refers to how often should logs be rotated.

        3) when : Details https://docs.python.org/3/library/logging.handlers.html

        """
        logger = logging_package.CustomLogger(is_console_handler=
                                              config.getboolean('LOGGING_LEVELS', 'is_console_handler'),
                                              is_enable_log_level_debug=
                                              config.getboolean('LOGGING_LEVELS', 'is_enable_log_level_debug'),
                                              is_enable_log_level_info=
                                              config.getboolean('LOGGING_LEVELS', 'is_enable_log_level_info'),
                                              is_enable_log_level_warning=
                                              config.getboolean('LOGGING_LEVELS', 'is_enable_log_level_warning'),
                                              is_enable_log_level_error=
                                              config.getboolean('LOGGING_LEVELS', 'is_enable_log_level_error'),
                                              is_enable_log_level_critical=
                                              config.getboolean('LOGGING_LEVELS', 'is_enable_log_level_critical'),
                                              back_up_count=
                                              config.getint('configurations', 'back_up_count'),
                                              rotating_interval=
                                              config.getint('configurations', 'rotating_interval'),
                                              when=
                                              str(config.get('configurations', 'when'))).return_logger()

        return logger
