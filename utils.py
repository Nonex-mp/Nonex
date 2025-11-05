import requests

TELEGRAM_TOKEN = "8485710868:AAGgWgsZLeQiyhEEwxLTy-3T4gQae9GJ5S0"
TELEGRAM_CHAT_ID = 8109954183

def send_telegram_notification(product_name, email):
    message = f"📦 New Order Received!\nProduct: {product_name}\nBuyer Email: {email}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)
