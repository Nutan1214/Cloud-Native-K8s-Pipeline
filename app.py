from flask import Flask, jsonify
import os
import time
from prometheus_client import start_http_server, Counter, Summary

app = Flask(__name__)

# Metrics for Prometheus
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests to the app')
REQUEST_LATENCY = Summary('app_request_latency_seconds', 'Time spent processing request')

@app.route('/')
@REQUEST_LATENCY.time()
def home():
    REQUEST_COUNT.inc()
    # Pulls from an environment variable (Testing Kubernetes ConfigMaps)
    env_message = os.getenv("APP_MESSAGE", "Welcome to the Cloud-Native App!")
    return jsonify({
        "status": "Success",
        "message": env_message,
        "timestamp": time.time()
    })

# Liveness Probe: Tells K8s if the app is alive
@app.route('/health')
def health():
    return jsonify({"status": "UP"}), 200

# Readiness Probe: Tells K8s if the app is ready for traffic
@app.route('/ready')
def ready():
    return jsonify({"status": "READY"}), 200

if __name__ == '__main__':
    # Start Prometheus metrics on port 8000
    start_http_server(8000)
    # Run Flask app on port 5000
    app.run(host='0.0.0.0', port=5000)
