from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    # your AR HTML (renamed to ar_navigator.html or routes.html)
    return render_template('ar_navigator.html')

# Serve the precomputed routes JSON at /destination_routes.json
@app.route('/destination_routes.json')
def destination_routes():
    return send_from_directory(app.static_folder, 'destination_routes.json')

# (Optional) if you reference any other top‑level JSON directly:
@app.route('/<path:filename>.json')
def serve_json(filename):
    # this lets you do /scenes.json or /any_other.json if needed
    path = f"{filename}.json"
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
