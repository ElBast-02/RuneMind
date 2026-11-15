
import os
import sys
import tempfile
import unittest
from pathlib import Path

# ==========================================
# 1. TEST DATABASE SETUP
# ==========================================

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

# Create a temporary database for testing
test_db = tempfile.TemporaryDirectory()

os.environ["DATABASE_URL"] = (
    "sqlite:///" + str(Path(test_db.name) / "test.db").replace("\\", "/")
)

# Import Flask application after setting the test database
from app import app, db, User


# ==========================================
# 2. AUTHENTICATION TESTS
# ==========================================

class AuthenticationTests(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        # Close database connections after all tests
        with app.app_context():
            db.session.remove()
            db.engine.dispose()

        # Delete the temporary test database
        test_db.cleanup()

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        # Reset database before each test
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    # --------------------------------------
    # Helper: Register a test user
    # --------------------------------------

    def register_user(self):
        return self.client.post("/api/register", json={
            "username": "TestPlayer",
            "email": "test@example.com",
            "password": "password123"
        })

    # ======================================
    # TEST 1: HEALTH CHECK
    # ======================================

    def test_health(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    # ======================================
    # TEST 2: USER REGISTRATION
    # ======================================

    def test_registration(self):
        response = self.register_user()

        self.assertEqual(response.status_code, 201)

        with app.app_context():
            user = User.query.filter_by(
                email="test@example.com"
            ).first()

            self.assertIsNotNone(user)
            self.assertNotEqual(user.password_hash, "password123")
            self.assertTrue(user.check_password("password123"))

    # ======================================
    # TEST 3: DUPLICATE REGISTRATION
    # ======================================

    def test_duplicate_registration(self):
        self.register_user()

        response = self.register_user()

        self.assertEqual(response.status_code, 409)

    # ======================================
    # TEST 4: VALID LOGIN
    # ======================================

    def test_login(self):
        self.register_user()

        response = self.client.post("/api/login", json={
            "email": "test@example.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Logged in successfully"
        )

    # ======================================
    # TEST 5: INVALID LOGIN
    # ======================================

    def test_invalid_login(self):
        self.register_user()

        response = self.client.post("/api/login", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 401)

    # ======================================
    # TEST 6: PROTECTED PROFILE
    # ======================================

    def test_protected_profile(self):
        response = self.client.get("/api/profile")

        self.assertEqual(response.status_code, 401)

    # ======================================
    # TEST 7: LOGOUT
    # ======================================

    def test_logout(self):
        self.register_user()

        self.client.post("/api/login", json={
            "email": "test@example.com",
            "password": "password123"
        })

        response = self.client.post("/api/logout")

        self.assertEqual(response.status_code, 200)

        # Verify user cannot access profile after logout
        profile_response = self.client.get("/api/profile")

        self.assertEqual(profile_response.status_code, 401)


# ==========================================
# 3. RUN TESTS
# ==========================================

if __name__ == "__main__":
    unittest.main()
