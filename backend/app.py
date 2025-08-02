from flask import Flask, request, jsonify
import hashlib
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ✅ Function to check if password is pwned using HaveIBeenPwned API
def check_pwned(password):
    sha1pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1pwd[:5]
    suffix = sha1pwd[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return "❌ Error: API request failed"

        hashes = (line.split(":") for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"⚠️ Found in {count} breaches!"
        return "✅ No breach found."
    except requests.RequestException:
        return "❌ Network Error: Unable to check breaches"

@app.route("/")
def home():
    return jsonify({"message": "SecureKey Insight API is running!"})

@app.route("/api/check", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    result = check_pwned(password)
    return jsonify({"breach_result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
