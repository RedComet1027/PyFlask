from sqlalchemy import create_engine, text
import psycopg2
import os

# Obtain secrets from environment
USERNAME = os.environ['DB_USER']
PASSWORD = os.environ['DB_PWD']
HOST = os.environ['DB_HOST']
DATABASE = os.environ['DB_NAME']

conn_str = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}?sslmode=require'

engine = create_engine(conn_str)

def save_portfolio_data_to_db(portfolio_name, selected_stocks):
  with engine.connect() as conn:
    query = text("INSERT INTO user_folio (name, stock_tickers) VALUES (:name, :tickers)")
    conn.execute(query, {"name": portfolio_name, "tickers": ','.join(selected_stocks)})
    conn.commit()

def update_portfolio_data_to_db(portfolio_name, selected_stocks):
  with engine.connect() as conn:
    query = text("UPDATE user_folio SET stock_tickers = :tickers WHERE name = :name")
    conn.execute(query, {"name": portfolio_name, "tickers": ','.join(selected_stocks)})
    conn.commit()

def delete_portfolio_from_db(portfolio_name):
  with engine.connect() as conn:
    query = text("DELETE FROM user_folio WHERE name = :name")
    conn.execute(query, {"name": portfolio_name})
    conn.commit()
    
def load_portfolios_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT DISTINCT name FROM user_folio"))
    return [dict(row._mapping) for row in result.all()]

def load_portfolio_stocks_from_db(portfolio_name):
  with engine.connect() as conn:
    # Get the stock IDs for the portfolio
    portfolio = conn.execute(
      text("SELECT stock_tickers FROM user_folio WHERE name = :name"),
      {"name": portfolio_name}
    ).first()
    
    if portfolio:
      stock_ids = [int(id) for id in portfolio[0].split(',')]
      stocks = []
      # Get each stock individually
      for stock_id in stock_ids:
        result = conn.execute(
          text("SELECT * FROM stock WHERE id = :id"),
          {"id": stock_id}
        ).first()
        if result:
          stocks.append(dict(result._mapping))
      return stocks
    return []

def load_stocks_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from stock"))
    # convert row objects to dicts
    result_dicts = []
    for row in result.all():
      result_dicts.append(dict(row._mapping))
    return result_dicts

# for showing single stock by URL: /api/stock/1
def load_stock_from_db(id):
  with engine.connect() as conn:
    # for SQLAchemy less than 2.0
    #result = conn.execute(
    #    text("select * from playing_with_neon where id = :val"), val=id)

    # for SQLAchemy greater than 2.0, all params in dict
    result = conn.execute(text("select * from stock where id = :val"),
                {"val": id})

    stock = result.all()
    if len(stock) == 0:
      # check if result is empty
      return None
    else:
      # convert result (or row) object to a dict
      return dict(stock[0]._mapping)

def save_stock_to_db(name, ticker, price):
  with engine.connect() as conn:
      query = text("INSERT INTO stock (name, ticker, price) VALUES (:name, :ticker, :price)")
      conn.execute(query, {"name": name, "ticker": ticker, "price": float(price)})
      conn.commit()

def update_stock_in_db(stock_id, name, ticker, price):
  with engine.connect() as conn:
      query = text("UPDATE stock SET name = :name, ticker = :ticker, price = :price WHERE id = :id")
      conn.execute(query, {"id": stock_id, "name": name, "ticker": ticker, "price": float(price)})
      conn.commit()