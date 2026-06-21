from flask import Flask, request, jsonify, render_template, redirect, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json, os
from database import init_db, get_db
from models import User, Patient, Drug, Prescription
from config import get_doctor, save_settings, load_settings, DRUG_CATEGORIES
from utils.prescription_engine import build_pdf_base64
from utils.gemini_helper import analyze_case

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

init_db()

# تحميل الأدوية
from data.drug_database import ALL_DRUGS
db = get_db()
if db.query(User).filter_by(username='admin').first() is None:
    db.add(User(username='admin', password_hash=generate_password_hash('admin123'), is_admin=True, is_active=True))
if db.query(Drug).count() == 0:
    for d in ALL_DRUGS:
        db.add(Drug(**d))
db.commit()
db.close()

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    return db.query(User).get(int(user_id))

# --- PWA Routes ---
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('.', 'sw.js')

@app.route('/icon-192.png')
def icon_192():
    return send_from_directory('.', 'icon-192.png')

@app.route('/icon-512.png')
def icon_512():
    return send_from_directory('.', 'icon-512.png')

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        user = db.query(User).filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            if not user.is_active:
                return render_template('login.html', error='Account disabled.')
            login_user(user)
            return redirect('/')
        return render_template('login.html', error='Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/')
@login_required
def index():
    return render_template('index_pwa.html')

# --- Admin ---
@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect('/')
    return render_template('admin.html')

@app.route('/api/admin/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def manage_users():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    db = get_db()
    if request.method == 'GET':
        users = db.query(User).all()
        return jsonify([{'id': u.id, 'username': u.username, 'is_admin': u.is_admin, 'is_active': u.is_active} for u in users])
    elif request.method == 'POST':
        data = request.json
        if db.query(User).filter_by(username=data['username']).first():
            return jsonify({'error': 'Username exists'}), 400
        u = User(username=data['username'], password_hash=generate_password_hash(data['password']), is_active=True)
        db.add(u); db.commit()
        return jsonify({'status': 'ok', 'id': u.id})
    elif request.method == 'PUT':
        data = request.json
        u = db.query(User).get(data['id'])
        if u and u.id != current_user.id:
            if 'is_active' in data: u.is_active = data['is_active']
            db.commit()
            return jsonify({'status': 'ok'})
        return jsonify({'error': 'Cannot modify'}), 400
    elif request.method == 'DELETE':
        u = db.query(User).get(request.args.get('id'))
        if u and u.id != current_user.id:
            db.delete(u); db.commit()
            return jsonify({'status': 'ok'})
        return jsonify({'error': 'Cannot delete'}), 400

@app.route('/api/drugs')
@login_required
def drugs():
    db = get_db()
    cat = request.args.get('category')
    q = db.query(Drug)
    if cat: q = q.filter_by(category=cat)
    return jsonify([{'id': d.id, 'trade_name': d.trade_name, 'category': d.category, 'admin_route': d.admin_route, 'dosage': d.dosage, 'frequency': d.frequency, 'duration': d.duration} for d in q.all()])

@app.route('/api/patients', methods=['GET', 'POST'])
@login_required
def patients():
    db = get_db()
    if request.method == 'POST':
        data = request.json
        p = Patient(**data)
        db.add(p); db.commit()
        return jsonify({'id': p.id}), 201
    return jsonify([{'id': p.id, 'name': p.name, 'age': p.age, 'gender': p.gender, 'phone': p.phone} for p in db.query(Patient).all()])

@app.route('/api/ai/analyze', methods=['POST'])
@login_required
def ai_analyze():
    data = request.json
    result = analyze_case(data['symptoms'], data.get('age',''), data.get('gender',''), data.get('chronic',''), data.get('allergies',''))
    return jsonify({'result': result})

@app.route('/api/generate-pdf', methods=['POST'])
@login_required
def generate_pdf():
    data = request.json
    b64 = build_pdf_base64(data['patient'], data['drugs'], data.get('diagnosis',''), data.get('notes',''), get_doctor())
    return jsonify({'pdf_base64': b64})

@app.route('/api/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST' and current_user.is_admin:
        save_settings(request.json)
        return jsonify({'status': 'ok'})
    return jsonify(load_settings())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
