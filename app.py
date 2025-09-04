# 1. ADD 'flash' TO THE IMPORT
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 2. ADD A SECRET_KEY FOR FLASH MESSAGES
app.config['SECRET_KEY'] = 'your-super-secret-key'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save to the database (your existing code)
        entry = Contact(name=name, email=email, message=message)
        db.session.add(entry)
        db.session.commit()

        # NEW: Save to a .txt file
        with open('submissions.txt', 'a', encoding='utf-8') as f:
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Message: {message}\n")
            f.write("----------------------------------------\n\n")

        flash('Thank you! Your message has been sent successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html')
@app.route('/messages')
def messages():
    # Simple password protection
    auth = request.authorization
    # IMPORTANT: Change 'admin' and 'your-password' to something secure!
    if not auth or not (auth.username == 'admin' and auth.password == 'your-password'):
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    # Fetch all messages from the database, newest first
    all_messages = Contact.query.order_by(Contact.id.desc()).all()
    return render_template('messages.html', messages=all_messages)
