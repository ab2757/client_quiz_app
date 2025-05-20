from flask import Flask, render_template, request
import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv
load_dotenv()
import os

sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    responses = {
        'Question 1': request.form['q1'],
        'Question 2': request.form['q2'],
        'Question 3': request.form['q3'],
        'Question 4': request.form['q4'],
        'Question 5': request.form['q5'],
    }

    # Send email with the responses
    send_email(responses)
    
    return 'thank-you'

def send_email_with_attachment(filepath):
    sender = 'your_email@example.com'
    password = 'your_email_password'
    recipient = 'recipient_email@example.com'

    msg = EmailMessage()
    msg['Subject'] = 'New Client Response'
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content('Attached is the new client response.')

    with open(filepath, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application',
                           subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                           filename=filepath)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

def send_email(responses):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    from_email = Email("ab2757@gmail.com")  # Your email or a SendGrid verified email
    to_email = To("ab2757@gmail.com")  # Your email or the recipient's email
    subject = "New Client Responses"
    
    body = f"""
    Here are the new client responses:
    
    Question 1: {responses['Question 1']}
    Question 2: {responses['Question 2']}
    Question 3: {responses['Question 3']}
    Question 4: {responses['Question 4']}
    Question 5: {responses['Question 5']}
    """
    
    content = Content("text/plain", body)
    mail = Mail(
    from_email='ab2757@gmail.com',
    to_emails='ab2757@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content = content)
    
    try:
        response = sg.send(mail)
        print(f"Email sent with status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
