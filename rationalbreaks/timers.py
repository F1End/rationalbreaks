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

    def _save_cycle_work(self):
        self._saved_work += self._calculate_cycle_time()

    def rest_time(self):
        if self._status == "Working":
            return self._saved_rest + (self._calculate_cycle_time() / self._ratio)
        elif self._status == "Resting":
            return self._calculate_remaining_rest()

    def _calculate_remaining_rest(self):
        remaining_rest = self._saved_rest - self._calculate_cycle_time()
        return remaining_rest if remaining_rest >= timedelta(0) else timedelta(0)

    def _save_cycle_rest(self):
        self._saved_rest = self.rest_time()

    def work_and_rest_time(self):
        return self.work_time(), self.rest_time()
