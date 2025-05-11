import streamlit as st
from frontend.components.appointments_ui import AppointmentsUI
from api_client import ApiClient

client = ApiClient()

def appointments_page():
    st.title("Appointments Management")
    patient_id = st.sidebar.number_input("Patient ID", min_value=1, value=1)
    ui = AppointmentsUI(patient_id, client)
    ui.render()