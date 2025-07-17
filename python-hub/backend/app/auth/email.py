from flask import current_app

def send_verification_email(user, token):
    # In production, use Flask-Mail or an async provider
    print(f"[EMAIL] Send verification to {user.email} with token: {token}")
 
def send_password_reset_email(user, token):
    print(f"[EMAIL] Send password reset to {user.email} with token: {token}") 