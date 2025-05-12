"""
Script di avvio e demo per l’intera applicazione Healthcare Assistant.
Esegue:
  1. Inizializzazione del database (SQLite di default)
  2. Popolamento con dati di esempio (paziente, dottore, appuntamento)
  3. Indicizzazione di un piccolo set di documenti medici
  4. Simulazione:
     • Chat RAG (retrieval + generation)
     • Raccomandazione medici
     • Calcolo degli slot disponibili
"""

import threading
import time
import webbrowser
import requests

from database.schema import Base, get_engine
from database.operations import (
    get_session,
    create_patient, create_doctor, create_appointment,
    save_chat_message, get_available_slots
)
from rag.retriever import Retriever
from rag.generator import Generator
from models.recommender import DoctorRecommender

API_BASE = "http://localhost:5000/api"


def init_db():
    engine = get_engine()                
    Base.metadata.create_all(engine)
    print("[DB] Database inizializzato.")


def seed_data(session):
    print("[DB] Creo dati di esempio...")
    p = create_patient(session,
                       first_name="Giulia",
                       last_name="Verdi",
                       email="giulia.verdi@example.com",
                       date_of_birth="1985-07-15")
    d = create_doctor(session,
                      first_name="Luca",
                      last_name="Bianchi",
                      specialization="Cardiologia",
                      email="luca.bianchi@example.com")
    appt = create_appointment(session,
                              patient_id=p.id,
                              doctor_id=d.id,
                              date=str(time.strftime("%Y-%m-%d")),
                              time="10:00")
    print(f"  Paziente:  {p.to_dict()}")
    print(f"  Dottore:   {d.to_dict()}")
    print(f"  Appuntamento schedulato: {appt.to_dict()}")
    return p, d


def start_backend():
    """Avvia il server Flask in un thread separato."""
    from api.app import create_app
    app = create_app()
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=False),
                     daemon=True).start()
    print("[API] Backend Flask avviato su http://localhost:5000")
    time.sleep(2)


def index_documents():
    print("[RAG] Indicizzo documenti di esempio...")
    docs = [
        "Il diabete mellito è una condizione cronica caratterizzata da iperglicemia.",
        "I sintomi della polmonite includono tosse, febbre e difficoltà respiratorie."
    ]
    retriever = Retriever(index_path="data/faiss_index.idx")
    retriever.index_documents(docs)
    print("[RAG] Indicizzazione completata.")


def demo_chat(patient_id: int):
    print("\n[DEMO] Chat RAG")
    question = "Quali sono i sintomi della polmonite?"
    print(f"Domanda: {question}")
    retriever = Retriever(index_path="data/faiss_index.idx")
    docs = retriever.retrieve(question, top_k=2)
    gen = Generator()
    answer = gen.generate(question, docs)
    print(f"Risposta: {answer}")


def demo_recommendation(problem: str):
    print("\n[DEMO] Raccomandazione medici")
    resp = requests.get(f"{API_BASE}/doctors")
    doctors = resp.json()
    recommender = DoctorRecommender()
    ranked = recommender.rank(doctors, problem)
    print(f"Problema: {problem}")
    print("Medici consigliati (in ordine):")
    for doc in ranked:
        print(f"  • {doc['first_name']} {doc['last_name']} ({doc['specialization']})")


def demo_slots(doctor_id: int):
    print("\n[DEMO] Calcolo slot disponibili")
    today = time.strftime("%Y-%m-%d")
    session = get_session()
    slots = get_available_slots(session, doctor_id, today)
    print(f"Slot liberi per dottore #{doctor_id} in data {today}:")
    for s in slots:
        print(f"  • {s}")


if __name__ == "__main__":
    # 1) Inizializza DB e dati
    init_db()
    session = get_session()
    p, d = seed_data(session)

    # 2) Avvia backend
    start_backend()

    # 3) Indicizza documenti
    index_documents()

    # 4) Demo console
    demo_chat(patient_id=p.id)
    demo_recommendation(problem="ho dolore al petto e affanno")
    demo_slots(doctor_id=d.id)

    # 5) Apri frontend nel browser
    print("\n[ACTION] Avvio interfaccia Streamlit...")
    webbrowser.open("http://localhost:8501")
    # Nota: dev’essere lanciato separatamente con `streamlit run frontend/app.py`
    print("Per l'interfaccia grafica, in un altro terminale esegui:\n\n  streamlit run frontend/app.py\n")