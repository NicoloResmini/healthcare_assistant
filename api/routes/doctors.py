from flask import Blueprint, request, jsonify, abort
from database.operations import (
    create_doctor, get_doctor, get_all_doctors,
    update_doctor, delete_doctor
)
from database import get_session

doctors_bp = Blueprint("doctors", __name__)

@doctors_bp.route("", methods=["GET"])
def list_doctors():
    session = get_session()
    doctors = get_all_doctors(session)
    return jsonify([d.to_dict() for d in doctors]), 200

@doctors_bp.route("", methods=["POST"])
def add_doctor():
    data = request.json
    session = get_session()
    doctor = create_doctor(session, **data)
    return jsonify(doctor.to_dict()), 201

@doctors_bp.route("/<int:doctor_id>", methods=["GET"])
def read_doctor(doctor_id):
    session = get_session()
    doctor = get_doctor(session, doctor_id)
    if not doctor:
        abort(404, description="Doctor not found")
    return jsonify(doctor.to_dict()), 200

@doctors_bp.route("/<int:doctor_id>", methods=["PUT"])
def edit_doctor(doctor_id):
    data = request.json
    session = get_session()
    doctor = update_doctor(session, doctor_id, **data)
    if not doctor:
        abort(404, description="Doctor not found")
    return jsonify(doctor.to_dict()), 200

@doctors_bp.route("/<int:doctor_id>", methods=["DELETE"])
def remove_doctor(doctor_id):
    session = get_session()
    success = delete_doctor(session, doctor_id)
    if not success:
        abort(404, description="Doctor not found")
    return "", 204