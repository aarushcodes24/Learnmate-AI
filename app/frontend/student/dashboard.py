
import streamlit as st
import pandas as pd
import plotly.express as px

from app.frontend.components.metrics import show_metric
from app.frontend.components.cards import show_course_card


def show_student_dashboard():

    st.title("Good to see you! 👋")
    st.write("Welcome to your personalised learning dashboard.")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric("Courses Enrolled", "3", "+1")

    with col2:
        show_metric("Topics Completed", "18", "+4")

    with col3:
        show_metric("Study Hours", "24 hrs", "+3 hrs")

    with col4:
        show_metric("Overall Progress", "53%", "+8%")

    st.write("")

    st.subheader("📚 My Learning Progress")

    courses = [
        ("Python Programming", 75, "12 Topics"),
        ("Mathematics", 55, "10 Topics"),
        ("Data Structures", 30, "15 Topics")
    ]

    course_columns = st.columns(3)

    for column, course in zip(course_columns, courses):
        name, progress, topics = course

        with column:
            show_course_card(name, progress, topics)

    st.write("")

    st.subheader("📈 Weekly Learning Activity")

    activity = pd.DataFrame({
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"],
        "Study Hours": [1.5, 2, 1, 2.5, 3, 2, 1.5]
    })

    chart = px.bar(
        activity,
        x="Day",
        y="Study Hours",
        title="Your study hours this week",
        text="Study Hours"
    )

    chart.update_layout(
        yaxis_title="Hours",
        xaxis_title="",
        showlegend=False
    )

    st.plotly_chart(chart, use_container_width=True)

    st.subheader("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 Ask AI Tutor", use_container_width=True):
            st.info("Select AI Tutor from the sidebar.")

    with col2:
        if st.button("📝 Practice Quiz", use_container_width=True):
            st.info("Select Practice Quiz from the sidebar.")

    with col3:
        if st.button("📖 Explore Syllabus", use_container_width=True):
            st.info("Select Syllabus Explorer from the sidebar.")

    st.caption("Dashboard currently displays sample data for development.")
