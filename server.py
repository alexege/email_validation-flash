from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

app = Flask(__name__)
app.secret_key = "My Super Secret Key"

# Landing page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=["POST"])
def add_email():
    if not EMAIL_REGEX.match(request.form['email_entry']):
        flash("Invalid email address")
    else:
        flash("THank you for valid email address")
        db = connectToMySQL('email_validation')
        query = "INSERT INTO email_validation (email) VALUES (%(email)s);"
        data = {
            'email' : request.form['email_entry']
        }
        val = db.query_db(query, data)
        print("__VAL__")
        print(val)
        return redirect('/success')
    return redirect("/")

@app.route("/success")
def success():
    db = connectToMySQL('email_validation')
    query = "SELECT * FROM email_validation"
    users = db.query_db(query)
    print("____USERS____")
    print(users)
    return render_template("success.html", all_users=users)

if __name__=="__main__":
    app.run(debug=True)