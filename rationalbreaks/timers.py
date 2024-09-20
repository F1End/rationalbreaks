from datetime import datetime, timedelta
from typing import Optional


class RatioNalTimer:
    def __init__(self, ratio: Optional[int] = None):
        self._ratio = ratio if ratio is not None else 3
        self._status = "Not started"
        self._cycle_timestamps = []
        self._current_cycle_time = timedelta(0)
        self._current_worked = timedelta(0)
        self._carried_worked = timedelta(0)
        self._current_rest = timedelta(0)
        self._carried_rest = timedelta(0)
        self._overrest = timedelta(0)

    def start(self):
        self._status = "Working"
        self._cycle_timestamps.append(datetime.now())

    def rest(self):
        self._status = "Resting"
        self._carry_worked()
        self._carry_rest()
        self._cycle_timestamps.append(datetime.now())

    def continue_work(self):
        # self._update_timers()
        self._carry_rest()
        self.start()

    def stop(self):
        raise NotImplemented

    def status(self):
        return self._status

    # def times(self):
    #     self._update_timers()
    #     return self._total_worked, self._available_rest

    def work_time(self):
        self._update_worked()
        return self._carried_worked + self._current_worked

    def _update_worked(self):
        if self._status == "Working":
            self._current_worked = datetime.now() - self._cycle_timestamps[-1]
        elif self._status == "Resting":
            self._current_worked = timedelta(0)

    def _carry_worked(self):
        self._carried_worked += self._current_worked

    def rest_time(self):
        self._update_rest()
        if self._status == "Working":
            available_rest = self._current_rest + self._carried_rest
        elif self._status == "Resting":
            available_rest = self._carried_rest - self._current_rest
        print(f"Available rest after update: {available_rest}")
        if available_rest > timedelta(0):
            return available_rest
        else:
            return timedelta(0)

    def _update_rest(self):
        if self._status == "Working":
            self._current_rest = self._current_worked / self._ratio
        elif self._status == "Resting":
            self._current_rest = datetime.now() - self._cycle_timestamps[-1]

    def _carry_rest(self):
        if self._carried_rest - self._current_rest > timedelta(0):
            self._carried_rest += self._current_rest
        else:
            self._carried_rest = timedelta(0)

    # def _update_rest(self):
    #     if self._status == "Working":
    #         self._current_rest = self._current_worked / self._ratio
    #         self._available_rest += self._current_rest
    #     elif self._status == "Resting":
    #         self._current_rest = datetime.now() - self._cycle_timestamps[-1]
    #         self._available_rest -= self._current_rest
    #         if self._available_rest < timedelta(0):
    #             self._available_rest = timedelta(0)
    #             self._overrest += self._current_rest
                
    # def _carry_rest(self):
    #     self._carried_rest +=

    # def _update_timers(self):
    #     self._update_worked()
    #     self._update_rest()
