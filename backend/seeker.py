from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import csv
import os

app = Flask(__name__)
CORS(app)  # 👈 allows requests from any origin (Netlify, localhost, etc.)

# ensure db folder exists
os.makedirs("db", exist_ok=True)
CSV_FILE = "db/results.csv"


@app.route("/")
def home():
    return jsonify({"message": "Seeker API is live", "timestamp": datetime.now().isoformat()})


@app.route("/seeker", methods=["POST"])
def seeker():
    try:
        data = request.form.to_dict() or request.get_json(force=True)
        print("\n--- NEW SUBMISSION ---")
        for k, v in data.items():
            print(f"{k}: {v}")

        # Save data to CSV
        fieldnames = list(data.keys()) + ["timestamp"]
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(data)

        return jsonify({"status": "success", "message": "Data logged successfully", "data": data})

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
