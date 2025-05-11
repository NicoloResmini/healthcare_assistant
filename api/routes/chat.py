from flask import Blueprint, request, jsonify
from rag.retriever import Retriever 
from rag.generator import Generator 
from database import get_session
from database.operations import save_chat_message

chat_bp = Blueprint("chat", __name__)

retriever = Retriever()
generator = Generator()

@chat_bp.route("/message", methods=["POST"])
def handle_message():
    """
    Receives JSON { patient_id: int, message: str }
    - retrieves relevant documents
    - generates response
    - saves the chat in DB
    """
    data = request.json
    pid = data["patient_id"]
    msg = data["message"]

    # 1) retrieval
    docs = retriever.retrieve(msg)

    # 2) generation
    response = generator.generate(question=msg, context_docs=docs)

    # 3) saves in DB
    session = get_session()
    save_chat_message(session, patient_id=pid, message=msg, response=response)

    return jsonify({"response": response}), 200
