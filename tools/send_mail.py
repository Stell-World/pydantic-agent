import smtplib
from email.mime.text import MIMEText

def send_email(receiver_email="fredyhoundayi@gmail.com", subject="Subject", message=""):
    """
    Send an email using Gmail SMTP.
    
    Args:
        receiver_email (str): Email address of the recipient (default: "fredyhoundayi@gmail.com")
        subject (str): Email subject (default: "Subject")
        message (str): Email message content
    """
    # Sender credentials
    sender = "fredhoundayi@gmail.com"
    app_password = "celmokazxbuhqhjg"
    
    # Add automatic disclaimer
    disclaimer = "\n\n---\nThis is an automated email sent by an AI agent and can be subject of incoherence. Please verify the information before acting."
    full_message = message + disclaimer
    
    # Create email message
    msg = MIMEText(full_message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver_email
    
    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.send_message(msg)
    
    print(f"✅ Email sent successfully to {receiver_email}!")

# Example usage
if __name__ == "__main__":
    send_email()
