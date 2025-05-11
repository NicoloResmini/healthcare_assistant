import streamlit as st
from frontend.components.chat_ui import ChatUI
from api_client import ApiClient

client = ApiClient()

def chat_page():
    st.title("Chat with the assistant")
    patient_id = st.sidebar.number_input("Patient ID", min_value=1, value=1)
    ui = ChatUI()
    if ui.user_message:
        response = client.send_message(patient_id, ui.user_message)
        ui.display_response(response)
    ui.render()