from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
from payment import payment_bp
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(payment_bp)

# --- HOME ---
@app.route('/')
def home():
    return render_template('index.html')

# --- PRESENTATIONS PAGE ---
@app.route('/presentations')
def presentations():
    subjects = [
        {
            "category": "History",
            "presentations": [
                {"name": "History", "thumbnail": url_for('static', filename='presentations/history1.png'), "price": 50},
                {"name": "Greek", "thumbnail": url_for('static', filename='presentations/greek1.png'), "price": 50}
            ]
        },
        {
            "category": "Mathematics",
            "presentations": [
                {"name": "Mathematics", "thumbnail": url_for('static', filename='presentations/mathematics1.png'), "price": 55},
            ]
        },
        {
            "category": "Filipino",
            "presentations": [
                {"name": "Mga Uri ng Pangungusap", "thumbnail": url_for('static', filename='presentations/mga_uri_ng_pangungusap1.png'), "price": 55}
            ]
        },
        {
            "category": "English",
            "presentations": [
                {"name": "English", "thumbnail": url_for('static', filename='presentations/english1.png'), "price": 30}
            ]
        },
        {
            "category": "Science",
            "presentations": [
                {"name": "Science", "thumbnail": url_for('static', filename='presentations/science1.png'), "price": 30}
            ]
        }
    ]
    return render_template('presentations.html', subjects=subjects)

# --- VIEW PRESENTATION PAGE ---
@app.route('/presentations/<subject>')
def view_presentation(subject):
    slides = []
    subject_lower = subject.lower()

    if subject_lower == "history":
        slides = [url_for('static', filename=f'presentations/history{i}.png') for i in range(1, 9)]
    elif subject_lower == "greek":
        slides = [url_for('static', filename=f'presentations/greek{i}.png') for i in range(1, 9)]
    elif subject_lower == "mathematics":
        slides = [url_for('static', filename=f'presentations/mathematics{i}.png') for i in range(1, 8)]
    elif subject_lower == "mga uri ng pangungusap":
        slides = [url_for('static', filename=f'presentations/mga_uri_ng_pangungusap{i}.png') for i in range(1, 9)]
    elif subject_lower == "english":
        slides = [url_for('static', filename=f'presentations/english{i}.png') for i in range(1, 6)]
    elif subject_lower == "science":
        slides = [url_for('static', filename=f'presentations/science{i}.png') for i in range(1, 6)]
    else:
        return render_template("404.html"), 404

    return render_template("view_presentation.html", subject=subject.capitalize(), slides=slides)

# --- OTHER PAGES ---
@app.route('/clothes')
def clothes():
    return render_template('clothes.html')

@app.route('/wallpapers')
def wallpapers():
    return render_template('wallpapers.html')

@app.route('/others')
def others():
    return render_template('others.html')

# --- GOOGLE SITE VERIFICATION ---
@app.route('/googleb29496bb2ba553a1.html')
def google_verify():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'googleb29496bb2ba553a1.html')

# --- SITEMAP + ROBOTS ---
@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

# --- TELEGRAM CUSTOM PRESENTATION REQUEST ---
TELEGRAM_TOKEN = "8485710868:AAGgWgsZLeQiyhEEwxLTy-3T4gQae9GJ5S0"
TELEGRAM_CHAT_ID = "8109954183"

def send_to_telegram(name, email, topic, description, language, deadline, budget):
    message = (
        f"🎨 *New Custom Presentation Request*\n\n"
        f"👤 *Name:* {name}\n"
        f"📧 *Email:* {email}\n"
        f"📚 *Topic:* {topic}\n"
        f"🗒 *Description:* {description}\n"
        f"🌐 *Language:* {language}\n"
        f"⏰ *Deadline:* {deadline or 'Not specified'}\n"
        f"💰 *Budget:* {budget or 'Not specified'}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })

    if response.status_code != 200:
        print("⚠️ Failed to send message to Telegram:", response.text)

@app.route('/request-presentation', methods=['GET', 'POST'])
def request_presentation():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        topic = request.form.get('topic')
        description = request.form.get('description')
        language = request.form.get('language')
        deadline = request.form.get('deadline')
        budget = request.form.get('budget')

        if not name or not email or not topic or not description:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('request_presentation'))

        send_to_telegram(name, email, topic, description, language, deadline, budget)
        return render_template('thank_you.html', name=name)

    return render_template('request_presentation.html')

# --- FILE UPLOAD CONFIG ---
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == "__main__":
    app.run(debug=True)






