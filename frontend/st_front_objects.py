from time import sleep
from datetime import timedelta, datetime
import threading
from os import path
from typing import Optional

import streamlit as st
from playsound3 import playsound

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
        # st.session_state["rest_alert"]["rest_state"] = "Muted"

    def rest(self):
        self.timer.rest()
        st.session_state["status"] = "Resting"
        st.session_state["rest_consumed"] = False
        st.session_state["alert"]["cycle_timestamp"] = None
        st.session_state["alert"]["played"] = False

    def continue_work(self):
        self.timer.continue_work()
        st.session_state["status"] = "Working"
        # st.session_state["rest_alert"]["rest_state"] = "Muted"

    def stop(self):
        pass

    def reset(self):
        self.timer.reset()
        st.session_state["status"] = "Not started"
        # st.session_state["rest_alert"]["rest_state"] = "Muted"


def check_rest_consumed(timer_instance: RatioNalTimerStreamlit):
    if timer_instance.all_rest_consumed() and st.session_state["status"] == "Resting":
        st.session_state["rest_consumed"] = True
        st.rerun()

def display_timers(timer_instance: RatioNalTimerStreamlit, update_per_sec: int = 10):
    work_time_display = st.empty()
    rest_time_display = st.empty()
    while True:
        work, rest = timer_instance.work_and_rest_time()
        work_time_display.metric("Worked time", str(work))
        rest_time_display.metric("Available rest", str(rest))

        check_rest_consumed(timer_instance)  # to trigger alarm

        sleep(1 / update_per_sec)

def alarm():
    if st.session_state["alert"]["play_sound"]:
        play_alarm_sound()

def play_alarm_sound(sound_file: Optional[path] = None):
    if sound_file is None:
        sound_file = path.join("resources", "mixkit-interface-hint-notification-911.wav")
    playsound(sound_file, block=True)

def alert():
    # creating timestamp for alert start
    if st.session_state["alert"]["cycle_timestamp"] is None:
        st.session_state["alert"]["cycle_timestamp"] = datetime.now()

    time_passed = datetime.now() - st.session_state["alert"]["cycle_timestamp"]
    play_limit = timedelta(seconds=st.session_state["alert"]["length"])

    if time_passed < play_limit and st.session_state["alert"]["played"] is False:
        alarm()
        print("Trigg")
        st.rerun()

    elif time_passed >= play_limit and st.session_state["alert"]["played"] is False:
        st.session_state["alert"]["played"] = True

# def alert(play_sound: True):
#     triggered = True if st.session_state.rest_alert == "Triggered" else False
#     if triggered:
#         print("Triggered")
#     time_since_trigger = time.time.now() - st.session_state["rest_alert"]["timestamp"]
#     print(f"Time since tr:", time_since_trigger)
#     completed = True if time_since_trigger.seconds() > 0 else False
#     if completed:
#         print("Completed")
#     if triggered and not completed:
#         print("triggered and not completed")
#         sound_path = path.join("resources", "mixkit-interface-hint-notification-911.wav")
#         playsound(sound_path, block=False)
#         st.session_state.rest_alert["rest_state"] = "Muted"
#         st.rerun()
