"""
Mission 80 Coach
Navigation Components
Version 2.0
"""

import streamlit as st


MENU_ITEMS = [
    ("🏠", "Dashboard"),
    ("💪", "Workout"),
    ("📚", "Exercise Library"),
    ("🍽", "Nutrition"),
    ("📈", "Progress"),
    ("🤖", "AI Coach"),
    ("⚙️", "Settings"),
]


def sidebar_navigation() -> str:
    """
    Main navigation used throughout the app.
    """

    with st.sidebar:

        st.markdown("## 💪 Mission 80 Coach")

        st.markdown("---")

        page = st.radio(
            "Navigate",
            [item[1] for item in MENU_ITEMS],
            format_func=lambda x: next(icon for icon, name in MENU_ITEMS if name == x)
            + " "
            + x,
        )

        st.markdown("---")

        st.caption("Mission Progress")

        st.progress(0.33)

        st.caption("95 kg ➜ 80 kg")

        st.markdown("---")

        st.caption("Version 2.0")

    return page


def top_navigation():

    st.markdown(
        """
        <style>

        .topbar{
            display:flex;
            justify-content:space-between;
            align-items:center;
            background:#1E293B;
            padding:12px 18px;
            border-radius:18px;
            margin-bottom:20px;
            border:1px solid rgba(255,255,255,.08);
        }

        .topbar h2{
            margin:0;
            color:white;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="topbar">
            <h2>Mission 80 Coach</h2>
            <div>💪 Stay Consistent</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bottom_status():

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Workout Streak", "0")

    with col2:
        st.metric("Coach Score", "0")

    with col3:
        st.metric("Mission", "95 ➜ 80")