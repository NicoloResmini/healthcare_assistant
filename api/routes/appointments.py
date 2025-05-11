from flask import Blueprint, request, jsonify, abort
from database.operations import (
    create_appointment, get_appointment,
    get_appointments_by_patient, update_appointment, delete_appointment
)
from database import get_session

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("", methods=["GET"])
def list_appointments():
    session = get_session()
    patient_id = request.args.get("patient_id", type=int)
    if patient_id:
        apps = get_appointments_by_patient(session, patient_id)
    else:
        apps = session.query(Appointment).all()
    return jsonify([a.to_dict() for a in apps]), 200
    
@appointments_bp.route("", methods=["POST"])
def book_appointment():
    data = request.json
    session = get_session()
    appt = create_appointment(session, **data)
    return jsonify(appt.to_dict()), 201

@appointments_bp.route("/<int:appt_id>", methods=["GET"])
def read_appointment(appt_id):
    session = get_session()
    appt = get_appointment(session, appt_id)
    if not appt:
        abort(404, description="Appointment not found")
    return jsonify(appt.to_dict()), 200

@appointments_bp.route("/<int:appt_id>", methods=["PUT"])
def edit_appointment(appt_id):
    data = request.json
    session = get_session()
    appt = update_appointment(session, appt_id, **data)
    if not appt:
        abort(404, description="Appointment not found")
    return jsonify(appt.to_dict()), 200

@appointments_bp.route("/<int:appt_id>", methods=["DELETE"])
def cancel_appointment(appt_id):
    session = get_session()
    success = delete_appointment(session, appt_id)
    if not success:
        abort(404, description="Appointment not found")
    return "", 204