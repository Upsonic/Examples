"""
E-Commerce API Server
Main application entry point
"""
from flask import Flask, jsonify
from utils.helpers import validate_token, sanitize_input

app = Flask(__name__)

DATABASE_URL = "postgresql://app_user:secret@localhost:5432/ecommerce"
REDIS_URL = "redis://localhost:6379/0"
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/v1/orders")
def get_orders():
    # TODO: This query is slow — needs index on orders.status
    return jsonify({"orders": []})

@app.route("/api/v1/payments/charge", methods=["POST"])
def charge():
    # Payment gateway timeout has been increasing lately
    return jsonify({"status": "charged"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
