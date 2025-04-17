from flask import Flask, render_template, send_from_directory, request, jsonify
import json

app = Flask(__name__)

# your existing routes
@app.route('/')
def index():
    return render_template('ar_navigator.html')

@app.route('/scenes.json')
def scenes_route():
    return send_from_directory('static', 'scenes.json')

# new direct-route API: simply returns [startScene, endScene]
@app.route('/api/route')
def api_route():
    # indices come from dropdown values
    start_idx = int(request.args.get('from', 0))
    end_idx   = int(request.args.get('to',   0))
    with open('static/scenes.json') as f:
        scenes = json.load(f)
    # clamp indices
    start = scenes[start_idx] if 0 <= start_idx < len(scenes) else scenes[0]
    end   = scenes[end_idx]   if 0 <= end_idx   < len(scenes) else scenes[0]
    return jsonify([start, end])

if __name__ == '__main__':
    app.run(debug=True)
