from sqlalchemy.orm import Session
from .schema import Patient, Doctor, Appointment, ChatMessage, get_session
from typing import List, Optional
import datetime

# Patients CRUD

def create_patient(session: Session, first_name: str, last_name: str,
                   email: str, date_of_birth: Optional[str] = None) -> Patient:
    dob = None
    if date_of_birth:
        dob = datetime.datetime.fromisoformat(date_of_birth).date()
    patient = Patient(
        first_name=first_name,
        last_name=last_name,
        email=email,
        date_of_birth=dob
    )
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


def get_patient(session: Session, patient_id: int) -> Optional[Patient]:
    return session.query(Patient).filter(Patient.id == patient_id).first()


def get_all_patients(session: Session) -> List[Patient]:
    return session.query(Patient).all()


def update_patient(session: Session, patient_id: int, **kwargs) -> Optional[Patient]:
    patient = get_patient(session, patient_id)
    if not patient:
        return None
    for key, value in kwargs.items():
        if hasattr(patient, key):
            setattr(patient, key, value)
    session.commit()
    return patient


def delete_patient(session: Session, patient_id: int) -> bool:
    patient = get_patient(session, patient_id)
    if not patient:
        return False
    session.delete(patient)
    session.commit()
    return True


# Doctors CRUD

def create_doctor(session: Session, first_name: str, last_name: str,
                  specialization: str, email: str) -> Doctor:
    doctor = Doctor(
        first_name=first_name,
        last_name=last_name,
        specialization=specialization,
        email=email
    )
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor


def get_doctor(session: Session, doctor_id: int) -> Optional[Doctor]:
    return session.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_all_doctors(session: Session) -> List[Doctor]:
    return session.query(Doctor).all()


def update_doctor(session: Session, doctor_id: int, **kwargs) -> Optional[Doctor]:
    doctor = get_doctor(session, doctor_id)
    if not doctor:
        return None
    for key, value in kwargs.items():
        if hasattr(doctor, key):
            setattr(doctor, key, value)
    session.commit()
    return doctor


def delete_doctor(session: Session, doctor_id: int) -> bool:
    doctor = get_doctor(session, doctor_id)
    if not doctor:
        return False
    session.delete(doctor)
    session.commit()
    return True


# Appointments CRUD

def create_appointment(session: Session, patient_id: int, doctor_id: int,
                       date: str, time: str, status: str = "scheduled") -> Appointment:
    appt_date = datetime.date.fromisoformat(date)
    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        date=appt_date,
        time=time,
        status=status
    )
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


def get_appointment(session: Session, appointment_id: int) -> Optional[Appointment]:
    return session.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments_by_patient(session: Session, patient_id: int) -> List[Appointment]:
    return session.query(Appointment).filter(Appointment.patient_id == patient_id).all()


def update_appointment(session: Session, appointment_id: int, **kwargs) -> Optional[Appointment]:
    appt = get_appointment(session, appointment_id)
    if not appt:
        return None
    for key, value in kwargs.items():
        if hasattr(appt, key):
            setattr(appt, key, value)
    session.commit()
    return appt


def delete_appointment(session: Session, appointment_id: int) -> bool:
    appt = get_appointment(session, appointment_id)
    if not appt:
        return False
    session.delete(appt)
    session.commit()
    return True


# Chat CRUD

def save_chat_message(session: Session, patient_id: int, message: str, response: str) -> ChatMessage:
    chat = ChatMessage(
        patient_id=patient_id,
        message=message,
        response=response
    )
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat


def get_chat_history(session: Session, patient_id: int) -> List[ChatMessage]:
    return session.query(ChatMessage).filter(ChatMessage.patient_id == patient_id).order_by(ChatMessage.timestamp).all()

def get_chat_message(session: Session, message_id: int) -> Optional[ChatMessage]:
    return session.query(ChatMessage).filter(ChatMessage.id == message_id).first()

def update_chat_message(session: Session, message_id: int, **kwargs) -> Optional[ChatMessage]:
    chat_message = get_chat_message(session, message_id)
    if not chat_message:
        return None
    for key, value in kwargs.items():
        if hasattr(chat_message, key):
            setattr(chat_message, key, value)
    session.commit()
    return chat_message

def delete_chat_message(session: Session, message_id: int) -> bool:
    chat_message = get_chat_message(session, message_id)
    if not chat_message:
        return False
    session.delete(chat_message)
    session.commit()
    return True