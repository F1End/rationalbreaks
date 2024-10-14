import streamlit as st

from frontend import st_front_objects

# Button size styling
st.markdown("""
    <style>
    div.stButton > button {
        height: 30px;
        width: 150px;
        fint-size: 16px
    }
    </style>
    """, unsafe_allow_html=True)


timer = st_front_objects.RatioNalTimerStreamlit()
control = st_front_objects.StatusControl(timer)

# centering all elements
left, center, right = st.columns(3)

with center:
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

    if st.button("Reset timers"):
        control.reset()
        st.rerun()

    st_front_objects.display_timers(timer_instance=timer)
