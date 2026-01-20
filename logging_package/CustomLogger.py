"""
Author : Mohammed Hisham
Function : This is a re-usable custom logger, which can be repurposed for logging across different modules.
"""

import logging
import logging.handlers as handlers
import inspect
from pathlib import *
import sys
import os

"""
Useful Reference links.
https://docs.python.org/3/library/logging.handlers.html
https://docs.python.org/3/library/logging.html#logging-levels
https://tutorialedge.net/python/python-logging-best-practices/
"""


class CustomLogger:

    def __init__(self,
                 is_console_handler=None,
                 is_enable_log_level_debug=None,
                 is_enable_log_level_info=None,
                 is_enable_log_level_warning=None,
                 is_enable_log_level_error=None,
                 is_enable_log_level_critical=None,
                 back_up_count=None,
                 rotating_interval=None,
                 when=None):
        self.is_console_handler = is_console_handler
        self.is_enable_log_level_debug = is_enable_log_level_debug
        self.is_enable_log_level_info = is_enable_log_level_info
        self.is_enable_log_level_warning = is_enable_log_level_warning
        self.is_enable_log_level_error = is_enable_log_level_error
        self.is_enable_log_level_critical = is_enable_log_level_critical
        self.back_up_count = back_up_count
        self.rotating_interval = rotating_interval
        self.when = when

    def return_logger(self):

        # Get the path of CustomLogger.py
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Getting logger name.
        logger_name = inspect.stack()[1][3]

        # Logger object.
        logger = logging.getLogger(logger_name)

        # This conditional check to avoid duplication.
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            # CONSOLE handler for console logs, level is deliberately set to INFO to show all logs on the console
            # using stream handler.
            if self.is_console_handler is True:
                console_handler = logging.StreamHandler(sys.stdout)
                # console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

                # This will prevent duplication of logs.
                logger.propagate = False

            # CRITICAL Handler - will contain ONLY logs of FATAL / CRITICAL TYPE.
            if self.is_enable_log_level_critical is True:

                # Creating folders for file retention.
                try:
                    folder = os.path.join(script_dir, 'LOG_CRITICAL')
                    # Path("./LOG_CRITICAL").mkdir()
                    Path(folder).mkdir()
                except FileExistsError:
                    pass

                file = os.path.join(script_dir, 'LOG_CRITICAL', 'CRITICAL.log')
                critical_logs_handler = handlers.TimedRotatingFileHandler(file,
                                                                          when=self.when,
                                                                          interval=self.rotating_interval,
                                                                          backupCount=self.back_up_count)
                critical_logs_handler.setLevel(logging.CRITICAL)
                critical_logs_handler.setFormatter(formatter)
                logger.addHandler(critical_logs_handler)

                # This will prevent duplication of logs.
                logger.propagate = False

            # ERROR Handler - will contain ONLY logs of ERROR type OR HIGHER (Includes, ERROR AND WARNINGS)
            if self.is_enable_log_level_error is True:

                # Creating folders for file retention.
                try:
                    folder = os.path.join(script_dir, 'LOG_ERROR')
                    # Path("./LOG_ERROR").mkdir()
                    Path(folder).mkdir()
                except FileExistsError:
                    pass

                file = os.path.join(script_dir, 'LOG_ERROR', 'ERROR.log')
                error_logs_handler = handlers.TimedRotatingFileHandler(file,
                                                                       when=self.when,
                                                                       interval=self.rotating_interval,
                                                                       backupCount=self.back_up_count)
                error_logs_handler.setLevel(logging.ERROR)
                error_logs_handler.setFormatter(formatter)
                logger.addHandler(error_logs_handler)

                # This will prevent duplication of logs.
                logger.propagate = False

            # WARNING Handler - will contain ONLY LOGS OF WARNING type OR HIGHER
            # (Includes, WARNING, ERROR AND CRITICAL TYPES)
            if self.is_enable_log_level_warning is True:
                # Creating folders for file retention.
                try:
                    folder = os.path.join(script_dir, 'LOG_WARNING')
                    # Path("./LOG_WARNING").mkdir()
                    Path(folder).mkdir()
                except FileExistsError:
                    pass
                file = os.path.join(script_dir, 'LOG_WARNING', 'WARNING.log')
                warning_logs_handler = handlers.TimedRotatingFileHandler(file,
                                                                         when=self.when,
                                                                         interval=self.rotating_interval,
                                                                         backupCount=self.back_up_count)
                warning_logs_handler.setLevel(logging.WARNING)
                warning_logs_handler.setFormatter(formatter)
                logger.addHandler(warning_logs_handler)

                # This will prevent duplication of logs.
                logger.propagate = False

            # INFO Handler - WILL CONTAIN ALL MESSAGES.
            if self.is_enable_log_level_info is True:
                try:
                    folder = os.path.join(script_dir, 'LOG_INFO')
                    # Path("./LOG_INFO").mkdir()
                    Path(folder).mkdir()
                except FileExistsError:
                    pass
                file = os.path.join(script_dir, 'LOG_INFO', 'INFO.log')
                info_log_handler = handlers.TimedRotatingFileHandler(file,
                                                                     when=self.when,
                                                                     interval=self.rotating_interval,
                                                                     backupCount=self.back_up_count)
                info_log_handler.setLevel(logging.INFO)
                info_log_handler.setFormatter(formatter)
                logger.addHandler(info_log_handler)
                # This will prevent duplication of logs.
                logger.propagate = False

            # INFO Handler - WILL CONTAIN ALL MESSAGES.
            if self.is_enable_log_level_debug is True:
                try:
                    folder = os.path.join(script_dir, 'LOG_DEBUG')
                    # Path("./LOG_DEBUG").mkdir()
                    Path(folder).mkdir()
                except FileExistsError:
                    pass
                file = os.path.join(script_dir, 'LOG_DEBUG', 'DEBUG.log')
                info_log_handler = handlers.TimedRotatingFileHandler(file,
                                                                     when=self.when,
                                                                     interval=self.rotating_interval,
                                                                     backupCount=self.back_up_count)
                info_log_handler.setLevel(logging.DEBUG)
                info_log_handler.setFormatter(formatter)
                logger.addHandler(info_log_handler)

                # This will prevent duplication of logs.
                logger.propagate = False

        return logger

