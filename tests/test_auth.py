
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

# Set the test database before importing app.py.
# This prevents the application from using the normal database.
test_db = tempfile.TemporaryDirectory()

os.environ["DATABASE_URL"] = (
    "sqlite:///" + str(Path(test_db.name) / "test.db").replace("\\", "/")
)

from app import app, db, User # noqa: E402


class AuthenticationTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.engine.dispose()

    def register_user(self):
        return self.client.post("/api/register", json={
            "username": "TestPlayer",
            "email": "test@example.com",
            "password": "password123"
        })

    def test_health(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

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

    def test_duplicate_registration(self):
        self.register_user()
        response = self.register_user()

        self.assertEqual(response.status_code, 409)

    def test_login(self):
        self.register_user()

        response = self.client.post("/api/login", json={
            "email": "test@example.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        self.register_user()

        response = self.client.post("/api/login", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 401)

    def test_protected_profile(self):
        response = self.client.get("/api/profile")

        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        self.register_user()

        self.client.post("/api/login", json={
            "email": "test@example.com",
            "password": "password123"
        })

        response = self.client.post("/api/logout")

        self.assertEqual(response.status_code, 200)

        profile_response = self.client.get("/api/profile")

        self.assertEqual(profile_response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
