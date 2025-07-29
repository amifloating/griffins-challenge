from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import init_db, get_user_progress, submit_answer, get_next_challenge

# Create Flask app
app = Flask(__name__)

# Secret key for session encryption (replace in production!)
app.secret_key = "super-secret-key"

# Enable Cross-Origin Resource Sharing so frontend can talk to backend
CORS(app, supports_credentials=True)

# Initialize the database when the app starts
@app.before_first_request
def setup():
    init_db()

# Endpoint to log in a user by username
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    session['username'] = username  # Save username in session
    return jsonify({"message": "Logged in", "username": username})

# Endpoint to get current user progress
@app.route('/progress', methods=['GET'])
def progress():
    username = session.get('username')
    return jsonify(get_user_progress(username))

# Endpoint to get the current challenge for the user
@app.route('/challenge', methods=['GET'])
def get_challenge():
    username = session.get('username')
    return jsonify(get_next_challenge(username))

# Endpoint to submit an answer to a challenge
@app.route('/submit', methods=['POST'])
def submit():
    username = session.get('username')
    flag = request.json.get("flag")
    return jsonify(submit_answer(username, flag))

# Run the Flask app in debug mode for development
if __name__ == '__main__':
    app.run(debug=True)
