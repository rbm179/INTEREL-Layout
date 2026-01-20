# Python module.
import datetime
import logging_package as logstream
logger = logstream.GetLogger().get_logger()


class ConvertDateToMilliseconds:

    def __init__(self,
                 raw_date):
        self.raw_date = raw_date

    # Parsing Raw time-stamp from config.
    @staticmethod
    def parse_raw_date(raw_date):
        time_stamp = str(raw_date)
        time_stamp_split = time_stamp.split()
        date_parser = str(time_stamp_split[0])
        time_parser = str(time_stamp_split[1])
        year = int(str(date_parser).split("-")[0])
        month = int(str(date_parser).split("-")[1])
        day = int(str(date_parser).split("-")[2])
        hour = int(str(time_parser).split(":")[0])
        minute = int(str(time_parser).split(":")[1])
        second = int(str(str(time_parser).split(":")[2]).split('.')[0])
        try:
            millisecond = int(str(str(time_parser).split(":")[2]).split('.')[1])
            return year, month, day, hour, minute, second, millisecond

        except IndexError:
            millisecond = 0
            # print(millisecond)
            return year, month, day, hour, minute, second, millisecond

    # Convert parsed date into UTC time / date.
    # Irrespective of whether its local time OR GMT / UTC, unix ticks remains same.
    def convert_parsed_date_into_utc(self):
        year, month, day, hour, minute, second, millisecond = self.parse_raw_date(self.raw_date)
        date_time_object = datetime.datetime(year, month, day, hour, minute, second, millisecond)
        utc_date_time_object = date_time_object.astimezone(datetime.timezone.utc)
        utc_date_time_string = utc_date_time_object.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        logger.info(f"LOCAL TIME : {self.raw_date}")
        logger.info(f"UTC TIME : {utc_date_time_string}")

    # Convert UTC date into milliseconds.
    def convert_date_ticks(self):
        # local_date_time_string = self.convert_parsed_date_into_local_time()
        year, month, day, hour, minute, second, millisecond = self.parse_raw_date(self.raw_date)
        date_time = datetime.datetime(year, month, day, hour, minute, second, millisecond)
        time_in_secs = int(datetime.datetime.timestamp(date_time))
        time_in_ms = time_in_secs * 1000
        return time_in_secs, time_in_ms




