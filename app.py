from flask import Flask, render_template, jsonify, request, redirect
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
@app.route('/new-portfolio')
def new_portfolio():
    stocks = load_stocks_from_db()
    return render_template('new_portfolio.html', stocks=stocks)

@app.route('/', methods=['POST'])
def save_portfolio():
    # Handle form submission
    portfolio_name = request.form['portfolioName']
    stock_names = request.form.getlist('stockName[]')
    stock_tickers = request.form.getlist('stockTicker[]')
    stock_prices = request.form.getlist('stockPrice[]')
    
    # Here you would save the data to your database
    # For now we'll just redirect back to home
    return redirect('/')


app.run(host='0.0.0.0', port=81)
