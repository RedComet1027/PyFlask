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
