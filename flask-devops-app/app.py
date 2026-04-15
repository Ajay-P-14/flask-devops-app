from flask import Flask, jsonify
import logging
import os

# ── App Setup ────────────────────────────────────────────────
app = Flask(__name__)

# Logging config (shows in Jenkins console + kubectl logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ── Routes ───────────────────────────────────────────────────

@app.route("/")
def home():
    logger.info("Home endpoint hit")
    return jsonify({
        "message": "Hello from Ajay DevOps Project",
        "status":  "running"
    }), 200


@app.route("/health")
def health():
    logger.info("Health check endpoint hit")
    return jsonify({
        "status":  "healthy",
        "service": "flask-devops-app"
    }), 200


@app.route("/info")
def info():
    logger.info("Info endpoint hit")
    return jsonify({
        "app":         "flask-devops-app",
        "author":      "Ajay",
        "version":     os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("APP_ENV", "production")
    }), 200


# ── Error Handlers ───────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 - Route not found: {e}")
    return jsonify({
        "error":   "Route not found",
        "status":  404
    }), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 - Internal server error: {e}")
    return jsonify({
        "error":  "Internal server error",
        "status": 500
    }), 500


# ── Entry Point ──────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    logger.info(f"Starting Flask app on port {port} | debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)
