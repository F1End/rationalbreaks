"""
File to run for front-end web-application based on streamlit.
Imports elements from st_front_objects
Control flow overlaps st_front_objects module and this file
"""
from time import sleep

import streamlit as st

from frontend import st_front_objects

st.markdown(st_front_objects.FORMAT_BUTTONS_HTML, unsafe_allow_html=True)


timer = st_front_objects.RatioNalTimerStreamlit()  # cached
control = st_front_objects.StatusControl(timer)
alarm = st_front_objects.Alarm()  # cached

sessions = {"status": "Not started", "rest_consumed": False,
            "alert": {"play_sound": True, "muted": False},
            "settings_clicked": False,
            "reset_clicked": False}
for state, value in sessions.items():
    if state not in st.session_state.keys():
        st.session_state[state] = value

# Initiating player element here (JS)
# This pushes down the other buttons a bit, should be on top or bottom
alarm.load_player_html()

# centering all elements
left, center, right = st.columns(3)

with center:
    # Settings section
    settings_container = st.container(border=False)
    settings_widget1, settings_widget2, settings_widget3, settings_widget4 = \
        (settings_container.empty() for i in range(4))

    if st.session_state.settings_clicked is False:
        if settings_widget1.button("Settings"):
            st.session_state.settings_clicked = True
            st.rerun()
    else:
        if settings_widget1.button("Hide settings"):
            st.session_state.settings_clicked = False
            st.rerun()

        current_ratio = control.get_timer_ratio()
        current_value = st.session_state.alert["play_sound"]
        new_ratio = settings_widget2.number_input("Work:Rest ratio",
                                                  min_value=0.1,
                                                  max_value=100.00,
                                                  value=current_ratio)

        alarm_sound = settings_widget3.toggle("Alarm if rest consumed", value=current_value)

        if settings_widget4.button("Save settings"):
            control.set_ratio(new_ratio)
            st.session_state["alert"]["play_sound"] = alarm_sound
            st.rerun()

    # Status section
    status_container = st.container()
    status_widget1 = status_container.empty()

    if st.session_state.status == "Not started":
        if status_widget1.button("Start"):
            control.start()
            st.rerun()

    elif st.session_state.status == "Working":
        if status_widget1.button("Rest"):
            control.rest()
            st.rerun()

    elif st.session_state.status == "Resting":
        if status_widget1.button("Continue"):
            control.continue_work()
            st.rerun()

    # Reset section
    reset_container = st.container(border=False)
    reset_widget1, reset_widget2, reset_widget3 = (reset_container.empty() for i in range(3))

    if not st.session_state["reset_clicked"]:
        if reset_widget1.button("Reset timers"):
            st.session_state["reset_clicked"] = True
            st.rerun()

    else:
        reset_widget1.write("Are you sure you want to reset?")
        if reset_widget2.button("Confirm"):
            control.reset()
            st.session_state["reset_clicked"] = False
            st.rerun()
        if reset_widget3.button("Cancel"):
            st.session_state["reset_clicked"] = False
            st.rerun()

    # Alarm section
    # Alarm: mute button
    alarm_container = st.container()
    alarm_widget1 = st.empty()
    if st.session_state["rest_consumed"] and not st.session_state.alert["muted"]:
        if alarm_widget1.button("Mute alarm"):
            control.mute_alarm()
            st.rerun()

    # Alarm: We are looping here while alarm is playing
    while st.session_state["rest_consumed"] and not st.session_state.alert["muted"]:
        sleep(1)
        st.rerun()

    # Display
    work_time_display = st.empty()
    rest_time_display = st.empty()
    st_front_objects.display_timers(timer_instance=timer,
                                    work_time_display=work_time_display,
                                    rest_time_display=rest_time_display
                                    )
