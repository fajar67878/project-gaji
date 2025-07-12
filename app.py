from flask import Flask, render_template, request, redirect, url_for, session
import logging

app = Flask(__name__)

# Dummy data
karyawan_list = []
gaji_list = []

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# @app.route('/index')
# def index():
#     return render_template('index.html')
# app.py

# 1. IMPOR SEMUA YANG DIBUTUHKAN DI SINI
# from flask import Flask, render_template, request, redirect, url_for, session # <--- PASTIKAN 'session' ADA DI SINI

# 2. INISIALISASI APLIKASI FLASK
app = Flask(__name__)
# 3. SET SECRET_KEY UNTUK SESSI (SANGAT PENTING!)
app.secret_key = 'your_super_secret_key_here' # <-- GANTI INI DENGAN KUNCI YANG KUAT!

# 4. DATA GLOBAL ATAU KONFIGURASI LAINNYA
# Dummy data (for demonstration purposes)
karyawan_list = []
gaji_list = []

# --- User Management (Dummy) ---
# In a real application, you would store this in a database
# with hashed passwords.
USERS = {
    "admin": "pasword123", # DUMMY PASSWORD, DO NOT USE IN PRODUCTION
    "user": "userpass"
}

# --- DECORATOR UNTUK LOGIN REQUIRED (Opsional, tapi disarankan) ---
# Ini harus didefinisikan sebelum digunakan oleh rute-rute
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- RUTU-RUTU APLIKASI ANDA DIMULAI DI SINI ---

@app.route('/')
@login_required # Tambahkan ini jika Anda ingin melindungi halaman utama
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        logging.info(f'username: ' + username)
        logging.info(f'password: ' + password)

        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            logging.info(f'loggin successs')
            return redirect(url_for('index'))
        else:
            logging.info(f'loggin Error')
            return render_template('login.html', error="Invalid username or password")
        logging.info(f'is not post')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/karyawan', methods=['GET', 'POST'])
@login_required # Lindungi rute ini
def karyawan():
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        karyawan_list.append({'nama': nama, 'jabatan': jabatan})
        return redirect(url_for('karyawan'))
    return render_template('karyawan.html', karyawan_list=karyawan_list)

# ... (rute lainnya) ...

# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/karyawan', methods=['GET', 'POST'])
# def karyawan():
#     if request.method == 'POST':
#         nama = request.form['nama']
#         jabatan = request.form['jabatan']
#         karyawan_list.append({'nama': nama, 'jabatan': jabatan})
#         return redirect(url_for('karyawan'))
#     return render_template('karyawan.html', karyawan=karyawan_list)

@app.route('/gaji', methods=['GET', 'POST'])
@login_required # Lindungi rute ini
def gaji():
    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = request.form['jumlah']
        gaji_list.append({'nama': nama, 'jumlah': jumlah})
        return redirect(url_for('gaji'))
    return render_template('gaji.html', gaji=gaji_list, karyawan=karyawan_list)

@app.route('/laporan')
def laporan():
    return render_template('laporan.html', gaji=gaji_list)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

if __name__ == '__main__':
    app.run(debug=True)