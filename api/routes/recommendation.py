from flask import Blueprint, request, jsonify
from database.operations import get_all_doctors
from some_ai_module import DoctorRecommender  # TODO: custom module for AI-based recommendations

recommendation_bp = Blueprint("recommendation", __name__)
recommender = DoctorRecommender()

@recommendation_bp.route("", methods=["POST"])
def recommend():
    """
    Receives JSON { patient_id: int, problem: str }
    Returns a list of recommended doctors
    """
    data = request.json
    problem = data["problem"]
    doctors = get_all_doctors()
    ranked = recommender.rank(doctors, problem)
    return jsonify([d.to_dict() for d in ranked]), 200
