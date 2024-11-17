"""
This module hold the actual timer and its associated methods/classes.
RatioNalTimer class is doing the primary interface,
where all non-hidden (not starting with _) methods
are the interfaces.
There is also a SimpleTime class that is returned by one of the methods.
Simplelclass is to allow easy display and storage of granual time variables.
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from copy import deepcopy


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

    def _slice_to_time_units(self) -> (int, int, int, int, int):
        secs_per_day, secs_per_hour, secs_per_minute = 86400, 3600, 60  # constants

        days = self.timedelta.days
        secs_after_days = self.timedelta.total_seconds() - days * secs_per_day
        hours, secs_after_hours = divmod(secs_after_days, secs_per_hour)
        minutes, seconds = divmod(secs_after_hours, secs_per_minute)
        full_seconds = int(seconds)
        centi_seconds = int((seconds - full_seconds) * 100)

        return days, int(hours), int(minutes), full_seconds, centi_seconds

    def __str__(self) -> str:
        if self.days == 1:
            return f"{self.days} day {self.hours}:" \
                   f"{self.minutes}:{self.full_seconds}:{self.centi_seconds}"
        if self.days > 1:
            return f"{self.days} days {self.hours}:" \
                   f"{self.minutes}:{self.full_seconds}:{self.centi_seconds}"
        if self.hours > 0:
            return f"{self.hours:02}:" \
                   f"{self.minutes:02}:{self.full_seconds:02}:{self.centi_seconds:02}"
        return f"{self.minutes:02}:{self.full_seconds:02}:{self.centi_seconds:02}"

    def to_string(self):
        return str(self)

    def to_timedelta(self):
        tdelta = deepcopy(self.timedelta)
        return tdelta


class RatioNalTimer:
    """Main class that measures time after start is triggered and calculates the "deserved" rest
    based on a specified ratio (defaults to 3 -> One third of the work time can be used as rest).
    Can be stopped and restarted for breaks, time passed and available rest can be polled.
    """
    def __init__(self, ratio: Optional[float] = None):
        self._ratio = float(ratio) if ratio is not None else float(3)
        self._status = "Not started"
        self._cycle_timestamps = []
        self._current_cycle_time = timedelta(0)
        self._saved_work = timedelta(0)
        self._saved_rest = timedelta(0)

    def start(self) -> None:
        self._cycle_timestamps.append(datetime.now())
        self._status = "Working"

    def rest(self) -> None:
        self._save_cycle_work()
        self._save_cycle_rest()
        self._cycle_timestamps.append(datetime.now())
        self._status = "Resting"

    def continue_work(self) -> None:
        self._save_cycle_rest()
        self.start()

    def get_ratio(self) -> float:
        return self._ratio

    def set_ratio(self, new_ratio: float = 3) -> None:
        converted_to_float = float(new_ratio)
        self._ratio = converted_to_float

    def _calculate_cycle_time(self) -> timedelta:
        time_passed = datetime.now() - self._cycle_timestamps[-1]
        return time_passed

    def status(self) -> str:
        return self._status

    def work_time(self) -> timedelta:
        if self._status == "Working":
            return self._saved_work + self._calculate_cycle_time()
        if self._status == "Resting":
            return self._saved_work
        # no cycle is running --> use saved only
        return self._saved_work

    def _save_cycle_work(self):
        self._saved_work += self._calculate_cycle_time()

    def rest_time(self) -> timedelta:
        if self._status == "Working":
            return self._saved_rest + (self._calculate_cycle_time() / self._ratio)
        if self._status == "Resting":
            return self._calculate_remaining_rest()
        # no cycle is running --> use saved only
        return self._saved_rest

    def _calculate_remaining_rest(self) -> timedelta:
        remaining_rest = self._saved_rest - self._calculate_cycle_time()
        return remaining_rest if remaining_rest >= timedelta(0) else timedelta(0)

    def _save_cycle_rest(self) -> None:
        self._saved_rest = self.rest_time()

    def work_and_rest_time(self, use_simpletime: bool = True) -> Union[timedelta, SimpleTime]:
        """
        :param use_simpletime: If True returns SimpleTime objects, else returns timedelta objects
        :return:
        """
        if use_simpletime:
            return SimpleTime(self.work_time()), SimpleTime(self.rest_time())
        return self.work_time(), self.rest_time()

    def reset(self) -> None:
        self._status = "Not started"
        self._cycle_timestamps = []
        self._current_cycle_time = timedelta(0)
        self._saved_work = timedelta(0)
        self._saved_rest = timedelta(0)

    def all_rest_consumed(self) -> bool:
        has_rest_started = len(self._cycle_timestamps)
        has_time_expired = self.rest_time() == timedelta(0)
        is_consumed = has_rest_started and has_time_expired
        return is_consumed
