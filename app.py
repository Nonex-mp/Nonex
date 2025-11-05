<<<<<<< HEAD
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/presentations')
def presentations():
    return render_template('presentations.html')

@app.route('/wallpapers')
def wallpapers():
    return render_template('wallpapers.html')

@app.route('/clothes')
def clothes():
    return render_template('clothes.html')

@app.route('/others')
def others():
    return render_template('others.html')

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/presentations')
def presentations():
    return render_template('presentations.html')

@app.route('/wallpapers')
def wallpapers():
    return render_template('wallpapers.html')

@app.route('/clothes')
def clothes():
    return render_template('clothes.html')

@app.route('/others')
def others():
    return render_template('others.html')

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 9d31006 (Initial commit - Nonex website)
