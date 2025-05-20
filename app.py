from flask import Flask, render_template, request
import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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

    # Save to Excel
    df = pd.DataFrame([responses])
    filename = 'client_responses.xlsx'
    df.to_excel(filename, index=False)

    # Email it (Optional - fill in credentials)
    send_email_with_attachment(filename)

    return 'Thank you for your submission!'

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
    from_email = "your-email@gmail.com"  # Replace with your Gmail address
    to_email = "recipient-email@example.com"  # Your email or the recipient's email
    subject = "New Client Responses"
    
    # Compose the email body
    body = f"""
    Here are the new client responses:
    
    Question 1: {responses['Question 1']}
    Question 2: {responses['Question 2']}
    Question 3: {responses['Question 3']}
    Question 4: {responses['Question 4']}
    Question 5: {responses['Question 5']}
    """

    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email using Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, "your-app-password")  # Use your Gmail App Password
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
