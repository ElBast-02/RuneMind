# RuneMind

RuneMind is an Elden Ring companion website developed as a Computer Engineering graduation project.

The goal is to help players manage their characters, plan builds, and improve their gameplay.

## Features

### User Authentication (Implemented)
- Register a new account
- Log in and log out
- Secure password hashing
- User sessions using Flask-Login
- Protected dashboard for logged-in users
- Registration input validation

### Build Advisor (Planned)
- Character attributes and leveling recommendations
- Weapon and equipment recommendations
- Boss preparation assistance

### Gameplay Analyzer (Planned)
- Machine learning-based gameplay analysis
- Combat classification based on available labeled data

## Technologies

- Frontend: HTML, CSS, JavaScript, Jinja2
- Backend: Python, Flask
- Database: SQLite with Flask-SQLAlchemy
- Authentication: Flask-Login and Werkzeug password hashing
- Testing: Python unittest
- CI/CD: GitHub Actions
- Machine Learning: Model and libraries to be selected after dataset inspection

## Requirements

- Python 3.11 or newer

## Installation

Install the required Python libraries:

```cmd
python -m pip install flask flask-sqlalchemy flask-login
```

## Run the Application

From the RuneMind project folder:

```cmd
python backend\app.py
```

Open the following pages:

- Registration: http://127.0.0.1:5000/register
- Login: http://127.0.0.1:5000/login
- Dashboard: http://127.0.0.1:5000/dashboard
- Health-check API: http://127.0.0.1:5000/api/health

The dashboard requires the user to be logged in.

## Authentication

Users can register with a username, email, and password.

Passwords are stored as hashes instead of plaintext.

After registration, users can log in and access their dashboard. Logging out ends their authenticated session.

## Automated Testing

Run the authentication tests from the project folder:

```cmd
python -m unittest discover -s tests -v
```

The current test suite contains 7 automated authentication and API tests.

GitHub Actions automatically runs Python syntax checks and automated tests when code is pushed to GitHub or a pull request is opened.

Workflow file: `.github/workflows/ci.yml`

## Project Management

Development is tracked using GitHub Issues and the RuneMind Dev Kanban board.

Each development commit references its related GitHub Issue.

Screen designs are stored in `docs/screens/` before implementing the corresponding frontend pages.