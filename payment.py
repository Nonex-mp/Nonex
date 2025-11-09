from utils import send_telegram_notification
from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import os
import requests

# Blueprint
payment_bp = Blueprint('payment', __name__)

# Folders & files
UPLOAD_FOLDER = 'uploads'
APPROVED_FOLDER = os.path.join(UPLOAD_FOLDER, 'approved')
EMAILS_FILE = os.path.join(UPLOAD_FOLDER, 'emails.txt')
APPROVED_LIST = os.path.join(UPLOAD_FOLDER, 'approved_list.txt')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(APPROVED_FOLDER, exist_ok=True)

# Telegram settings
TELEGRAM_TOKEN = "8485710868:AAGgWgsZLeQiyhEEwxLTy-3T4gQae9GJ5S0"
TELEGRAM_CHAT_ID = "8109954183"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

# Route: Choose payment
@payment_bp.route('/buy/<item>', methods=['GET'])
def choose_payment(item):
    return render_template("choose_payment.html", item=item)

# Route: GCash
@payment_bp.route('/buy/gcash/<item>', methods=['GET', 'POST'])
def buy_gcash(item):
    gcash_number = os.getenv("GCASH_NUMBER", "09382082847")
    qr_url = url_for('static', filename='img/gcash_qr.png')

    if request.method == 'POST':
        email = request.form.get('email')
        file = request.files.get('proof')
        if not email or not file:
            return "Email and proof are required!"

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Save record
        with open(EMAILS_FILE, 'a') as f:
            f.write(f"{email}|{item}|{filename}\n")
        with open(APPROVED_LIST, 'a') as f:
            f.write(f"{filename}|{item}\n")

        # Telegram notification
        message = f"You Have A New Gcash order📦!\nProduct: {item}\nEmail: {email}"
        send_telegram_message(message)

        return render_template("upload_success.html", product=item, email=email)

    return render_template("upload_proof.html", gcash_number=gcash_number, qr_url=qr_url, item=item)

# Route: PayPal
@payment_bp.route('/buy/paypal/<item>', methods=['GET', 'POST'])
def buy_paypal(item):
    if request.method == 'POST':
        email = request.form.get('email')
        file = request.files.get('proof')
        if not email or not file:
            return "Email and proof are required!"

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Save record
        with open(EMAILS_FILE, 'a') as f:
            f.write(f"{email}|{item}|{filename}\n")
        with open(APPROVED_LIST, 'a') as f:
            f.write(f"{filename}|{item}\n")

        # Telegram notification
        message = f"You Have A New PayPal order📦!\nProduct: {item}\nEmail: {email}"
        send_telegram_message(message)

        return render_template("upload_success.html", product=item, email=email)

    return render_template("upload_proof.html", gcash_number="PayPal Payment", qr_url="", item=item)











