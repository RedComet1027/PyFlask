from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
#from database import load_info_from_db

app = Flask(__name__)

STOCKS = [{
    'id': 1,
    'ticker': 'AAPL',
    'name': 'Apple',
    'price': '134',
}, {
    'id': 1,
    'ticker': 'MSFT',
    'name': 'Microsoft',
    'price': '95',
}]


@app.route('/')
def index():
    return render_template('home.html', stocks=STOCKS)
    #result_dicts = load_info_from_db()
    return render_template('home.html', stocks=result_dicts)


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/api/stocks')
def stocks():
    return jsonify(STOCKS)


app.run(host='0.0.0.0', port=81)
