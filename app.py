from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ar_navigator.html')

@app.route('/scenes.json')
def scenes():
    return send_from_directory('static', 'scenes.json')

if __name__ == '__main__':
    app.run(debug=True)
