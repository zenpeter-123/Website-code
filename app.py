import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# Környezeti változók betöltése a .env fájlból
load_dotenv()

app = Flask(__name__)

# Titkos kulcs a Flask session-höz és SQL-höz
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallback-dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Jelszó hash előállítása környezeti változóból
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS_HASH = generate_password_hash(os.getenv('ADMIN_PASS', 'alapertelmezett_jelszo'))

@auth.verify_password
def verify_password(username, password):
    if username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password):
        return username
    return None

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cim = db.Column(db.String(100), nullable=False)
    tema = db.Column(db.String(50), nullable=False)
    leiras = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Kapcsolat a tananyagokhoz
    tananyagok = db.relationship('Material', backref='kurzus', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course {self.id}>'


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kurzus_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    tipus = db.Column(db.String(20), nullable=False)
    cim = db.Column(db.String(200), nullable=False)
    tartalom = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Material {self.id}>'


@app.route('/admin')
@auth.login_required
def admin():
    kurzusok = Course.query.order_by(Course.date_created).all()
    return render_template('admin/admin.html', kurzusok=kurzusok)

@app.route('/admin/new_course', methods=['GET', 'POST'])
@auth.login_required
def new_course():
    if request.method == 'POST':
        cim = request.form['cim']
        tema = request.form['tema']
        leiras = request.form.get('leiras', '')
        uj = Course(cim=cim, tema=tema, leiras=leiras)
        db.session.add(uj)
        db.session.commit()
        return redirect('/admin')
    return render_template('admin/new_course.html')


@app.route('/admin/course/<int:kurzus_id>/course_material', methods=['GET', 'POST'])
@auth.login_required
def course_material(kurzus_id):
    kurzus = Course.query.get_or_404(kurzus_id)
    return render_template('admin/course_material.html', kurzus=kurzus)


@app.route('/admin/course/<int:kurzus_id>/new_material', methods=['POST', 'GET'])
@auth.login_required
def new_material(kurzus_id):
    kurzus = Course.query.get_or_404(kurzus_id)
    if request.method == 'POST':
        tipus = request.form['tipus']
        cim = request.form['cim']
        tartalom = request.form['tartalom']
        uj = Material(kurzus_id=kurzus_id, tipus=tipus, cim=cim, tartalom=tartalom)
        db.session.add(uj)
        db.session.commit()
        return redirect(f'/admin/course/{kurzus.id}/course_material')
    return render_template('admin/new_material.html', kurzus=kurzus)


@app.route('/admin/material/<int:id>/delete')
@auth.login_required
def delete_material(id):
    tananyag = Material.query.get_or_404(id)
    kurzus_id = tananyag.kurzus_id
    db.session.delete(tananyag)
    db.session.commit()
    return redirect(f'/admin/course/{kurzus_id}/course_material')

@app.route('/admin/course/<int:kurzus_id>/delete')
@auth.login_required
def delete_course(kurzus_id):
    kurzus = Course.query.get_or_404(kurzus_id)
    db.session.delete(kurzus) # A cascade="all, delete-orphan" automatikusan törli a tananyagokat is
    db.session.commit()
    return redirect('/admin')

@app.route('/admin/course/<int:kurzus_id>/update', methods=['GET', 'POST'])
@auth.login_required
def update_course(kurzus_id):
    kurzus = Course.query.get_or_404(kurzus_id)
    if request.method == 'POST':
        kurzus.cim = request.form['cim']
        kurzus.tema = request.form['tema']
        kurzus.leiras = request.form.get('leiras', '')
        db.session.commit()
        return redirect('/admin')
    return render_template('admin/update_course.html', kurzus=kurzus)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_me')
def about():
    return render_template('about_me.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)