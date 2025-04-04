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

@app.route('/save-portfolio', methods=['POST'])
def save_portfolio():
    portfolio_name = request.form['portfolioName']
    selected_stocks = request.form.getlist('selectedStocks')
    
    with engine.connect() as conn:
        # Insert into user_folio table
        query = text("INSERT INTO user_folio (name, stock_tickers) VALUES (:name, :tickers)")
        conn.execute(query, {"name": portfolio_name, "tickers": ','.join(selected_stocks)})
        conn.commit()
    
    return redirect('/')


app.run(host='0.0.0.0', port=81)
