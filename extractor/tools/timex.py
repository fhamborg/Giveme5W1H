from datetime import datetime

from dateutil.relativedelta import relativedelta


class Timex:
    """
    Simply represents a Timex object. Main reason for this class is that the datetime class (and other Python
    equivalents) do not allow to reflect a month or a day but only a single point in time.
    """
    _date_format_month = '%Y-%m'
    _date_format_week = '%Y-W%W' + '-%w'
    _date_format_day = '%Y-%m-%d'
    _date_format_time_nosecs = '%Y-%m-%dT%H:%M'

    # _log = logging.getLogger('GiveMe5W')

    def __init__(self, start_datetime, end_datetime):
        self._start_date = start_datetime
        self._end_date = end_datetime

    def __str__(self):
        return 'Timex(' + str(self._start_date) + ', ' + str(self._end_date) + ')'

    @staticmethod
    def _get_date_distance_in_seconds(date1, date2):
        return abs((date2 - date1).total_seconds())

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    def get_duration(self):
        return self._end_date - self._start_date

    def is_entailed_in(self, other_timex):
        return other_timex.get_start_date() <= self._start_date and self.get_end_date() <= other_timex._end_date

    def get_min_distance_in_seconds_to_datetime(self, other_datetime):
        return min(Timex._get_date_distance_in_seconds(self._start_date, other_datetime),
                   Timex._get_date_distance_in_seconds(self._end_date, other_datetime))

    def get_json(self):
        """
        return a serializable representation of this object.
        :return:
        """
        return {
            'start_date': self._start_date.isoformat(),
            'end_date': self._end_date.isoformat()
        }

    @staticmethod
    def from_timex_text(text):
        # month (2017-11)
        try:
            start_date = datetime.strptime(text, Timex._date_format_month)
            end_date = start_date + relativedelta(months=1) - relativedelta(seconds=1)
            return Timex(start_date, end_date)
        except ValueError as verr:
            pass

        # week (2017-W45)
        try:
            default_day = '-0'  # https://stackoverflow.com/a/17087427/1455800
            start_date = datetime.strptime(text + default_day, Timex._date_format_week)
            end_date = start_date + relativedelta(weeks=1) - relativedelta(seconds=1)
            return Timex(start_date, end_date)
        except ValueError as verr:
            pass

        # day (2017-11-01)
        try:
            start_date = datetime.strptime(text, Timex._date_format_day)
            end_date = start_date + relativedelta(days=1) - relativedelta(seconds=1)
            return Timex(start_date, end_date)
        except ValueError as verr:
            pass

        # datetime without seconds (2017-02-04T13:55)
        try:
            start_date = datetime.strptime(text, Timex._date_format_time_nosecs)
            end_date = start_date + relativedelta(minutes=1) - relativedelta(seconds=1)
            return Timex(start_date, end_date)
        except ValueError as verr:
            pass

        # Timex._log.error('could not parse "' + text + '" to Timex')
        # print('could not parse "' + text + '" to Timex')
        # we cannot parse the following things
        # could not parse "2017-SU" to Timex: This summer
        return None
