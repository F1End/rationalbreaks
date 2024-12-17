"""
This module is for storing classes and functions used by streamlit front end.

"""

from time import sleep
from os import path
from typing import Optional
from base64 import b64encode

import streamlit as st

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
        self.audio_base64 = self.encode_audio()

    def encode_audio(self):
        with open(self.soundfile, "rb") as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = b64encode(audio_bytes).decode()
            return audio_base64

    def trigger_audio(self):
        """
        Evaluate session_states and return value inserted into JS code.
        :return: lower case string imitating js boolean
        """
        play_alarm = st.session_state.alert["play_sound"] is True \
            and st.session_state.alert["muted"] is False \
            and st.session_state.rest_consumed is True
        formatted_to_js = str(play_alarm).lower()
        return formatted_to_js

    def load_player_html(self, refresh_frequency: int = 1000):
        st.components.v1.html(
            f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js">
            </script>
            <script>
            const sound = new Howl({{
                src: ['data:audio/wav;base64,{self.audio_base64}']
            }});
    
            // Monitor Streamlit for playback trigger
            const checkPlayback = () => {{
                const playAudio = {self.trigger_audio()};
                if (playAudio) {{
                    sound.play();
                }}
            }};
    
            // Poll the server for updates every "refresh_frequency" ms
            setInterval(checkPlayback, {refresh_frequency});
            </script>
            """,
            height=1)


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

    def stop(self):
        pass

    def reset(self):
        self.timer.reset()
        st.session_state["status"] = "Not started"
        st.session_state["alert"]["muted"] = True

    def mute_alarm(self):
        st.session_state["alert"]["muted"] = True
        st.rerun()

    def get_timer_ratio(self) -> float:
        return self.timer.get_ratio()

    def set_ratio(self, new_ratio: float):
        self.timer.set_ratio(new_ratio)


def check_rest_consumed(timer_instance: RatioNalTimerStreamlit) -> bool:
    if timer_instance.all_rest_consumed() and st.session_state["status"] == "Resting":
        st.session_state["rest_consumed"] = True
        return True
    return False


def display_timers(timer_instance: RatioNalTimerStreamlit,
                   work_time_display,
                   rest_time_display,
                   update_per_sec: int = 10) -> None:
    loop = True
    while loop:
        work, rest = timer_instance.work_and_rest_time()
        work_time_display.metric("Worked time", str(work))
        rest_time_display.metric("Available rest", str(rest))

        # to trigger alarm
        rest_consumed = check_rest_consumed(timer_instance)

        alarm_active = not st.session_state.alert["muted"] and st.session_state.alert["play_sound"]

        # interrupting loop if we are resting and alarm needs to be played (outside loop)
        if rest_consumed and alarm_active:
            loop = False
            st.rerun()

        sleep(1 / update_per_sec)


"""Non-python code injection elements below"""

format_buttons_html = """
    <style>
    div.stButton > button {
        height: 30px;
        width: 220px;
        font-size: 25px
    }
    </style>
    """