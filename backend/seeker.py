from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import csv, os

app = Flask(__name__)
CORS(app)

os.makedirs("db", exist_ok=True)
CSV_FILE = "db/results.csv"

@app.route("/")
def home():
    return jsonify({"message": "Seeker API is live"})

@app.route("/seeker", methods=["POST"])
def seeker():
    try:
        data = request.form.to_dict() or request.get_json(force=True)
        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        fieldnames = list(data.keys())
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists: writer.writeheader()
            writer.writerow(data)

        print("\n--- NEW SUBMISSION ---")
        for k, v in data.items(): print(f"{k}: {v}")

        return jsonify({"status": "success", "message": "Data saved", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
