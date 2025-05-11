import streamlit as st
from frontend.pages.home import home_page
from frontend.pages.chat import chat_page
from frontend.pages.appointments import appointments_page
from frontend.pages.history import history_page

PAGES = {
    "Home": home_page,
    "Chat": chat_page,
    "Appointments": appointments_page,
    "History": history_page,
}

st.set_page_config(page_title="Healthcare Assistant", layout="wide")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page()