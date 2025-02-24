# To view this app: https://bishs-services-f22217090ef6.herokuapp.com/
# ** Disclaimer - This application is for experimentation and demonstration /n
# purposes only. It is not intended for official use. Although labeled as a /n
# project for Bish's, it is solely a showcase of my development skills and /n
# should not be considered an official Bish's product. **
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# Configure Flask-Mail server
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # server address
app.config["MAIL_PORT"] = 587  # server port
app.config["MAIL_USE_TLS"] = (
    True  # enable TLS encryption, this makes the communication secure
)
app.config["MAIL_USERNAME"] = "rhettpoole.20@gmail.com"
app.config["MAIL_PASSWORD"] = "zron snjn lyjm xtpy"  # app password for gmail account

# Configure SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # database URI, SQLite - https://www.sqlite.org/docs.html
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # disable tracking modifications

mail = Mail(app)
db = SQLAlchemy(app)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send_email", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    # Create email message
    msg = Message(
        "New Form Submission",
        sender="rhettpoole.20@gmail.com",
        recipients=["rhettpoole.20@gmail.com"],
    )  # Replace with the recipient's email
    msg.body = f"Name: {name}\Phone Number\nEmail: {email}\nMessage: {message}"

    # Send the email
    mail.send(msg)

    # Need to add submission to database functionality at some point.


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
