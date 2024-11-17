"""
This module is for storing classes and functions used by streamlit front end.

"""

from time import sleep
from os import path
from typing import Optional

import streamlit as st
import simpleaudio as sa

from rationalbreaks.timers import RatioNalTimer


@st.cache_resource
class RatioNalTimerStreamlit(RatioNalTimer):
    """Caching timer instance for streamlit"""
    def __init__(self):
        super().__init__()


@st.cache_resource
class Alarm:
    """Cached alarm that provides notification based on timer preferences."""
    def __init__(self, soundfile: Optional[path] = None):
        default_sound = path.join("resources", "ring_1.wav")
        self.soundfile = soundfile if soundfile else default_sound
        self.player = self.create_player()
        self.play_object = None

    def create_player(self):
        return sa.WaveObject.from_wave_file(self.soundfile)

    def play(self):
        if self.play_object is None:
            self.play_object = self.player.play()
        if not self.play_object.is_playing():
            self.play_object = self.player.play()
        sleep(0.1)

    def stop(self):
        self.play_object.stop()

    def toogle(self):
        if self.play_object.is_playing():
            self.play_object.stop()
        else:
            self.player.play()


class StatusControl:
    """Class that changes the status of encapsulated cached timer
    based on user interaction.
    Technically it is compatible with RatioNalTimer, but in most
    streamlit application it should be a cached version, as
    defined above via class RatioNalTimerStreamlit

    """
    def __init__(self, timer_instance: RatioNalTimer):
        self.timer = timer_instance

    def start(self):
        self.timer.start()
        st.session_state["status"] = "Working"

    def rest(self):
        self.timer.rest()
        st.session_state["status"] = "Resting"
        st.session_state["rest_consumed"] = False
        if st.session_state["alert"]["play_sound"]:
            st.session_state["alert"]["muted"] = False

    def continue_work(self):
        self.timer.continue_work()
        st.session_state["status"] = "Working"
        st.session_state["alert"]["muted"] = True
        st.session_state["refresh"] = True

    def stop(self):
        pass

    def reset(self):
        self.timer.reset()
        st.session_state["status"] = "Not started"
        st.session_state["alert"]["muted"] = True
        # st.session_state["refresh"] = True

    def mute_alarm(self):
        st.session_state["alert"]["muted"] = True
        st.session_state["refresh"] = True
        st.rerun()


def refresh_elements() -> None:
    if st.session_state["refresh"]:
        st.session_state["refresh"] = False
        st.rerun()
        sleep(0.1)


def check_rest_consumed(timer_instance: RatioNalTimerStreamlit) -> bool:
    if timer_instance.all_rest_consumed() and st.session_state["status"] == "Resting":
        st.session_state["rest_consumed"] = True
        st.session_state["refresh"] = True
        return True
    return False


def display_timers(timer_instance: RatioNalTimerStreamlit,
                   work_time_display,
                   rest_time_display,
                   update_per_sec: int = 10) -> None:
    # work_time_display = st.empty()
    # rest_time_display = st.empty()
    while True:
        work, rest = timer_instance.work_and_rest_time()
        work_time_display.metric("Worked time", str(work))
        rest_time_display.metric("Available rest", str(rest))

        # to trigger alarm
        rest_consumed = check_rest_consumed(timer_instance)

        # no need to loop here if there is no rest to update
        if rest_consumed:
            break

        # clearing display to avoid shadowing (st rerun creates new objects)
        if st.session_state["refresh"]:
            print("Should break here")
            work_time_display.empty()
            rest_time_display.empty()
            break

        sleep(1 / update_per_sec)
