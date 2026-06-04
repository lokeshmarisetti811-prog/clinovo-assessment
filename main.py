from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import traceback
import os
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SMTP_EMAIL = os.getenv("SMTP_SENDER_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "API Running"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

@app.post("/send-report")
async def send_report(
    file: UploadFile = File(...),
    candidate_name: str = Form(...),
    candidate_email: str = Form(...),
    candidate_phone: str = Form(...)
):
    try:
        pdf_data = await file.read()
        msg = EmailMessage()
        msg["Subject"] = f"Assessment Report - {candidate_name}"
        msg["From"] = SMTP_EMAIL
        msg["To"] = SMTP_EMAIL
        msg.set_content(
            f"""
Candidate Assessment Submitted
Name: {candidate_name}
Email: {candidate_email}
Phone: {candidate_phone}
The assessment report is attached.
"""
        )
        msg.add_attachment(
            pdf_data,
            maintype="application",
            subtype="pdf",
            filename=file.filename,
        )
        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as smtp:
            smtp.starttls()
            smtp.login(
                SMTP_EMAIL,
                SMTP_PASSWORD
            )
            smtp.send_message(msg)
        return {
            "success": True,
            "message": "Report emailed successfully"
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "message": str(e)
        }