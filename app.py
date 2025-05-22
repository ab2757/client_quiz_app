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
from flask import Flask, render_template, request, redirect
from openpyxl import Workbook, load_workbook
from datetime import datetime
import dropbox


app = Flask(__name__)

DROPBOX_ACCESS_TOKEN = "_vWi9k20dIAAAAAAAAAAEUWp8ls44vAnYZhtocDkbx7EHXv9V4uGS3gXceBzErNO"
#DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_TOKEN")  # Set this in your Render env

EXCEL_FILE = "responses.xlsx"

@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    print("📝 Received form submission", flush=True)
    responses = {
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    }

    # Send email with the responses
    #send_email(responses)

    responses = [q1, q2, q3, q4, q5]
    save_to_excel(responses)
    upload_to_dropbox()
    
    #return 'thank-you'
    return "✅ Response submitted and uploaded to Dropbox!"

def save_to_excel(data):
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.append(["Timestamp", "Q1", "Q2", "Q3", "Q4", "Q5"])  # Adjust headers
    else:
        wb = load_workbook(EXCEL_FILE)
        ws = wb.active

    ws.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + data)
    wb.save(EXCEL_FILE)

def upload_to_dropbox():
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(EXCEL_FILE, "rb") as f:
        dbx.files_upload(f.read(), f"/{EXCEL_FILE}", mode=dropbox.files.WriteMode.overwrite)

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
    SENDGRID_API_KEY=os.getenv('SENDGRID_API_KEY')
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
        print("📤 Sending email...", flush=True)
        response = sg.send(mail)
        print(f"Email sent with status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

@app.route('/test-email')
def test_email():
    print("⚙️ Test email route hit", flush=True)
    try:
        SENDGRID_API_KEY=os.getenv('SENDGRID_API_KEY')
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        from_email='ab2757@gmail.com'
        to_email='ab2757@gmail.com'
        subject = "Test from Render"
        content = Content("text/plain", "This is a test email from Render.")
        mail = Mail(from_email, to_email, subject, content)
        response = sg.send(mail)
        print(f"✅ Email sent. Status: {response.status_code}", flush=True)
        return f"Sent. Status: {response.status_code}, Body: {response.body}"
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        return f"Error: {e}"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
