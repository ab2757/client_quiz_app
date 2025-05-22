import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
#from dotenv import load_dotenv
#load_dotenv()
import os
from flask import Flask, render_template, request, redirect
from openpyxl import Workbook, load_workbook
from datetime import datetime
import dropbox


app = Flask(__name__)

DROPBOX_ACCESS_TOKEN = "sl.u.AFtPbLmOd81UIRoLqsFxCzlI3Sh8Zi8ke-ESE-QdTtv23ntY_hpKFjBzBk_7Qpxe9OSB0f6RICsGORcgVHs7kEwzQ3nZ6YzqqRI1gAlSifqLu7AxcfWECWv-vImc6fZ_ul6xBr4GXxQ6ld_3L9mKABTgOPqNM5RpwXmzK-_-Zow0iWHWp2xUFhsas7uDqlyCCxUfkAJrF5BAZLQL31D_ck-FqMKceoW7XN5tCWWT4Q8a9XAdcPhqYZGGaQy9mMLTLdqUjJkFn4kKJPTIAEHW1hLJz6DeOmyt-k8WilIPqY_ymCRUkLBhnBqc6jmK7Wlp9-PhL7oOADB8ijzA6jwVAQc6zt4qhb8bVO6FJewmx277IU9Xse-7dy-UqKzxvE1N28SrgL7gHiKoA-AR_6BmsLYknwE4uD0A78FuAAED_DCsLwpdHlop33tuaLtMkWl2OLruKQxwH_TvrqWi0M64gfAoqx0QkDojCzIeolYh6HrPuCPMpNZceZP4oeYtW3aMp3obwiK7nEYmpk563YysSmLNfMFDj_fPotY_tlvHzMOqcXLm0dRgQlytfLINrCz5vJQ6yN3u5jP3ylarwGfp8Q84S4AjSx9fBgJi3JU7UH3YUmjiwg0vbfke_SCx99787cQoB13wgmCTjn7e94YIv55ooucQEX3vQ8iC2JyNrFetwo2XVXkQA1H2XLAm8iqYZ5m3E_wVifaSHd0owTdyO_V8GNfvTd4owj_PptUTe0JFNQJun-hmDzVhYS9a0RfptNaStlzhXnSZ0nE66wKGT3AZx3eZSvsM3Kxzv8Y6z52tQDUxXzKWZBU75OYBbocwRe45VrYuGGgInydziTTpWyFcqCmCFlX_aUZl1PfnZxyCiKAdGkcHAtAKbeKJ8mj0vkmPT5Lnm5dHEKvy0EsKJ-Nu_YvR-wN6K7CxW03qkr8S2lh0NV2_zIJC2gcuSgQwW4wDtXNpAlv714QGIUzhexwiMGEOU1r4XT9BrIfYmfUqFitn3oVmVt9wNG9C7RouY2caZnFOjS3KD1S-DskjdohVMH7xRYc3ajNxuCB6bhIk1h3TfEvy0sH_30RsSonsY8kyniAzfcxFjpFyL7l3402dzjMDQnAnYeC4loKQ7D1caeQg54jmsgz5TCrs_wekQGauKXF-8R8qzYQ7RNUG-M8edcPWJ5Yu7gYMflqcKB-pZXb4vSDxokivHbwTq777a4x-HXWSQyQvYnBtyvbNrektl-OcDSplIdJ7VQV1kXSOWvYmjBLdmnJsivi3aBjktRRTMmhYryoRSZeoCsQCOxKf"
#DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_TOKEN")  # Set this in your Render env

#filename = "responses.csv"

@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    print("📝 Received form submission", flush=True)
    email = request.form.get('email')  # 👈 New line to get email
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')

    responses = [q1, q2, q3, q4, q5]
    data = pd.DataFrame({'responses':responses})
    #print(responses)
    #print(data)
    #filename = email.replace('@','at')+'.csv'
    filename = email+'.csv'
    upload_to_dropbox(data,filename)
    
    return "✅ Response submitted and uploaded to Dropbox!"


def upload_to_dropbox(data,filename):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    df_string = data.to_csv(index=False)
    db_bytes = bytes(df_string, 'utf8')
    targetfile = "/Apps/ifm_risk_profiling_responses/" + filename
    meta = dbx.files_upload(db_bytes, targetfile, mode=dropbox.files.WriteMode("overwrite"))



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
