import streamlit as st


def show_course_card(name, progress, topics):
    with st.container(border=True):
        st.markdown(f"**{name}**")
        st.progress(progress / 100)
        st.write(f"**{progress}%** completed")
        st.caption(topics)