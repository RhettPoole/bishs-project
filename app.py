# To view this app: https://bishs-services-f22217090ef6.herokuapp.com/
# ** Disclaimer - This application is for experimentation and demonstration /n
# purposes only. It is not intended for official use. Although labeled as a /n
# project for Bish's, it is solely a showcase of my development skills and /n
# should not be considered an official Bish's product. **

#FLASK Framework
from flask import Flask, render_template, request, redirect, url_for, jsonify

#Email
from flask_mail import Mail, Message

#Database
from flask_sqlalchemy import SQLAlchemy

# .env file management so we can hide info on GitHub - https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

#Local file management, also allows for Heroku to find port numbers so it can use it as an environment variable
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Flask-Mail server using environment variables which were assigned in the .env file
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == 'True'
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

# Configure SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/test.db"  # database URI - SQLite - https://www.sqlite.org/docs.html -> https://sqliteviewer.app/
# Also look at DOCKER (For virtal machines), and Postgres - Mike/Bryan brought these up as tools to study for database integration/management.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # disable tracking modifications

mail = Mail(app)
db = SQLAlchemy(app)

# Set data types for our tables in the database
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)


# Allows us to create new tables in the database
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    # When running this app, it will render the index.html file
    return render_template("index.html")


@app.route("/send_email", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    # Create email message
    msg = Message(
        "New Form Submission",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[os.getenv("MAIL_USERNAME")],
    )  # Replace with the recipient's email
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    # Send the email
    mail.send(msg)

    #Save the submission to the database
    new_submission = Submission(name=name, email=email, message=message)
    db.session.add(new_submission)
    db.session.commit()

    # "Refresh" app after submitting the form
    return redirect(url_for("index"))

''' 
***********************
START SR_TRACKER LOGIC - GET
***********************
'''

repair_orders = {
    '86874': {'name': 'Poole', 'status': 'In Progress', 'details': 'Waiting on parts', 'writer': 'Brett Murdock', 'phone': '208-538-1043'},        
    '86875': {'name': 'Blair Leavitt', 'status': 'Completed', 'details': 'Ready for pickup', 'writer': 'Thomas Murdock', 'phone': '208-538-1044'}
} 

# Define route for sr_tracker and render the form before delivering data to customer.
@app.route("/sr_tracker")
def sr_tracker():
    return render_template("sr_tracker.html")

# Define new route for GET function.
@app.route('/handle_get', methods=['GET'])
# If sr_name and sr_number exist as key:value pairs, display welcome message, if not display !exist message.
def handle_get():
    if request.method =='GET':
        sr_name = request.args['sr_name']
        sr_number = request.args['sr_number']
        print(sr_name, sr_number)
        order = repair_orders.get(sr_number)
        if order and order['name'] == sr_name:
            return render_template("sr_details.html", order=order)
        else: return render_template("sr_tracker.html", error="That Service Request does not exist.")
    else:
        return render_template("sr_tracker.html")
    
''' 
***********************
START CREATE_SR LOGIC - POST
***********************
'''

# Add a new service request / create an RO.
@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        new_sr = request.json
        # Get the first key and value from the JSON
        sr_number, order_data = next(iter(new_sr.items()))
        repair_orders[sr_number] = order_data
        return jsonify({sr_number: order_data}), 201
    else:
        return render_template("sr_tracker.html")


''' 
***********************
START CREATE_SR LOGIC - PUT
***********************
'''



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)