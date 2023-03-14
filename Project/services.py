import os

import json
import requests
import sqlite3
from uuid import uuid4
from . import app
from . import secrets

from flask import redirect, session, url_for
from functools import wraps

app.secret_key = secrets.secret_key


def cmc_info(symbol):
    """Call the CoinMarketCap API to get info for crypto symbol"""

    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info"
    parameters = {
        'symbol': symbol
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': secrets.api_key,
    }    
    session = requests.Session()
    session.headers.update(headers)

    # Contact API
    try:
        response = session.get(url, params=parameters)
    except requests.RequestException:
        return None
    
    # Parse response
    try:
        data = json.loads(response.text)
        return data
    except (KeyError, TypeError, ValueError):
        print("Error")
        return None


def cmc_quote(symbol):
    """Call the CoinMarketCap API to get quotes for crypto symbol"""

    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameters = {
        'symbol': symbol
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': secrets.api_key,
    }    
    session = requests.Session()
    session.headers.update(headers)

    # Contact API
    try:
        response = session.get(url, params=parameters)
    except requests.RequestException:
        return None
    
    # Parse response
    try:
        data = json.loads(response.text)
        return data
    except (KeyError, TypeError, ValueError):
        print("Error")
        return None
    

def combine_op(db, quote):
    """Use database and quote from api to create combined data"""
    money_invested = 0
    actual_value = 0
    gain = 0

    for row in db:
        money_invested += row["price"]
        actual_value += row["quantity"] * quote["data"][row["coin"]][0]["quote"]["USD"]["price"]
    gain = actual_value - money_invested

    combined_data = {'invested': money_invested, 
                        'value': actual_value,
                        'gain': gain}
    return combined_data


def db_required(f):
    """
    Decorate routes to require database setup.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/create")
        return f(*args, **kwargs)
    return decorated_function


def delete_db():
    """Delete all user's informations from database"""
    # Delete from database
    query = "DELETE FROM usersdb WHERE user = ?"
    sqlite_op(query, (session["user_id"],))
    session.pop("user_id", None)
    # Delete downloaded file if there is one
    if os.path.exists(r"static\files\database.json"):
        os.remove(r"static\files\database.json")    


def display_db():
    """Query the database to return a list of dict of user assets"""
    query = "SELECT * FROM usersdb WHERE user = ? ORDER BY id desc"
    result = sqlite_op(query, (session.get("user_id"),))
    # Create a list of dict containing results from the query
    db = []
    for row in result:
        db.append({'id': row[0], 
                    'user': row[1], 
                    'coin': row[2], 
                    'quantity': row[3], 
                    'price': row[4], 
                    'date': row[5], 
                    'service': row[6]
                    })
    return db


def download_db():
    """Create a JSON file of user's assets and download it"""
    # Create the database to download
    db = display_db()
    with open(r"static\files\database.json", "w") as download_file:
        json.dump(db, download_file)
        download_file.close()


def get_info():
    """Call the API to get info of user assets symbol from database"""

    # Query the database to get user assets
    db = display_db()

    # Get each unique coin symbol from db
    symbol = []
    for row in db:
        if row["coin"] not in symbol:
            symbol.append(str(row["coin"]).upper())

    # Call the api with this coin symbol
    info = cmc_info(str(str(str(str(symbol).replace(" ","")).replace("[","")).replace("]","")).replace("'",""))
    return info


def get_quote():
    """Call the API to get quotes of user assets symbol from database"""

    # Query the database to get user assets
    db = display_db()

    # Get each unique coin symbol from db
    symbol = []
    for row in db:
        if row["coin"] not in symbol:
            symbol.append(str(row["coin"]).upper())

    # Call the api with this coin symbol
    quote = cmc_quote(str(str(str(str(symbol).replace(" ","")).replace("[","")).replace("]","")).replace("'",""))
    return quote


def group_op(db):
    """Use database to create grouped data, summing data about same coin"""
    grouped_data = []
    for row in db:
        if not grouped_data:
            grouped_data.append({'coin': row['coin'],
                                 'quantity': row["quantity"],
                                 'price': row["price"]
                                 })
        else:
            for coin in grouped_data:
                updated = False
                if coin['coin'] == row['coin']:
                    coin['quantity'] = coin['quantity'] + row['quantity']
                    coin['price'] = coin['price'] + row['price']
                    updated = True
                    break
            if not updated:
                grouped_data.append({'coin': row['coin'],
                                    'quantity': row["quantity"],
                                    'price': row["price"]
                                    })
    return grouped_data                   


def input_test(responses):
    """Realize tests for the user input"""
    try:
        # Realize tests for the id input
        if responses["id"]:
            query = "SELECT user FROM usersdb WHERE id = ?"
            result = sqlite_op(query, (responses["id"],))
            if result[0][0] != session.get("user_id"):
                return True

        # Realize tests for the coin input
        if not str(responses["coin"]).isalpha():
            return True
        symbol = str(responses["coin"]).upper()
        quote = cmc_quote(symbol)
        if not quote['data'][symbol]:
            return True
        
        # Realize tests for the quantity input
        if responses["id"] and float(responses["quantity"]) < 0:
            return True
        if not responses["id"] and float(responses["quantity"]) <= 0:
            return True

        # Realize tests for the price input
        if responses["price"]:
            if float(responses["price"]) < 0:
                return True

        # Realize tests for the service input
        if responses["service"]:
            if not str(responses["service"]).isalnum():
                return True
            
    except (KeyError, ValueError, TypeError):
        return True
        

def message_to_display(msg):
    # Different message to display with the rendering template message
    if msg == "delete":
        message = "Your database was sucessfuly deleted."
        return message

    if msg == "error":
        message = "Error occured during operations, please retry."
        return message
    
    if msg == "upload":
        message = "Error occured during operations, no/wrong file uploaded."
    
    if msg == "input":
        message = "Error occured during operations, wrong data submitted when creating / updating database."
        return message


def set_user():
    """Create a random user id to store in db"""
    session["user_id"] = str(uuid4())  


def sqlite_op(query, params):
    """Call sqlite to perform operations on database based on query arg"""
    try:
        sqliteConnection = sqlite3.connect('assetsmanager.db')
        cursor = sqliteConnection.cursor()
        cursor.execute(query, params)
        sqliteConnection.commit()
        result = cursor.fetchall()
        cursor.close()
        return result
    except sqlite3.Error as error:
        print('Error occured - ', error)
        return redirect(url_for('index'))
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def update_db(responses):
    """Use request inputs to create or update a row in the database"""

    responses["coin"] = str(responses["coin"]).upper()

    # If no price input, call the api to get the current price
    if not responses["price"]:
        quote = cmc_quote(responses["coin"])
        responses["price"] = float(responses["quantity"]) * float(quote["data"][responses["coin"]][0]["quote"]["USD"]["price"])

    # create a new row
    if not responses["id"]:
        if responses["date"]:
            query = "INSERT INTO usersdb (user, coin, quantity, price, date, service) VALUES (?, ?, ?, ?, ?, ?)"
            params = (session["user_id"],
                    responses["coin"],
                    responses["quantity"],
                    responses["price"],
                    responses["date"],
                    responses["service"]
                    )
        else:
            query = "INSERT INTO usersdb (user, coin, quantity, price, service) VALUES (?, ?, ?, ?, ?)"
            params = (session["user_id"],
                    responses["coin"],
                    responses["quantity"],
                    responses["price"],
                    responses["service"]
                    )
        sqlite_op(query, params)

    # update a row
    if responses["id"]:
        query = "UPDATE usersdb SET coin = ?, quantity = ?, price = ?, date = ?, service = ? WHERE id = ?"
        params = (responses["coin"],
                  responses["quantity"],
                  responses["price"],
                  responses["date"],
                  responses["service"],
                  responses["id"]
                  )
        sqlite_op(query, params)
        
    # delete a row
    if responses["id"] and (responses["quantity"] == "0"):
        query = "DELETE FROM usersdb WHERE id = ?"
        sqlite_op(query, (responses["id"],))


def upload_db():
    """Import the users assets from the uploaded file into the database"""
    # Open the uploaded file
    with open(r"static\files\import.json", "r") as uploaded_file:
        data = json.load(uploaded_file)
        uploaded_file.close()
    # Check user's information are deleted before adding informations in database
    query = "SELECT user FROM usersdb WHERE user = ?"
    existing_user = sqlite_op(query, (data[0]["user"],))
    if existing_user:
        query = "DELETE FROM usersdb WHERE user = ?"
        sqlite_op(query, (existing_user,))
    # Insert into the database each row from the file
    try:
        for row in data:
            query = "INSERT INTO usersdb (user, coin, quantity, price, date, service) VALUES (?, ?, ?, ?, ?, ?)"
            params = (row["user"],
                    row["coin"],
                    row["quantity"],
                    row["price"],
                    row["date"],
                    row["service"]
                    )
            sqlite_op(query, params)
    except (KeyError, ValueError, TypeError, IndexError):
        print('Error')
        return redirect(url_for('index'))
    finally:
        session["user_id"] = data[0]["user"]
        os.remove(r"static\files\import.json")


def usd(value):
    """Format value as USD"""
    return f"${value:,.2f}"