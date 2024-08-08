import smtplib
from email.mime.text import MIMEText

def send_verification_email(email):
    verification_link = f'http://localhost:3000/verify?email={email}'
    msg = MIMEText(f'Please verify your email by clicking on the following link: {verification_link}')
    msg['Subject'] = 'Email Verification'
    msg['From'] = 'sdk29day@gmail.com'
    msg['To'] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('sdk29day@gmail.com', 'Sami2507')
        server.sendmail(msg['From'], [msg['To']], msg.as_string())

def subscribe(db, email):
    try:
        send_verification_email(email)
        db.subscribers.insert_one({"email": email, "verified": False})
        return {"message": "Verification email sent"}
    except Exception as e:
        print('Error during subscription:', e)
        raise Exception('Error during subscription')
