from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize Firebase Admin
cred = credentials.Certificate('firebase_admin.json')
firebase_admin.initialize_app(cred)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/sessionLogin', methods=['POST'])
def session_login():
    id_token = request.json.get('idToken')

    try:
        decoded_token = auth.verify_id_token(id_token)
        session['username'] = decoded_token['email']
        return jsonify({"message": "Login successful"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Invalid ID token"}), 401

if __name__ == '__main__':
    app.run(debug=True)
