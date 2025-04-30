from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate("firebase_admin.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize Firebase Admin
cred = credentials.Certificate('firebase_admin.json')

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
    
@app.route('/drivers')
def get_drivers():
    driver_ref = db.collection('drivers')
    docs = driver_ref.stream()

    drivers = []
    for doc in docs:
        data = doc.to_dict()
        drivers.append({
            'id': doc.id,
            'name': data.get('name'),
            'status': data.get('status')
        })

    return jsonify(drivers)


@app.route('/loads')
def get_loads():
    load_ref = db.collection('loads')
    docs = load_ref.stream()

    loads = []
    for doc in docs:
        data = doc.to_dict()
        loads.append({
            'id': doc.id,
            'origin': data.get('origin'),
            'destination': data.get('destination'),
            'status': data.get('status')
        })

    return jsonify(loads)

from flask import request

@app.route('/assign', methods=['POST'])
def assign_load():
    data = request.get_json()
    driver_id = data.get('driver_id')
    load_id = data.get('load_id')

    try:
        # Update driver status to false (not available)
        db.collection('drivers').document(driver_id).update({
            'status': False
        })

        # Update load status to false (assigned)
        db.collection('loads').document(load_id).update({
            'status': False
        })

        return jsonify({"message": "Load successfully assigned!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
