from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

# In-memory storage for OTPs
otp_storage = {}

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_password'

def generate_otp():
    """Generate a 6-digit numeric OTP."""
    return ''.join(random.choices('0123456789', k=6))

def send_email(recipient, subject, body):
    """Send an email using SMTP."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [recipient], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/send-otp', methods=['POST'])
def send_otp():
    """Endpoint to generate and send OTP."""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'}), 400

    otp = generate_otp()
    otp_storage[email] = otp

    subject = 'Your OTP Code'
    body = f'Your OTP code is: {otp}'

    if send_email(email, subject, body):
        return jsonify({'success': True, 'message': 'OTP sent successfully.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP.'}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Endpoint to verify OTP."""
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if not email or not otp:
        return jsonify({'success': False, 'message': 'Email and OTP are required.'}), 400

    if email in otp_storage and otp_storage[email] == otp:
        del otp_storage[email]  # Clear OTP after successful verification
        return jsonify({'success': True, 'message': 'OTP verified successfully.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
