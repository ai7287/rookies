# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vuln')
def vuln():
    user_input = request.args.get('check', '')
    sanitized_input = user_input.replace('<', '&lt;').replace('>', '&gt;')
    return render_template('vuln.html', user_input = sanitized_input)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)