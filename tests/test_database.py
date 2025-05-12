import pytest
from database.schema import Base, get_engine, get_session
from database.operations import (
    create_patient, get_patient, get_all_patients, update_patient, delete_patient,
    create_doctor, get_doctor, get_all_doctors, update_doctor, delete_doctor,
    create_appointment, get_appointment, get_appointments_by_patient,
    save_chat_message, get_chat_history
)

@pytest.fixture(scope='function')
def session():
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return get_session(db_url="sqlite:///:memory:")

def test_patient_crud(session):
    # Create
    p = create_patient(session, "Mario", "Rossi", "mario@esempio.com", "1990-01-01")
    assert p.id is not None
    # Read
    fetched = get_patient(session, p.id)
    assert fetched.email == "mario@esempio.com"
    # Update
    updated = update_patient(session, p.id, first_name="Luigi")
    assert updated.first_name == "Luigi"
    # List all
    all_p = get_all_patients(session)
    assert len(all_p) == 1
    # Delete
    res = delete_patient(session, p.id)
    assert res is True
    assert get_patient(session, p.id) is None

def test_doctor_crud(session):
    d = create_doctor(session, "Anna", "Bianchi", "Cardiologia", "anna@esempio.com")
    assert d.id
    fetched = get_doctor(session, d.id)
    assert fetched.specialization == "Cardiologia"
    updated = update_doctor(session, d.id, last_name="Verdi")
    assert updated.last_name == "Verdi"
    all_d = get_all_doctors(session)
    assert len(all_d) == 1
    res = delete_doctor(session, d.id)
    assert res
    assert get_doctor(session, d.id) is None

def test_appointment_chat_crud(session):
    # Create patient and doctor
    p = create_patient(session, "Test", "User", "test@u.com", None)
    d = create_doctor(session, "Doc", "Tor", "Ortopedia", "doc@u.com")
    # Appointment
    appt = create_appointment(session, p.id, d.id, "2025-05-20", "10:00")
    assert appt.id
    fetched = get_appointment(session, appt.id)
    assert fetched.time == "10:00"
    apps = get_appointments_by_patient(session, p.id)
    assert len(apps) == 1
    # Chat
    chat = save_chat_message(session, p.id, "Ciao", "Hello")
    assert chat.response == "Hello"
    history = get_chat_history(session, p.id)
    assert len(history) == 1