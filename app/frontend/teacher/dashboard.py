import streamlit as st
import pandas as pd


def show_teacher_dashboard():

    st.subheader("Student Overview")

    students = pd.DataFrame({
        "Student": ["Student 1", "Student 2", "Student 3"],
        "Course Progress": [85, 65, 45]
    })

    st.dataframe(
        students,
        use_container_width=True,
        hide_index=True
    )

    st.caption("Illustrative sample data.")