# Python modules.
import pandas as pd
import logging_package as logstream
logger = logstream.GetLogger().get_logger()


class CalculateTimeDiffDataFrame:
    def __init__(self, df=None,
                 column_name=None,
                 is_enable_csv_output=None,
                 csv_file_path=None,
                 is_running_sum=None):
        self.df = df
        self.column_name = column_name
        self.is_enable_csv_output = is_enable_csv_output
        self.csv_file_path = csv_file_path
        self.is_running_sum = is_running_sum

    def calculate_time_diff_data_frame(self):

        # Converting TIME_STAMP column into date-time column in data-frame.
        # logger.debug("Converting TIME_STAMP column into date-time column in data-frame")
        self.df[self.column_name] = pd.to_datetime(self.df[self.column_name])

        # Data frame needs to be sorted in ascending to compute time-differences
        # between consecutive rows correctly.
        # logger.debug(f"Converting {self.column_name} column into date-time column in data-frame")
        self.df = self.df.sort_values(self.column_name, ascending=True)

        # Compute time-difference between consecutive rows in seconds
        # logger.debug("Compute time-difference between consecutive rows in seconds")
        self.df['time_diff_in_secs'] = self.df[self.column_name].diff().dt.total_seconds()
        self.df['cumulative_time_diff_in_secs'] = self.df['time_diff_in_secs'].cumsum()

        # Compute time-difference between consecutive rows in minutes
        # logger.debug("Compute time-difference between consecutive rows in minutes")
        self.df['time_diff_in_minutes'] = self.df[self.column_name].diff().dt.total_seconds() / 60
        self.df['cumulative_time_diff_in_minutes'] = self.df['time_diff_in_minutes'].cumsum()

        # Compute time-difference between consecutive rows in hours
        # logger.debug("Compute time-difference between consecutive rows in hours")
        self.df['time_diff_in_hours'] = self.df[self.column_name].diff().dt.total_seconds() / (60 * 60)
        self.df['cumulative_time_diff_in_hours'] = self.df['time_diff_in_hours'].cumsum()

        # Compute time-difference between consecutive rows in days
        # logger.debug("Compute time-difference between consecutive rows in days.")
        self.df['time_diff_in_days'] = self.df[self.column_name].diff().dt.total_seconds() / (24 * 60 * 60)
        self.df['cumulative_time_diff_in_days'] = self.df['time_diff_in_days'].cumsum()

        # Sum of differences.
        if self.is_running_sum is False:

            # Read from data-frame.
            time_diff_collection = []

            # Compute total time difference in secs, mins, hrs and days.
            total_time_diff_in_secs = round(self.df['time_diff_in_secs'].sum(), 4)
            total_time_diff_in_minutes = round(self.df['time_diff_in_minutes'].sum(), 4)
            total_time_diff_in_hours = round(self.df['time_diff_in_hours'].sum(), 4)
            total_time_diff_in_days = round(self.df['time_diff_in_days'].sum(), 4)

            # Logic to decide if output of CSV file needs to be writen into CSV file OR NOT.
            if self.is_enable_csv_output is True:
                # logger.debug(f"Contents will be written into CSV file path : {self.csv_file_path}")
                self.df.to_csv(self.csv_file_path)

            elif self.is_enable_csv_output is True:
                logger.debug(f"Contents will NOT be written into CSV file path : {self.csv_file_path}")

            else:
                pass
            # Adding time differences into collection.
            time_diff_list = [total_time_diff_in_secs, total_time_diff_in_minutes,
                              total_time_diff_in_hours, total_time_diff_in_days]
            for time_diff in time_diff_list:
                time_diff_collection.append(time_diff)

            return time_diff_collection, self.df

        # Cumulative / running sum of differences.
        elif self.is_running_sum is True:
            # Read from data-frame.
            running_sum_collection = []

            # Compute total time difference / cumulative sum in secs, mins, hrs and days.
            running_sum_diff_in_secs = round(self.df['cumulative_time_diff_in_secs'].iloc[-1], 4)
            running_sum_diff_in_minutes = round(self.df['cumulative_time_diff_in_minutes'].iloc[-1], 4)
            running_sum_diff_in_hours = round(self.df['cumulative_time_diff_in_hours'].iloc[-1], 4)
            running_sum_diff_in_days = round(self.df['cumulative_time_diff_in_days'].iloc[-1], 4)

            # Logic to decide if output of CSV file needs to be writen into CSV file OR NOT.
            if self.is_enable_csv_output is True:
                logger.debug(f"Contents will be written into CSV file path : {self.csv_file_path}")
                self.df.to_csv(self.csv_file_path)

            elif self.is_enable_csv_output is True:
                logger.debug(f"Contents will NOT be written into CSV file path : {self.csv_file_path}")

            else:
                pass
            # Adding time differences into collection.
            running_sum_list = [running_sum_diff_in_secs, running_sum_diff_in_minutes,
                                running_sum_diff_in_hours, running_sum_diff_in_days]
            for running_sum in running_sum_list:
                running_sum_collection.append(running_sum)
            return running_sum_collection, self.df

        else:
            pass

