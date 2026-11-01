
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "project": "RuneMind",
        "message": "Welcome to RuneMind!",
        "status": "running"
    })

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "RuneMind Backend"
    })

if __name__ == "__main__":
    app.run(debug=True)
