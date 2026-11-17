import streamlit as st


def show_metric(label, value, delta=None):
    st.metric(
        label=label,
        value=value,
        delta=delta
    )