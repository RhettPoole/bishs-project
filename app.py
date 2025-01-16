# filepath: /x:/bishs-project/app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configure Flask-Mail server
app.config['MAIL_SERVER']= 'smtp.gmail.com' # server address
app.config['MAIL_PORT'] = 587 # server port
app.config['MAIL_USE_TLS'] = True # enable TLS encryption, this makes the communication secure.
app.config['MAIL_USERNAME'] = 'rhettpoole.20@gmail.com' 
app.config['MAIL_PASSWORD'] = 'zron snjn lyjm xtpy' # app password for gmail account

mail = Mail(app)

# Set route for homepage, automatically selects "templates" folder, as this is a standard -
# - location for html files when using Flask.
@app.route('/')
def index():
    return render_template('index.html')

# Defining route for sending email, this will be called when the form is submitted.
@app.route('/send_email', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Create email message
    msg = Message('New Form Submission',
                  sender='rhettpoole.20@gmail.com',
                  recipients=['rhettpoole.20@gmail.com']) # setting recip to my email for testing
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    mail.send(msg)

    return redirect(url_for('index'))
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)