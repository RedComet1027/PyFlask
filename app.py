import yfinance as yf

from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy

from database import *

app = Flask(__name__)

@app.route('/')
def index():
  # result_dicts = load_stocks_from_db()
  # return render_template('home.html', stocks=result_dicts)
  stocks = load_stocks_from_db()
  for stock in stocks:
    ticker = stock['ticker']
    try:
      yf_stock = yf.Ticker(ticker)
      latest_price = yf_stock.info.get('regularMarketPrice')
      if latest_price is not None:
        stock['price'] = latest_price
    except Exception as e:
      # If API fails, keep DB price
      pass
  return render_template('home.html', stocks=stocks)

@app.route('/hello')
def hello():
  return 'Hello, World!'

@app.route('/api/stock/<id>')
def show_stock(id):
  stock = load_stock_from_db(id)
  return jsonify(stock)

@app.route('/new-portfolio')
def new_portfolio():
  stocks = load_stocks_from_db()
  return render_template('new_portfolio.html', stocks=stocks)


@app.route('/save-portfolio', methods=['POST'])
def save_portfolio():
  portfolio_name = request.form['portfolioName']
  selected_stocks = request.form.getlist('selectedStocks')
  save_portfolio_data_to_db(portfolio_name, selected_stocks)
  return redirect('/')

@app.route('/list-portfolio')
def list_portfolio():
  portfolios = load_portfolios_from_db()
  return render_template('list_portfolio.html', portfolios=portfolios)

@app.route('/edit-portfolio')
def edit_portfolio():
  portfolio_name = request.args.get('name')
  portfolio_stocks = load_portfolio_stocks_from_db(portfolio_name)
  stocks = load_stocks_from_db()

  selected_stock_ids = {str(stock['id']) for stock in portfolio_stocks}
  return render_template('edit_portfolio.html', 
         portfolio_name=portfolio_name, 
         stocks=stocks,
         selected_stock_ids=selected_stock_ids)

@app.route('/update-portfolio', methods=['POST'])
def update_portfolio():
  portfolio_name = request.form['portfolioName']
  selected_stocks = request.form.getlist('selectedStocks')
  
  update_portfolio_data_to_db(portfolio_name, selected_stocks)
  
  return redirect('/list-portfolio')  # Redirect back to the list portfolio page

@app.route('/delete-portfolio')
def delete_portfolio():
  portfolio_name = request.args.get('name')
  delete_portfolio_from_db(portfolio_name)
  
  return redirect('/list-portfolio')  # Redirect back to the list portfolio page
  
@app.route('/api/portfolio/<portfolio_name>/stocks')
def get_portfolio_stocks(portfolio_name):
  stocks = load_portfolio_stocks_from_db(portfolio_name)
  return jsonify(stocks)

@app.route('/list-stock')
def list_stock():
  stocks = load_stocks_from_db()
  # Fetch latest price for each stock
  for stock in stocks:
    ticker = stock['ticker']
    try:
      yf_stock = yf.Ticker(ticker)
      latest_price = yf_stock.info.get('regularMarketPrice')
      stock['latest_price'] = latest_price if latest_price is not None else "N/A"
    except Exception:
      stock['latest_price'] = "N/A"
  return render_template('list_stock.html', stocks=stocks)

@app.route('/new-stock')
def new_stock():
  return render_template('new_stock.html')

@app.route('/save-stock', methods=['POST'])
def save_stock():
  name = request.form['stockName']
  ticker = request.form['stockTicker']
  price = "0" # default price for all stocks
  save_stock_to_db(name, ticker, price)
  return redirect('/list-stock')
  
@app.route('/edit-stock/<int:stock_id>', methods=['GET', 'POST'])
def edit_stock(stock_id):
    if request.method == 'GET':
        stock = load_stock_from_db(stock_id)
        if not stock:
            return "Stock not found", 404
        return render_template('edit_stock.html', stock=stock)
    else:
        name = request.form['stockName']
        ticker = request.form['stockTicker']
        price = "0" # default price for all stocks
        update_stock_in_db(stock_id, name, ticker, price)
        return redirect('/list-stock')
      
@app.route('/delete-stock/<int:stock_id>', methods=['GET', 'POST'])
def delete_stock(stock_id):
    # On GET, check if this stock is in any portfolio
    if request.method == 'GET':
        portfolios = find_portfolios_with_stock(stock_id)
        if portfolios:
            # Show confirmation page with warning
            stock = load_stock_from_db(stock_id)
            return render_template('confirm_delete_stock.html', stock=stock, portfolios=portfolios)
        else:
            # If not in any portfolio, delete directly
            delete_stock_from_db(stock_id)
            return redirect('/list-stock')
    else:
        # POST: User confirmed deletion, delete and redirect
        delete_stock_from_db(stock_id)
        return redirect('/list-stock')

app.run(host='0.0.0.0', port=81)
