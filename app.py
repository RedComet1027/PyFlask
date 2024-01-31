from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import load_stocks_from_db, load_stock_from_db

app = Flask(__name__)


@app.route('/')
def index():
    result_dicts = load_stocks_from_db()
    return render_template('home.html', stocks=result_dicts)


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/api/stock/<id>')
def show_stock(id):
    stock = load_stock_from_db(id)
    return jsonify(stock)


app.run(host='0.0.0.0', port=81)
