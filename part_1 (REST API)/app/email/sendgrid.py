from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Замініть це на ваш ключ SendGrid API
SENDGRID_API_KEY = "your_sendgrid_api_key_here"


def send_email(to_email: str, subject: str, content: str):
    message = Mail(
        from_email="your_email@example.com",  # Ваша електронна адреса
        to_emails=to_email,
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response
    except Exception as e:
        print(str(e))
