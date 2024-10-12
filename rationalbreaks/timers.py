from datetime import datetime, timedelta
from typing import Optional


class RatioNalTimer:
    def __init__(self, ratio: Optional[float] = None):
        self._ratio = float(ratio) if ratio is not None else float(3)
        self._status = "Not started"
        self._cycle_timestamps = []
        self._current_cycle_time = timedelta(0)
        self._saved_work = timedelta(0)
        self._saved_rest = timedelta(0)

    def start(self):
        self._cycle_timestamps.append(datetime.now())
        self._status = "Working"

    def rest(self):
        self._save_cycle_work()
        self._save_cycle_rest()
        self._cycle_timestamps.append(datetime.now())
        self._status = "Resting"

    def continue_work(self):
        self._save_cycle_rest()
        self.start()

    def get_ratio(self):
        return self._ratio

    def set_ratio(self, new_ratio: float = 3):
        converted_to_float = float(new_ratio)
        self._ratio = converted_to_float
        
    def _calculate_cycle_time(self):
        time_passed = datetime.now() - self._cycle_timestamps[-1]
        return time_passed

    def status(self):
        return self._status

    def work_time(self):
        if self._status == "Working":
            return self._saved_work + self._calculate_cycle_time()
        elif self._status == "Resting":
            return self._saved_work
        else:  # no cycle is running --> use saved only
            return self._saved_work

    def _save_cycle_work(self):
        self._saved_work += self._calculate_cycle_time()

    def rest_time(self):
        if self._status == "Working":
            return self._saved_rest + (self._calculate_cycle_time() / self._ratio)
        elif self._status == "Resting":
            return self._calculate_remaining_rest()
        else:  # no cycle is running --> use saved only
            return self._saved_rest

    def _calculate_remaining_rest(self):
        remaining_rest = self._saved_rest - self._calculate_cycle_time()
        return remaining_rest if remaining_rest >= timedelta(0) else timedelta(0)

    def _save_cycle_rest(self):
        self._saved_rest = self.rest_time()

    def work_and_rest_time(self, use_simpletime: bool = True):
        """
        :param use_simpletime: If True will return SimpleTime object, if False, will return timedelta object
        :return:
        """
        if use_simpletime:
            return SimpleTime(self.work_time()), SimpleTime(self.rest_time())
        else:
            return self.work_time(), self.rest_time()

    def reset(self):
        self.__init__()


class SimpleTime:
    """This class exists to convert timedelta to easily displayable units.
    Assumes that dimedelta is positive.
    """
    def __init__(self, time: timedelta):
        self.timedelta = time
        days, hours, minutes, full_seconds, centi_seconds = self._slice_to_time_units()
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = full_seconds + centi_seconds / 100
        self.full_seconds = full_seconds
        self.centi_seconds = centi_seconds

    def _slice_to_time_units(self):
        secs_per_day = 86400
        secs_per_hour = 3600
        secs_per_minute = 60
        days = self.timedelta.days
        secs_after_days = self.timedelta.total_seconds() - days * secs_per_day
        hours, secs_after_hours = divmod(secs_after_days, secs_per_hour)
        minutes, seconds = divmod(secs_after_hours, secs_per_minute)
        full_seconds = int(seconds)
        centi_seconds = int((seconds - full_seconds) * 100)

        return days, int(hours), int(minutes), full_seconds, centi_seconds

    def __str__(self):
        if self.days == 1:
            return f"{self.days} day {self.hours}:{self.minutes}:{self.full_seconds}:{self.centi_seconds}"
        elif self.days > 1:
            return f"{self.days} days {self.hours}:{self.minutes}:{self.full_seconds}:{self.centi_seconds}"
        elif self.hours > 0:
            return f"{self.hours:02}:{self.minutes:02}:{self.full_seconds:02}:{self.centi_seconds:02}"
        else:
            return f"{self.minutes:02}:{self.full_seconds:02}:{self.centi_seconds:02}"
