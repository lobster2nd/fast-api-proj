import logging
import smtplib
import os

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from models.email import Email

load_dotenv()

app = FastAPI(title="Spam app")

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    )
logging.getLogger().addHandler(file_handler)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@app.post("/send_email")
async def send_email(email: Email):
    if not email.to:
        raise HTTPException(status_code=400, detail="Invalid email address")

    try:
        smtp_server = "smtp.yandex.ru"
        smtp_port = 587
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            message = f"From: {smtp_username}\nSubject: {email.subject}\n\n{email.message}"
            server.sendmail(smtp_username, email.to, message)

        logging.info(f"Email sent to: {email.to}")
        return {"message": "Email sent successfully"}
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
