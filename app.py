from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from database import load_stocks_from_db, load_stock_from_db, save_portfolio_to_db

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


# obtain new portfolio via Post from html FORM
@app.route('/portfolio/create', methods=['post'])
def create_portfolio():
    # get FORM data from request
    data = request.form
    # store data in database
    save_portfolio_to_db(data)
    # return for debug
    return jsonify(data)


app.run(host='0.0.0.0', port=81)
