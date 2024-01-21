# Crypto Assets Database

## **Website Demo:** https://Jakimpact.eu.pythonanywhere.com

## **Purpose of the project:**

One of the special features of crypto assets is the wide variety of way you can buy them, but also hold them. Whether you use an exchange, a web-based or a physical wallet, it is sometimes difficult to keep track of all these assets spread over these services allowing for their conservation.

The project's goal is to create a webapp that provide tools to create a crypto assets database,
displaying this assets in various tables offering statistics on these assets and an overall portfolio.

This webapp also allows to download the database created and to import it later in order to update it.

## **Configuration:**

To run the project you need to install libraries and packages listed in the file **requirements.txt**.

You also need to setup the file **secrets.py** by :

- creating a new secret key (eg:  `secret_key = "your_secret_key"` )
- creating a free account [on CoinMarketCap](https://pro.coinmarketcap.com/signup/) to get an API key, and putting it in **secrets.py** (eg: `api_key = “your_api_key”` )

If you run this project on another code editor than VSCode and a windows machine, you need to do some changes in files listed below : 

- in **webapp.py**, **views.py** and **services.py** :
    - remplace `from . import “files”` by `import “files”` where “files” is the name of right after import
- in **views.py** and **services.py** :
    - remplace any `\` by `/` except for the one in file **views.py** in `def allowed_file(filename):`

## **Files description:**

### **HTML files (templates folder):**

**create.html**:
It contains a table with a form to create a new user entry in database.

**delete.html**:
It contains a form to delete all rows of user in database.

**download.html**:
It contains a button to download a json file of all user's row from database.

**index.html**:
It contains paragraph to present purpose of this webapp and images to illustrate it.

**layout.html**:
Layout of other files. It contains head with import of bootstrap CSS, navigation bar and the footer.

**message.html**:
A file to display various messages.

**table.html**:
It contains three tables of user's row from database and corresponding informations from CoinMarketCap through api. The first table displays rows as they were inputed. The second table displays regrouped informations from same row's coin. The third table displays overall informations of user's row.

**update.html**:
It contains a table with a form in first row to create a new row for an existing user in database and below all user's row that can be updated.

**upload.html**:
It contains a form where user can upload a json file previously downloaded.

### **Javascript file (static folder):**

**myScript.js**:
This javascript is only loaded in the **table.html** file.

The first function is a DOMContentLoaded that will look for each value attribute from table rows with `class="gain"`. If the value is negative the color of the element will be set to red, if the value is positive, it will be set to green.

The `function sortTable1(n)` is adapted from a tutorial found on https://www.w3schools.com/howto/howto_js_sort_table.asp. This function allows users to sort first table from **table.html** by clicking on headers. It's a for loop nested in a while loop where the value of `row[i]` of column clicked will be compared to value of `row[i+1]` and switched if value of `row[i]` is lower or upper depending if dir is on asc or desc.

The `function sortTable2(n)` is the same function for second table of **table.html**.

### **SQL database:**

**assetsmanager.db** is a SQL database used for this project that contains one table named **usersdb**. This table contains seven columns, five of them (coin symbol, quantity, price, date and service) are input asked to user in **create.html** and **update.html**, the two other (id and user) are created by python files to identify users and row.

### **Python files:**

**__init__.py**:
This file initialize the flask app.

**secrets.py**:
This file contains `secret_key` needed for use of flask session and `api_key` which is needed to call the CoinMarketCap API.

**services.py**:
This file contains all the logic, operations, database operations and API calling. On top of the file there are the import of flask functions, python files and libraries and packages.

`def cmc_info(symbol)` is a function that call CoinMarketCap API to get info for the parameter `symbol` and return data if the API call worked.

`def cmc_quote(symbol)` is a function that call CoinMarketCap API to get quote for the parameter `symbol` and return data if the API call worked.

`def combine_op(db, quote)` is a function that get `db` (all user's rows) and `quote` (API data associated to theses rows) parameters to create overall data for a user. It will use these two parameters in a for loop to create and return a dict that contains the total money invested, the current value and the gain. 

`def db_required(f)` is a decorator function used in **views.py** that checks if the `session["user_id"]` is set. If the user try to access a route that uses this decorator without having a `session["user_id"]`, it will redirect the user to **create.html**.

`def delete_db()` is a function that deletes all rows from **usersdb** where user is `session["user_id"]` by calling `sqlite_op(query, params)`, resets `session["user_id"]` and if existing, removes `"database.json"` from `"static\files"`.

`def display_db()` is a function that get all rows from **usersdb** where user is `session["user_id"]` in `result` by calling `sqlite_op(query, params)`. Then it creates a list of dict for all rows in `result` and returns it.

`def download_db()` is a function that calls `display_db()` to get `db`, creates a new file `"database.json"` in `"static\files`, opens it and writes `db` in it.

`def get_info()` is a function that calls `display_db()` to get `db`, creates a list of unique coin symbol from `db` and calls `cmc_info(symbol)` with this list to get info and returns it.

`def get_quote()` is a function that calls `display_db()` to get `db`, creates a list of unique coin symbol from `db` and calls `cmc_quote(symbol)` with this list to get quote and returns it.

`def group_op(db)` is a function that get `db` (all user's rows) parameter to create grouped data for unique user's coin. It creates a list, in a for loop it looks if there is the coin symbol from row `db` in the list, if not it appends the row as a dict. Otherwise it adds the numeric value from row `db` in the list for the corresponding coin. Then it return the list.

`def input_test(responses)` is a function that get `responses` parameter and checks the different inputs. 
It checks `responses["id"]` by calling `sqlite_op(query, params)`, if the `responses["id"]` is not in **usersdb** it returns true. 
It checks `responses["coin"]`, if it's not alphabetic or nothing come back by calling `cmc_quote(symbol)` it returns true. 
It checks `responses["quantity"]`, if it's not a float it returns true.
It checks `responses["price"]`, if it's not a float it returns true.
It checks `responses["service"]`, if it's not alphanumeric it returns true. 

`def message_to_display(msg)` is a function a get a `msg` parameters and returns a different message depending on the `msg` parameter.

`def set_user()` is a function that creates a new `session["user_id"]` by using `uuid4()`.

`def sqlite_op(query, params)` is a function that get `query` and `params` parameters, connects to **assetsmanager.db** with sqlite and executes an operation with `query` and `params` and returns the result.

`def update_db(responses)` is a function that get `responses` parameters, if there is no `responses["price"]`, it calls `cmc_quote(symbol)` to get a `quote` and set the `responses["price"]` to be price from `quote`. Then it calls `sqlite_op(query, params)` to insert into **usersdb** the `responses` if there is no `responses["id"]`. Otherwise it updates **usersdb** with the `reponses` by calling `sqlite_op(query, params)`. If the `responses["quantity"]` is set to zero, it calls `sqlite_op(query, params)` to delete the row.

`def upload_db()` is a function that open a file `"import.json"` from `"static\files"` and read the file into `data`. Then it checks if the user form `data` is in **usersdb** by calling `sqlite_op(query, params)`, if there is calls `sqlite_op(query, params)` to delete all rows for user `data`. After that it calls the `sqlite_op(query, params)` to inserts `data` in **usersdb** row by row. Finally it removes the `import.json` and set the `session["user_id"]` to be user from `data`.

`def usd(value)` is a function that get a `value` parameter and formats `value` as USD.

**views.py**:
This file contains all side-effects of setting up routes for the application. On top of the file there are the import of flask functions and python files. Then we set the upload folder to be `static\files`. 

`def allowed_file(filename)` is a function that checks if the extension of files that users upload is json.

`def index()` returns **index.html**.

`def create_db()` returns **create.html** when the route method is `GET`. When it's `POST`, it gets the users inputs from form into `responses`, submitting them to `input_test(responses)` in **services.py**. If there is no error in inputs it calls `set_user()` and `update_db(responses)` with user's inputs in **services.py** and renders **update.html** with database updated from `display_db()` in **services.py**. Otherwise it renders an input error message with **message.html**.

`def delete_db()` returns **delete.html** when the route method is `GET`. When it's `POST`, it cheked if the input from user is a `"yes"`, if so it calls `delete_db()` in **services.py** and renders a delete message with **message.html**. Otherwise it redirect to homepage.

`def download_db()` call `download_db()` in services.py and renders **download.html**.

`def table()` call `display_db()`, `get_quote()`, `get_info()`, `group_op(db)` and `combine_op(db, quote)` in **services.py** to get data and s **table.html** with these data.

`def update_db()` returns **update.html** when the route method is `GET`. When it's `POST`, it gets the users inputs from form into `responses`, submitting them to `input_test(responses)` in **services.py**. If there is no error in inputs it calls `update_db(responses)` with user's inputs in **services.py** and renders **update.html** with database updated from `display_db()` in **services.py**. Otherwise it will renders an input error message with **message.html**.

`def upload_db()` returns **upload.html** when the route method is `GET`. When it's `POST`, it checks that a file is uploaded and call `allowed_file(filename)`, if there is no error it saves the file in the upload folder as `import.json`, call `upload_db()` in **services.py** and renders **update.html** with database updated from `display_db()` in **services.py**. Otherwise it renders a message with **message.html**.

**webapp.py**:
This file is the entry point for the application and import the other python files needed to run the application.
