import streamlit as st
from time import sleep

from rationalbreaks.timers import RatioNalTimer

# create shared object for ui frontend, ui backend and timer

# class for state update and timer update paralelization

class StatusControl:

    def __init__(self, timer_instance: RatioNalTimer, sessions:list):
        self.timer = timer_instance
        st.session_state["status"] = "Not started"

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
        pass

# create display frontend
# header, etc.
def display_timers(timer_instance: RatioNalTimer):
# function for timer update (loop)
# vars: timer session
# pols timer work and rest times
    work_display = st.empty()
    rest_display = st.empty()
    display_active = True
    while display_active:
        work_time, rest_time = timer_instance.work_and_rest_time()
        work_display.metric("Worked time", f"{work_time}")
        rest_display.metric("Rest time", f"{rest_time}")
        sleep(0.01)

# displays these in a reasonably large format
# status display via ss?
# loops indefinately (maybe interrupting brakes? if cannot work other way)

# function for displaying initial not started state
def display_start_button(control_instance: StatusControl):
    if st.button("Start"):
        control_instance.start()

# button for settings and starting, each changing state and timer via one func

# function for displaying settings state window conditions
def display_settings(timer_instance: RatioNalTimer):
    column_left, column_right = st.columns(2)
    with column_left:
        current_value = timer_instance.get_ratio()
        new_ratio = st.number_input("Ratio", min_value=0.1, step=0.1, value=current_value)
    # filed for ratio entry, apply button, reset question pop with appropriate calls to timer
    with column_right:
        if st.button("Update ratio"):
            timer_instance.set_ratio(new_ratio)

# functing for displaying work state
def display_rest_button(control_instance: StatusControl):
    if st.button("Rest"):
        control_instance.rest()

# buttons: rest (biggest), settings, reset

# function for displaying rest state
def display_continue_button(control_instance: StatusControl):
    if st.button("Work"):
        control_instance.continue_work()
# buttons: rest (biggest), settings, reset

# function for reset
def display_reset_button(control_instance: StatusControl):
    if st.button("Reset"):
        control_instance.reset()
# vars: timer session
# replaces session with a new, empty one

# main starts here

# create session states
sessions = ["Not started", "Working", "Resting", "Completed"]
timer = RatioNalTimer()
control = StatusControl(timer_instance=timer, sessions=sessions)

if st.session_state["status"] == "Not started":
    display_start_button(control)
    # display_settings(timer)

if st.session_state["status"] == "Working":
    display_rest_button(control)
    # display_settings(timer)
    display_reset_button(control)

if st.session_state["status"] == "Resting":
    display_continue_button(control)
    # display_settings(timer)
    display_reset_button(control)

display_timers(timer)
# actual calling of functions dependent on session_state with display loop at the end