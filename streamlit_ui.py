"""
File to run for front-end web-application based on streamlit.
Imports elements from st_front_objects
Control flow overlaps st_front_objects module and this file
"""
import datetime

import streamlit as st

from frontend import st_front_objects

# Button size styling
st.markdown("""
    <style>
    div.stButton > button {
        height: 30px;
        width: 220px;
        font-size: 25px
    }
    </style>
    """, unsafe_allow_html=True)

timer = st_front_objects.RatioNalTimerStreamlit()
control = st_front_objects.StatusControl(timer)
alarm = st_front_objects.Alarm()

sessions = {"status": "Not started", "rest_consumed": False,
            "alert": {"play_sound": True, "muted": False},
            "settings_clicked": False,
            "refresh": False,
            "reset_clicked": False}
for state, value in sessions.items():
    if state not in st.session_state.keys():
        st.session_state[state] = value

print(datetime.datetime.now())
print(st.session_state)
# centering all elements
left, center, right = st.columns(3)

with center:
    if st.session_state.settings_clicked is False:
        if st.button("Settings"):
            st.session_state.settings_clicked = True
            st.session_state["refresh"] = True
            st.rerun()

    if st.session_state.settings_clicked is True:
        if st.button("Hide settings"):
            st.session_state.settings_clicked = False
            st.session_state["refresh"] = True
            st.rerun()

        with center:
            current_ratio = control.get_timer_ratio()
            new_ratio = st.number_input("Work:Rest ratio",
                                        min_value=0.1,
                                        max_value=100.00,
                                        value=current_ratio)

        with center:
            current_value = st.session_state["alert"]["play_sound"]
            alarm_sound = st.toggle("Alarm if rest consumed")

        with center:
            if st.button("Update settings"):
                control.set_ratio(new_ratio)
                st.session_state["alert"]["play_sound"] = alarm_sound
                st.session_state["refresh"] = True
                st.rerun()

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

    if not st.session_state["reset_clicked"]:
        if st.button("Reset timers"):
            st.session_state["reset_clicked"] = True
            st.rerun()
    else:
        st.write("Are you sure you want to reset?")
        if st.button("Confirm"):
            control.reset()
            st.session_state["reset_clicked"] = False
            st.session_state["refresh"] = True

        if st.button("Cancel"):
            st.session_state["reset_clicked"] = False
            print("Does it pass?")
            st.session_state["refresh"] = True
            print("Sessoin here:")
            print(st.session_state)

    if st.session_state["rest_consumed"] and not st.session_state["alert"]["muted"]:
        alarm.play()

    mute_button = st.empty()
    if st.session_state["rest_consumed"] and not st.session_state["alert"]["muted"]:
        if mute_button.button("Mute alarm"):
            control.mute_alarm()
        st.rerun()
    else:
        mute_button.empty()

    work_time_display = st.empty()
    rest_time_display = st.empty()
    st_front_objects.display_timers(timer_instance=timer,
                                    work_time_display=work_time_display,
                                    rest_time_display=rest_time_display
                                    )

    st_front_objects.refresh_elements()
