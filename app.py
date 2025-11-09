from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
from payment import payment_bp
import os

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
                {"name": "Greek", "thumbnail": url_for('static', filename='presentations/greek1.png'), "price": 99}
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
                {"name": "Filipino", "thumbnail": url_for('static', filename='presentations/filipino1.png'), "price": 25}
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
    elif subject_lower == "filipino":
        slides = [url_for('static', filename=f'presentations/filipino{i}.png') for i in range(1, 6)]
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

# --- GOOGLE VERIFICATION ---
@app.route('/googleb29496bb2ba553a1.html')
def google_verification():
    return send_from_directory('.', 'googleb29496bb2ba553a1.html')

# --- UPLOAD CONFIG ---
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == "__main__":
    app.run(debug=True)


