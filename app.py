from flask import Flask, request, render_template
import pandas as pd
import dropbox
import os
from dotenv import load_dotenv

load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

app = Flask(__name__)

# Initialize Dropbox with your access token
DROPBOX_ACCESS_TOKEN = "sl.u.AFtTnd8kYAD1Nk3yVEeDsLz4BKxTHgHDD3jtLdk-LHYR024A7hiXv-ZsV0rP2MTvENvKSAgCMXFTfsY0J7txhkxrg3AuCf_8t3rSuzjxu1ZSKJJw4Q1FRYBrINTjeW4haIvZe8J2Q9aSLS4OfIusFebUynSnCJKordQpedNga-0nFdoE9cy6GweKdL4TogRvWiSuxxmmonMrZ8HEdHfbgEs3kxVaDrCbOfBLH0S1FL5e_ZdB0uXqxR-yE8Yesi1HDW1bxrjK2Q4LniM9JnpWJgMqUBSGWGxOlnNV02a12JE85PmijO5bJiEDMT0_d2RHIlfnAoOx4r9EVS2YUNntL9ppmIGZWiqaYPPphbEKRoP4AdPhpcfpVcxFYrkayagGo1gzNdmlJefbXJR1h7E2fQr8A2DPUAppvOaS8N588xRGcMA-IR5hfuqq5qp1ekvpbN8HEn_3qoeAt-45F9kn5yDF5zTiA-E6RyyYfgYvzF46HGVLJVw2uxPC-Eb8gZBQYv2ojcDc4KDUmtrK02BtY7fvlydGk_kmKII4KIKim8Kw-koQgSL8dIl_e1DUPr-n7JdQIMVy4xigqK1FprJxLDbj2hOHTuFsmefST32pC10WcnxH9iytcwm3JGsypZtSeb9zWCQcHv0tCxy_I34jNidJnnclFWpl9C-zBkdeWVD_wzdNDGPA3kW73hg_bHYPQVoRSyrE-qFo-3qIODW5gpeyT_ZsSA0e4_NtzCC3Qbu6S45cAPZSY0t5ie_dFmRYg97YffWzusIfjeZqwZGtbLPq2gJgiL2nLzg_BrTY120bWZ1LM8e0qvPeHZVA6Gu_ykK4vmxWwT4BxxIyxhco3pi3RyWpfZLIiSJq_KTofRpUhrdOeAXMMoDXQK_HJcpd6qwRt9DqEAq77vWt8gDh_1V82nAm6gzUTQiwAVoQE-4V3t1ovwbnC5a1WGnzyfoKVt9SdRUFl-dD8JTWcFrioXQEDU3JKGTkRV5-hocQBGQDxcth1hstRGB4NZV82qlpr9SVsgUz7f6YQm0IhnaGaoPS0JojTv354e7xHAUTuPB74Qu0Mb5EMHB6gA720DrjsRoQhQqkkqQ_GrNg2LGJpbApYR0CUkeiQOf_X_NIon_Twv5eFJTItONAK1wXSEi8B5jEa0BOcIGILnIr9JnQ5Abl8PxioZAU8DCLSWJEorWRQr-YWCccYfOXImw7L6mgro4CGSTSJ69JVwE4Yf-vGo1GqkgmvzjljfQ1KL2XHnM3vH6G9aEdY9l7B-O-cGeCTZCNAnfoPXOZnWJTLoy4jcIq"

@app.route('/')
def index():
    return render_template('form.html')

def upload_to_dropbox(data,filename):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    df_string = data.to_csv(index=False)
    db_bytes = bytes(df_string, 'utf8')
    targetfile = "/Apps/ifm_risk_profiling_responses/" + filename
    meta = dbx.files_upload(db_bytes, targetfile, mode=dropbox.files.WriteMode("overwrite"))

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form

    # Extract values
    email = data.get('email')
    q1 = int(data.get('q1'))
    q2 = int(data.get('q2'))
    q3 = int(data.get('q3'))
    q4 = int(data.get('q4'))
    q5 = int(data.get('q5'))
    q6 = int(data.get('q6'))
    q7 = int(data.get('q7'))

    # Q8: Checkboxes — can have multiple values
    q8_values = request.form.getlist('q8')
    q8_score = sum(int(val) for val in q8_values)

    q9 = int(data.get('q9'))
    q10 = int(data.get('q10'))
    q11 = int(data.get('q11'))
    q12 = int(data.get('q12'))
    q13 = int(data.get('q13'))
    q14 = int(data.get('q14'))
    q15 = int(data.get('q15'))

    total_score = sum([
        q1, q2, q3, q4, q5, q6, q7, q8_score,
        q9, q10, q11, q12, q13, q14, q15
    ])

    # Store in DataFrame
    new_row = pd.DataFrame([{
        'Email': email,
        'Q1': q1, 'Q2': q2, 'Q3': q3, 'Q4': q4, 'Q5': q5,
        'Q6': q6, 'Q7': q7, 'Q8': q8_score, 'Q9': q9, 'Q10': q10,
        'Q11': q11, 'Q12': q12, 'Q13': q13, 'Q14': q14, 'Q15': q15,
        'Total Score': total_score
    }])

    #data = pd.DataFrame({'responses':new_row})
    print(new_row)


    # Append to Excel
    #df_existing = pd.read_excel(LOCAL_EXCEL_PATH)
    #df_updated = pd.concat([df_existing, new_row], ignore_index=True)
    #df_updated.to_excel(LOCAL_EXCEL_PATH, index=False)

    filename = email+'.csv'
    upload_to_dropbox(new_row,filename)
    
    return "✅ Response submitted and uploaded to Dropbox!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
