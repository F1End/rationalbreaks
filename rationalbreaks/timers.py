from datetime import datetime, timedelta
from typing import Optional


class RatioNalTimer:
    def __init__(self, ratio: Optional[int] = None):
        self._ratio = ratio if ratio is not None else 3
        self._status = "Not started"
        self._work_start_times = []
        self._rest_start_times = []
        self._total_worked = timedelta(0)
        self._available_rest = timedelta(0)
        self._consumed_rest = timedelta(0)
        self._overrest = timedelta(0)

    def start(self):
        self._status = "Working"
        self._work_start_times.append(datetime.now())

    def rest(self):
        self._status = "Resting"
        self._rest_start_times.append(datetime.now())

    def continue_work(self):
        self.start()

    def stop(self):
        pass

    def status(self):
        return self._status

    def work_time(self):
        if self._status == "Working":
            self._total_worked += datetime.now() - self._work_start_times[-1]
        return self._total_worked

    def rest_time(self):
        if self._status == "Resting":
            self._update_rest_consumed()
        self._available_rest = self._total_worked / self._ratio - self._consumed_rest
        if self._available_rest < timedelta(0):
            self._available_rest = timedelta(0)
        return self._available_rest

    def _update_rest_consumed(self):
        if self._consumed_rest < self._available_rest:
            self._consumed_rest += (datetime.now() - self._rest_start_times[0])
        else:
            self._overrest += self._consumed_rest
            self._consumed_rest = timedelta(0)
