import streamlit as st
from datetime import date, datetime

class AppointmentsUI:
    def __init__(self, patient_id, client):
        self.patient_id = patient_id
        self.client = client

    def render(self):
        st.header("Book an appointment")
        doctor_id = st.number_input("Doctor ID", min_value=1, value=1)
        appt_date = st.date_input("Appointment date", value=date.today())
        appt_time = st.text_input("Time (HH:MM)", value="09:00")
        if st.button("Book"):
            appt = self.client.create_appointment(
                self.patient_id,
                doctor_id,
                appt_date.isoformat(),
                appt_time
            )
            st.success(f"Appointment booked: {appt}")

        st.subheader("Your appointments")
        apps = self.client.get_appointments(self.patient_id)
        for a in apps:
            st.write(f"{a['date']} {a['time']} with doctor ID {a['doctor_id']} - Status: {a['status']}")