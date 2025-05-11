from flask import Blueprint, request, jsonify, abort
from database.operations import (
    create_patient, get_patient, get_all_patients,
    update_patient, delete_patient
)
from database import get_session

patients_bp = Blueprint("patients", __name__)

@patients_bp.route("", methods=["GET"])
def list_patients():
    session = get_session()
    patients = get_all_patients(session)
    return jsonify([p.to_dict() for p in patients]), 200

@patients_bp.route("", methods=["POST"])
def add_patient():
    data = request.json
    session = get_session()
    patient = create_patient(session, **data)
    return jsonify(patient.to_dict()), 201

@patients_bp.route("/<int:patient_id>", methods=["GET"])
def read_patient(patient_id):
    session = get_session()
    patient = get_patient(session, patient_id)
    if not patient:
        abort(404, description="Patient not found")
    return jsonify(patient.to_dict()), 200

@patients_bp.route("/<int:patient_id>", methods=["PUT"])
def edit_patient(patient_id):
    data = request.json
    session = get_session()
    patient = update_patient(session, patient_id, **data)
    if not patient:
        abort(404, description="Patient not found")
    return jsonify(patient.to_dict()), 200

@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
def remove_patient(patient_id):
    session = get_session()
    success = delete_patient(session, patient_id)
    if not success:
        abort(404, description="Patient not found")
    return "", 204