
import streamlit as st
import pandas as pd
import plotly.express as px


def run_app():

    st.set_page_config(
        page_title="AI Teaching Assistant",
        page_icon="🎓",
        layout="wide"
    )


    st.markdown("""
    <style>

    /* Main application background */
    .stApp {
        background-color: #F5F7FB;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #172554 !important;
        font-weight: 700 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5EAF2;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5EAF2;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    /* Content containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 14px;
        border-color: #E5EAF2;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 9px;
        padding: 9px 18px;
        font-weight: 600;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
        border: none;
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #2563EB;
    }

    /* Dividers */
    hr {
        border-color: #E5EAF2;
    }

    </style>
    """, unsafe_allow_html=True)


    # ---------- WELCOME SCREEN ----------

    if "user_role" not in st.session_state:
        st.session_state.user_role = None

    if st.session_state.user_role is None:

        st.markdown(
            """
            <div style="text-align:center; padding:55px 15px 25px;">
                <h1 style="font-size:48px; color:#172554;">
                    🎓 LearnMate AI
                </h1>
                <p style="font-size:19px; color:#64748B;">
                    Your intelligent learning companion
                </p>
                <p style="font-size:15px; color:#64748B;">
                    Learn smarter. Practice better. Achieve more.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            "<h2 style='text-align:center;'>Get started with LearnMate AI</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center; color:#64748B;'>"
            "Choose how you would like to use the platform.</p>",
            unsafe_allow_html=True
        )

        left, middle, right = st.columns([1, 2, 1])

        with middle:

            with st.container(border=True):
                st.markdown("### 🎓 Student")
                st.write(
                    "Explore your syllabus, learn with AI, "
                    "practice quizzes and track your progress."
                )

                if st.button(
                    "Continue as Student",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state.user_role = "Student"
                    st.rerun()

            with st.container(border=True):
                st.markdown("### 👨‍🏫 Teacher")
                st.write(
                    "Manage courses, upload study materials "
                    "and monitor student performance."
                )

                if st.button(
                    "Continue as Teacher",
                    use_container_width=True
                ):
                    st.session_state.user_role = "Teacher"
                    st.rerun()

        st.markdown(
            "<p style='text-align:center; color:#94A3B8; "
            "font-size:12px; margin-top:45px;'>"
            "LearnMate AI | Intelligent Learning Platform"
            "</p>",
            unsafe_allow_html=True
        )

        st.stop()



    # ---------------- SIDEBAR ----------------

    st.sidebar.title("🎓 LearnMate AI")
    st.sidebar.caption("Your Intelligent Learning Companion")
    st.sidebar.divider()

    role = st.sidebar.selectbox(
    "Select your role",
    ["Student", "Teacher"],
    key="user_role"
)

    if role == "Student":
        page = st.sidebar.radio(
            "STUDENT MENU",
            [
                "Dashboard",
                "My Courses",
                "Syllabus Explorer",
                "AI Tutor",
                "Practice Quiz",
                "Flashcards",
                "My Notes",
                "Analytics"
            ]
        )
    else:
        page = st.sidebar.radio(
            "TEACHER MENU",
            [
                "Dashboard",
                "Manage Courses",
                "Upload Study Material",
                "Student Performance"
            ]
        )

    st.sidebar.divider()
    st.sidebar.caption("Version 1.0 | Project MVP")

    # ---------------- STUDENT DASHBOARD ----------------

    if role == "Student" and page == "Dashboard":

        st.title("Good to see you! 👋")
        st.write("Welcome to your personalised learning dashboard.")
        st.divider()

        # Statistics

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Courses Enrolled", "3", "+1")
        col2.metric("Topics Completed", "18", "+4")
        col3.metric("Study Hours", "24 hrs", "+3 hrs")
        col4.metric("Overall Progress", "53%", "+8%")

        st.write("")

        # Course Progress

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
                with st.container(border=True):
                    st.markdown(f"**{name}**")
                    st.progress(progress / 100)
                    st.write(f"**{progress}%** completed")
                    st.caption(topics)

        st.write("")

        # Weekly Activity

        st.subheader("📈 Weekly Learning Activity")

        activity = pd.DataFrame({
            "Day": [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ],
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

        # Quick Actions

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

        st.caption(
            "Dashboard currently displays sample data for development."
        )

    # ---------------- OTHER STUDENT PAGES ----------------

    elif role == "Student":

        st.title(f"🎓 {page}")
        st.divider()

        if page == "My Courses":
            st.subheader("Your Enrolled Courses")

            for name, progress, topics in [
                ("Python Programming", 75, 12),
                ("Mathematics", 55, 10),
                ("Data Structures", 30, 15)
            ]:
                with st.container(border=True):
                    st.subheader(name)
                    st.progress(progress / 100)
                    st.write(f"{progress}% completed | {topics} topics")

        elif page == "Syllabus Explorer":
            subject = st.selectbox(
                "Choose a subject",
                ["Python Programming", "Mathematics", "Data Structures"]
            )

            topics = {
                "Python Programming": [
                    "Introduction to Python",
                    "Variables and Data Types",
                    "Conditional Statements",
                    "Loops",
                    "Functions",
                    "Object-Oriented Programming"
                ],
                "Mathematics": [
                    "Matrices",
                    "Differentiation",
                    "Integration",
                    "Probability"
                ],
                "Data Structures": [
                    "Arrays",
                    "Linked Lists",
                    "Stacks",
                    "Queues",
                    "Trees"
                ]
            }

            st.subheader(f"{subject} Topics")

            for i, topic in enumerate(topics[subject], 1):
                with st.expander(f"Topic {i}: {topic}"):
                    st.write("Study material will be integrated here.")
                    st.checkbox(
                        "Mark as completed",
                        key=f"topic_{subject}_{i}"
                    )

        elif page == "AI Tutor":
            st.info(
                "AI integration will be connected through Member 2's module."
            )

            subject = st.selectbox(
                "Choose Subject",
                ["Python Programming", "Mathematics", "Data Structures"]
            )

            question = st.text_area(
                "Ask your question",
                placeholder="What would you like to learn today?"
            )

            if st.button("Ask AI Tutor", type="primary"):
                if question.strip():
                    st.warning("AI service is not connected yet.")
                else:
                    st.error("Please enter a question.")

        elif page == "Practice Quiz":
            st.subheader("Python Programming Quiz")

            answer = st.radio(
                "Which keyword defines a function in Python?",
                ["function", "def", "define", "fun"],
                index=None
            )

            if st.button("Submit Answer"):
                if answer is None:
                    st.warning("Select an answer first.")
                elif answer == "def":
                    st.success("Correct answer! Well done.")
                else:
                    st.error("Incorrect. The correct answer is 'def'.")

        elif page == "Flashcards":

            cards = [
                ("What is Python?",
                 "Python is a high-level programming language."),
                ("What is a variable?",
                 "A variable stores a value in a program."),
                ("What is a loop?",
                 "A loop repeats a block of code.")
            ]

            if "card_index" not in st.session_state:
                st.session_state.card_index = 0

            if "answer_visible" not in st.session_state:
                st.session_state.answer_visible = False

            index = st.session_state.card_index
            question, answer = cards[index]

            with st.container(border=True):
                st.caption(f"Flashcard {index + 1} of {len(cards)}")
                st.subheader(question)

                if st.session_state.answer_visible:
                    st.success(answer)

                if st.button("Show Answer"):
                    st.session_state.answer_visible = True
                    st.rerun()

            col1, col2 = st.columns(2)

            if col1.button("Previous"):
                st.session_state.card_index = (index - 1) % len(cards)
                st.session_state.answer_visible = False
                st.rerun()

            if col2.button("Next"):
                st.session_state.card_index = (index + 1) % len(cards)
                st.session_state.answer_visible = False
                st.rerun()

        elif page == "My Notes":

            subject = st.selectbox(
                "Select Subject",
                ["Python Programming", "Mathematics", "Data Structures"]
            )

            notes = st.text_area(
                "Write your notes",
                height=200
            )

            if st.button("Save Notes"):
                if notes.strip():
                    st.success(
                        "Notes entered successfully. "
                        "Permanent storage will be integrated later."
                    )
                else:
                    st.warning("Please write some notes.")

        elif page == "Analytics":

            st.subheader("Your Learning Analytics")

            col1, col2 = st.columns(2)

            col1.metric("Average Progress", "53%")
            col2.metric("Study Streak", "5 Days")

            st.info("Detailed student analytics will be integrated later.")

    # ---------------- TEACHER DASHBOARD ----------------

    else:

        st.title("Teacher Dashboard 👨‍🏫")
        st.write("Welcome to your teaching workspace.")
        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Students", "120")
        col2.metric("Active Courses", "4")
        col3.metric("Assessments", "12")

        if page == "Dashboard":

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

        elif page == "Manage Courses":

            st.subheader("Manage Courses")

            course_name = st.text_input("Course Name")
            description = st.text_area("Course Description")

            if st.button("Create Course"):
                if course_name.strip():
                    st.success(f"Course '{course_name}' entered.")
                else:
                    st.warning("Enter a course name.")

        elif page == "Upload Study Material":

            st.subheader("Upload Learning Resources")

            uploaded_file = st.file_uploader(
                "Choose a study material file",
                type=["pdf", "docx", "txt"]
            )

            if uploaded_file:
                st.success(f"{uploaded_file.name} selected.")

        elif page == "Student Performance":

            st.subheader("Student Performance")

            performance = pd.DataFrame({
                "Student": ["Student 1", "Student 2", "Student 3"],
                "Marks": [85, 72, 60]
            })

            st.dataframe(
                performance,
                use_container_width=True,
                hide_index=True
            )

            st.caption("Sample performance data.")


if __name__ == "__main__":
    run_app()
