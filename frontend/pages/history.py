import streamlit as st
from api_client import ApiClient

client = ApiClient()

def history_page():
    st.title("Chat History")
    patient_id = st.sidebar.number_input("Patient ID", min_value=1, value=1)
    chats = client.get_chat_history(patient_id)
    for msg in chats:
        st.markdown(f"**You:** {msg['message']}")
        st.markdown(f"**Assistant:** {msg['response']}")