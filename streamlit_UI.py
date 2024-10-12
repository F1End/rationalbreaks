import streamlit as st
from time import sleep

from rationalbreaks.timers import RatioNalTimer


@st.cache_resource
class RatioNalTimerStreamlit(RatioNalTimer):
    def __init__(self):
        super().__init__()


class StatusControl:

    def __init__(self, timer_instance: RatioNalTimer):
        self.timer = timer_instance

    def start(self):
        self.timer.start()
        st.session_state["status"] = "Working"

    def rest(self):
        self.timer.rest()
        st.session_state["status"] = "Resting"

    def continue_work(self):
        self.timer.continue_work()
        st.session_state["status"] = "Working"

    def stop(self):
        pass

    def reset(self):
        st.session_state["status"] = "Not started"
        timer.reset()


def display_timers(timer_instance: RatioNalTimerStreamlit, update_per_sec: int = 10):
    work_time_display = st.empty()
    rest_time_display = st.empty()
    while True:
        work, rest = timer_instance.work_and_rest_time()
        work_time_display.metric("Worked time", str(work))
        rest_time_display.metric("Available rest", str(rest))
        sleep(1 / update_per_sec)


timer = RatioNalTimerStreamlit()
control = StatusControl(timer)

if st.session_state.get("status", None) is None:
    control.reset()

if st.session_state.status == "Not started":
    if st.button("Start"):
        control.start()
        st.rerun()

elif st.session_state.status == "Working":
    if st.button("Rest"):
        control.rest()
        st.rerun()

elif st.session_state.status == "Resting":
    if st.button("Continue"):
        control.continue_work()
        st.rerun()

display_timers(timer_instance=timer)
