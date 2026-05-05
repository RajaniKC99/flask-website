from flask import Flask, render_template, request
import datetime
import sqlite3


app = Flask(__name__)

# create database
def init_db():
    with sqlite3.connect("messages.db") as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS messages (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     message TEXT,
                     date TEXT
                     )
                     """)
init_db()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    message = request.form["message"]
    today = str(datetime.datetime.now())

    # save to database
    with sqlite3.connect("messages.db") as conn:
        conn.execute(
            "INSERT INTO messages (name, message, date) VALUES (?, ?, ?)",
            (name, message, today)
        )
    return render_template("thankyou.html", name=name)

@app.route("/messages")
def view_messages():
    with sqlite3.connect("messages.db") as conn:
        messages = conn.execute("SELECT * FROM messages").fetchall()
    return render_template("messages.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True, port=8000) 