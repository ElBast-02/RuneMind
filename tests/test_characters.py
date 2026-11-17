
import unittest

from test_auth import app, db


class CharacterTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        with app.app_context():
            db.session.remove()
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

    def register_and_login(self):
        self.client.post("/api/register", json={
            "username": "CharacterTester",
            "email": "character@example.com",
            "password": "password123"
        })

        return self.client.post("/api/login", json={
            "email": "character@example.com",
            "password": "password123"
        })

    def test_create_character(self):
        login_response = self.register_and_login()

        self.assertEqual(login_response.status_code, 200)

        response = self.client.post("/api/characters", json={
            "name": "Tarnished",
            "vigor": 40,
            "strength": 30,
            "dexterity": 25
        })

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.json["message"],
            "Character saved successfully"
        )

        with app.app_context():
            from models import Character

            character = Character.query.filter_by(
                name="Tarnished"
            ).first()

            self.assertIsNotNone(character)
            self.assertEqual(character.vigor, 40)
            self.assertEqual(character.strength, 30)
            self.assertEqual(character.dexterity, 25)


    def test_get_characters(self):
        # Register and log in
        self.register_and_login()

        # Create a character
        create_response = self.client.post("/api/characters", json={
            "name": "Samurai",
            "vigor": 35,
            "strength": 20,
            "dexterity": 45
        })

        self.assertEqual(create_response.status_code, 201)

        # Retrieve saved characters
        response = self.client.get("/api/characters")

        self.assertEqual(response.status_code, 200)

        characters = response.json["characters"]

        # Verify the saved character was returned
        self.assertEqual(len(characters), 1)
        self.assertEqual(characters[0]["name"], "Samurai")
        self.assertEqual(characters[0]["vigor"], 35)
        self.assertEqual(characters[0]["strength"], 20)
        self.assertEqual(characters[0]["dexterity"], 45)
        
        
    def test_unauthorized_character_access(self):
        # Attempt to retrieve characters without logging in
        get_response = self.client.get("/api/characters")

        self.assertEqual(get_response.status_code, 401)

        # Attempt to create a character without logging in
        post_response = self.client.post("/api/characters", json={
            "name": "UnauthorizedPlayer",
            "vigor": 40,
            "strength": 30,
            "dexterity": 25
        })

        self.assertEqual(post_response.status_code, 401)

        # Verify no character was saved to the database
        from models import Character

        with app.app_context():
            self.assertEqual(Character.query.count(), 0)


    def test_invalid_character_attributes(self):
        # Register and log in
        self.register_and_login()

        invalid_characters = [
            {
                "name": "InvalidVigor",
                "vigor": 150,
                "strength": 30,
                "dexterity": 25
            },
            {
                "name": "InvalidStrength",
                "vigor": 40,
                "strength": 0,
                "dexterity": 25
            },
            {
                "name": "InvalidDexterity",
                "vigor": 40,
                "strength": 30,
                "dexterity": -5
            },
            {
                "name": "",
                "vigor": 40,
                "strength": 30,
                "dexterity": 25
            },
            {
                "name": "InvalidType",
                "vigor": "forty",
                "strength": 30,
                "dexterity": 25
            }
        ]

        for character_data in invalid_characters:
            with self.subTest(character=character_data):
                response = self.client.post(
                    "/api/characters",
                    json=character_data
                )

                self.assertEqual(response.status_code, 400)

        # Confirm none of the invalid characters were saved
        from models import Character

        with app.app_context():
            self.assertEqual(Character.query.count(), 0)


    def test_character_user_isolation(self):
        # Register and log in as User A
        self.register_and_login()

        # User A creates a character
        response = self.client.post("/api/characters", json={
            "name": "PlayerACharacter",
            "vigor": 40,
            "strength": 30,
            "dexterity": 25
        })

        self.assertEqual(response.status_code, 201)

        # Log out User A
        logout_response = self.client.post("/api/logout")
        self.assertEqual(logout_response.status_code, 200)

        # Register User B
        register_response = self.client.post("/api/register", json={
            "username": "SecondPlayer",
            "email": "second@example.com",
            "password": "password456"
        })

        self.assertEqual(register_response.status_code, 201)

        # Log in as User B
        login_response = self.client.post("/api/login", json={
            "email": "second@example.com",
            "password": "password456"
        })

        self.assertEqual(login_response.status_code, 200)

        # User B retrieves their characters
        response = self.client.get("/api/characters")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["characters"], [])

        # Log out User B
        self.client.post("/api/logout")

        # Log back in as User A
        self.client.post("/api/login", json={
            "email": "character@example.com",
            "password": "password123"
        })

        # Verify User A can still retrieve their character
        response = self.client.get("/api/characters")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["characters"]), 1)
        self.assertEqual(
            response.json["characters"][0]["name"],
            "PlayerACharacter"
        )


if __name__ == "__main__":
    unittest.main()
