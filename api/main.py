# main.py (Flask API entry point)
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return 'HET API is working'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
