from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.auth_utils import verify_email, reset_password

router = APIRouter()


def send_email(to_email: str, subject: str, html_content: str):
    message = Mail(
        from_email="your_email@example.com",  # Ваша електронна адреса
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        # Ваш API-ключ SendGrid
        sg = SendGridAPIClient("your_sendgrid_api_key")
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(e)
        return None
    

@router.post("/email/verify/", response_model=User)
def verify_user_email(token: str, db: Session = Depends(SessionLocal)):
    # Маршрут для верифікації електронної пошти користувача
    return verify_email(db, token)


@router.post("/email/reset-password/")
def reset_user_password(email: str, db: Session = Depends(SessionLocal)):
    # Маршрут для скидання паролю (необов'язковий)
    return reset_password(db, email)
