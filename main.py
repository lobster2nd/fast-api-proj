import logging
import smtplib
import os

from email.mime.text import MIMEText
from email.header import Header
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from models.email import Email

load_dotenv()

app = FastAPI(title="Mailer app")

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    )
logging.getLogger().addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    )
logging.getLogger().addHandler(console_handler)

logging.getLogger().setLevel(logging.INFO)


@app.post("/send_email")
def send_email(email: Email):
    if not email.to:
        raise HTTPException(status_code=400, detail="Invalid email address")

    try:
        smtp_server = "smtp.mail.ru"
        smtp_port = 587
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            message = MIMEText(email.message, 'plain', 'utf-8')
            message['From'] = smtp_username
            message['To'] = email.to
            message['Subject'] = Header(email.subject, 'utf-8')

            server.sendmail(smtp_username, email.to, message.as_string())

        logging.info(f"Email sent to: {email.to}")
        return {"message": "Email sent successfully"}
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
