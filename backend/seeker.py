from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)  # allow Netlify or any frontend to send requests


@app.route("/")
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "Seeker API is live ✅",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/seeker", methods=["POST"])
def seeker():
    """Receive tracking + form data and log it"""
    try:
        # Accept JSON or form data
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()

        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- LIVE RENDER LOGS ---
        print("\n📍 --- NEW TRACKING LOG ---")
        print("Timestamp:", data["timestamp"])
        print(json.dumps(data, indent=2))
        print("---------------------------\n")

        return jsonify({
            "status": "success",
            "message": "Data received successfully",
            "data": data
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
