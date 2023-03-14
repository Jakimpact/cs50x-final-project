import os

from flask import redirect, render_template, request, url_for
from . import app
from . import services

UPLOAD_FOLDER = r'static\files'
ALLOWED_EXTENSIONS = {'json'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Custom filter
app.jinja_env.filters["usd"] = services.usd


def allowed_file(filename):
    return '.' in filename and \
            str(filename).rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    # Show the home page of the website
    return render_template("index.html")


@app.route("/create", methods=['GET', 'POST'])
def create_db():
    # From POST request, get the input to create the database
    if request.method == 'POST':
        responses = {'id': request.form.get("type"), 
                     'coin': request.form.get("coin"), 
                     'quantity': request.form.get("quantity"), 
                     'price': request.form.get("price"), 
                     'date': request.form.get("date"), 
                     'service': request.form.get("service")
                    }
        # Test inputs, true return means error 
        if services.input_test(responses):
            return render_template("message.html", message=services.message_to_display("input"))
        else:
            services.set_user()
            services.update_db(responses)
            return render_template("update.html", db=services.display_db())
        
    # From GET request, display page for creating the first row of the user database
    else:
        return render_template("create.html")


@app.route("/delete", methods=['GET', 'POST'])
@services.db_required
def delete_db():
    # From POST method, delete the database
    if request.method == 'POST':
        if request.form.get("answer") == "yes":
            services.delete_db()
            return render_template("message.html", message=services.message_to_display("delete"))
        else:
            return redirect(url_for('index'))

    # From GET method, ask the user to confirm delete
    else:
        return render_template("delete.html")


@app.route("/download")
@services.db_required
def download_db():    
    # FROM GET method, create a database.json that user can download
    services.download_db()
    return render_template("download.html")


@app.route("/table")
@services.db_required
def table():
    # Show different tables using the user database
    db = services.display_db()
    quote = services.get_quote()
    info = services.get_info()
    grouped_data = services.group_op(db)
    combined_data = services.combine_op(db, quote)
    return render_template("table.html", db=db, quote=quote, info=info, grouped_data=grouped_data, combined_data=combined_data)


@app.route("/update", methods=['GET', 'POST'])
@services.db_required
def update_db():
    # From POST request, get the update input
    if request.method == 'POST':
        responses = {'id': request.form.get("type"), 
                     'coin': request.form.get("coin"), 
                     'quantity': request.form.get("quantity"), 
                     'price': request.form.get("price"), 
                     'date': request.form.get("date"), 
                     'service': request.form.get("service")
                    }
        # Test inputs, true return means error 
        if services.input_test(responses):
            return render_template("message.html", message=services.message_to_display("input"))
        else:
            services.update_db(responses)
            return render_template("update.html", db=services.display_db())
    
    # From GET request, show the user's database 
    else:
        return render_template("update.html", db=services.display_db())
    

@app.route("/upload", methods=['GET', 'POST'])
def upload_db():
    # From POST request, upload the database and redirect to update
    if request.method == 'POST':
        # Check there is a file
        if ('database' not in request.files) or (request.files['database'].filename == ''):
            return render_template('message.html', message=services.message_to_display("upload"))
        # Check the file is a json file
        if request.files['database'] and allowed_file(request.files['database'].filename):
            request.files['database'].save(os.path.join(app.config['UPLOAD_FOLDER'], 'import.json'))
            services.upload_db()
            return redirect(url_for('update_db'))
        else:
            return render_template('message.html', message=services.message_to_display("upload"))

    # From GET request, ask the user to upload a database
    else:
        return render_template("upload.html")