
import os

from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from sqlalchemy.exc import IntegrityError

from models import db, User


# ==========================================
# 1. INITIALIZE FLASK
# ==========================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-only-change-before-deployment"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///runemind.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# ==========================================
# 2. INITIALIZE DATABASE
# ==========================================

db.init_app(app)

with app.app_context():
    db.create_all()


# ==========================================
# 3. INITIALIZE FLASK-LOGIN
# ==========================================

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        "error": "Authentication required. Please log in."
    }), 401


# ==========================================
# 4. HOME ENDPOINT
# ==========================================

@app.get("/")
def home():
    return jsonify({
        "project": "RuneMind",
        "message": "Welcome to RuneMind!",
        "status": "running"
    })


# ==========================================
# 5. HEALTH CHECK
# ==========================================

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "RuneMind Backend"
    })


# ==========================================
# 6. USER REGISTRATION
# ==========================================

@app.post("/api/register")
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A JSON object is required"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all(
        isinstance(value, str)
        for value in (username, email, password)
    ):
        return jsonify({
            "error": "All fields must be strings"
        }), 400

    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password:
        return jsonify({
            "error": "All fields are required"
        }), 400

    if len(username) > 50 or len(email) > 120:
        return jsonify({
            "error": "Username or email is too long"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must contain at least 8 characters"
        }), 400

    if "@" not in email:
        return jsonify({
            "error": "Invalid email address"
        }), 400

    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        return jsonify({
            "error": "Username or email already registered"
        }), 409

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "Username or email already registered"
        }), 409

    return jsonify({
        "message": "Account created successfully",
        "user_id": user.id,
        "username": user.username
    }), 201


# ==========================================
# 7. USER LOGIN
# ==========================================

@app.post("/api/login")
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A JSON object is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({
            "error": "Email and password are required"
        }), 400

    email = email.strip().lower()

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    login_user(user)

    return jsonify({
        "message": "Logged in successfully",
        "user_id": user.id,
        "username": user.username
    }), 200


# ==========================================
# 8. PROTECTED USER PROFILE
# ==========================================

@app.get("/api/profile")
@login_required
def profile():
    return jsonify({
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }), 200


# ==========================================
# 9. USER LOGOUT
# ==========================================

@app.post("/api/logout")
@login_required
def logout():
    logout_user()

    return jsonify({
        "message": "Logged out successfully"
    }), 200


# ==========================================
# 10. START FLASK SERVER
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
