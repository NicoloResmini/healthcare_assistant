from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime


Base = declarative_base()


def get_engine(db_url: str = None):
    """
    Returns a SQLAlchemy engine for the relational database.
    By default uses SQLite locale.
    """
    if db_url is None:
        db_url = "sqlite:///healthcare_assistant.db"
    engine = create_engine(db_url, echo=False)
    return engine


def get_session(db_url: str = None):
    """
    Creates a new session for the database.
    """
    engine = get_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    appointments = relationship("Appointment", back_populates="patient")
    chats = relationship("ChatMessage", back_populates="patient")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None
        }


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    appointments = relationship("Appointment", back_populates="doctor")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialization": self.specialization,
            "email": self.email
        }


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(String, nullable=False)
    status = Column(String, default="scheduled")  # scheduled, completed, canceled

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date.isoformat(),
            "time": self.time,
            "status": self.status
        }


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    message = Column(String, nullable=False)
    response = Column(String, nullable=False)

    patient = relationship("Patient", back_populates="chats")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "response": self.response
        }