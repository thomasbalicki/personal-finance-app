import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_INCOME_TABLE = """
CREATE TABLE IF NOT EXISTS income (
id SERIAL PRIMARY KEY,
amount FLOAT NOT NULL,
source TEXT NOT NULL,
date DATE NOT NULL
);
"""


CREATE_EXPENSES_TABLE = """
CREATE TABLE IF NOT EXISTS expenses (
id SERIAL PRIMARY KEY,
amount FLOAT NOT NULL,
category TEXT NOT NULL,
date DATE NOT NULL
);
"""

INSERT_INCOME = (
    "INSERT INTO income (amount, source, date) VALUES (%s, %s, %s);"
)
INSERT_EXPENSES = (
    "INSERT INTO expenses (amount, category, date) VALUES (%s, %s, %s);"
)

NET_INCOME = """SELECT SUM(amount) as net_income FROM INCOME;"""

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/income")
def ADD_INCOME():
    data = request.get_json()
    amount = data["amount"]
    source = data["source"]
    date = data["date"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_INCOME_TABLE)
            cursor.execute(INSERT_INCOME, (amount, source, date))
            # Check if any rows were inserted
            if cursor.rowcount == 0:
                return {"message": "No rows were inserted."}, 400
            # Fetch the last inserted row's ID
            cursor.execute("SELECT lastval()")
            income_id = cursor.fetchone()[0]
    return {"id": income_id, "message": f"Income of {amount} from {source}, on {date} created."}, 201

@app.post("/api/expenses")
def ADD_INCOME():
    data = request.get_json()
    amount = data["amount"]
    category = data["category"]
    date = data["date"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_EXPENSES_TABLE)
            cursor.execute(INSERT_EXPENSES, (amount, category, date))
            # Check if any rows were inserted
            if cursor.rowcount == 0:
                return {"message": "No rows were inserted."}, 400
            # Fetch the last inserted row's ID
            cursor.execute("SELECT lastval()")
            income_id = cursor.fetchone()[0]
    return {"id": income_id, "message": f"Expense of {amount} from {category}, on {date} created."}, 201
