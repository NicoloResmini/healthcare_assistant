import requests

class ApiClient:
    BASE_URL = "http://localhost:5000/api"

    def send_message(self, patient_id, message):
        resp = requests.post(
            f"{self.BASE_URL}/chat/message",
            json={"patient_id": patient_id, "message": message}
        )
        return resp.json().get("response")

    def create_appointment(self, patient_id, doctor_id, date, time):
        resp = requests.post(
            f"{self.BASE_URL}/appointments",
            json={
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "date": date,
                "time": time
            }
        )
        return resp.json()

    def get_appointments(self, patient_id):
        resp = requests.get(
            f"{self.BASE_URL}/appointments",
            params={"patient_id": patient_id}
        )
        return resp.json()

    def get_chat_history(self, patient_id):
        resp = requests.get(
            f"{self.BASE_URL}/chat/history",
            params={"patient_id": patient_id}
        )
        return resp.json()