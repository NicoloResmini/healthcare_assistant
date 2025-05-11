from flask import Flask
from api.routes.patients import patients_bp
from api.routes.doctors import doctors_bp
from api.routes.appointments import appointments_bp
from api.routes.chat import chat_bp
from api.routes.recommendation import recommendation_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config") 

    app.register_blueprint(patients_bp, url_prefix="/api/patients")
    app.register_blueprint(doctors_bp, url_prefix="/api/doctors")
    app.register_blueprint(appointments_bp, url_prefix="/api/appointments")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendation")


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
