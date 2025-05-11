import streamlit as st

class ChatUI:
    def __init__(self):
        self.user_message = None

    def render(self):
        self.user_message = st.text_input("Write a message:")

    def display_response(self, response: str):
        st.markdown(f"**Assistant:** {response}")