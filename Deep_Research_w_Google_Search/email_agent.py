import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

FROM_EMAIL = Email("your_mail_address@mail.co")
TO_EMAIL = To("your_mail_address@mail.co")

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send an email with the given subject and HTML body using SendGrid.

    Returns a dictionary indicating the result of the operation with a status key.
    """
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        return {"status": "error", "message": "Missing SENDGRID_API_KEY"}

    sg = sendgrid.SendGridAPIClient(api_key=api_key)
    try:
        content = Content("text/html", html_body)
        mail = Mail(FROM_EMAIL, TO_EMAIL, subject, content).get()
        response = sg.client.mail.send.post(request_body=mail)
        return {"status": "success", "code": str(response.status_code)}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
