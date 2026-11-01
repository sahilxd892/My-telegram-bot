import sqlite3
from flask import Flask, render_template, render_template_string, request, session, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sahilxd892@gmail.con'
app.config['MAIL_PASSWORD'] = 'hgimjdjpspvodquk'
mail = Mail(app)

# Database Initialization
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Auth System</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1b2a; color: #e0e1dd; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background-color: #1b263b; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); width: 100%; max-width: 400px; }
        h2 { text-align: center; color: #415a77; margin-bottom: 20px; }
        .input-group { margin-bottom: 15px; position: relative; }
        label { display: block; margin-bottom: 5px; color: #778da9; }
        input[type="text"], input[type="email"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #415a77; border-radius: 5px; box-sizing: border-box; background-color: #0d1b2a; color: #fff; }
        button { width: 100%; padding: 10px; background-color: #0077b6; border: none; border-radius: 5px; color: white; font-size: 16px; cursor: pointer; }
        button:hover { background-color: #0096c7; }
        .error { color: #ff4d4d; text-align: center; margin-bottom: 10px; }
        .success { color: #2ecc71; text-align: center; margin-bottom: 10px; }
        .toggle-password { position: absolute; right: 10px; top: 38px; cursor: pointer; color: #778da9; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% if request.endpoint == 'login' %}
            <h2>LOGIN</h2>
            <form action="{{ url_for('login') }}" method="POST">
                <div class="input-group">
                    <label>EMAIL ADDRESS</label>
                    <input type="email" name="email" required>
                </div>
                <div class="input-group">
                    <label>PASSWORD</label>
                    <input type="password" name="password" id="login_pass" required>
                    <span class="toggle-password" onclick="togglePass('login_pass')">SHOW</span>
                </div>
                <button type="submit">LOGIN</button>
            </form>
            <p style="text-align: center; margin-top: 15px;">
                <a href="{{ url_for('forgot_password') }}" style="color: #0096c7; text-decoration: none;">FORGOT PASSWORD?</a><br>
                DON'T HAVE AN ACCOUNT? <a href="{{ url_for('register') }}" style="color: #0096c7; text-decoration: none;">SIGN UP</a>
            </p>
        {% elif request.endpoint == 'register' %}
            <h2>REGISTER</h2>
            <form action="{{ url_for('register') }}" method="POST">
                <div class="input-group">
                    <label>USERNAME</label>
                    <input type="text" name="username" required>
                </div>
                <div class="input-group">
                    <label>EMAIL ADDRESS</label>
                    <input type="email" name="email" required>
                </div>
                <div class="input-group">
                    <label>PASSWORD</label>
                    <input type="password" name="password" id="reg_pass" required>
                    <span class="toggle-password" onclick="togglePass('reg_pass')">SHOW</span>
                </div>
                <div class="input-group">
                    <label>CONFIRM PASSWORD</label>
                    <input type="password" name="confirm_password" id="confirm_pass" required>
                    <span class="toggle-password" onclick="togglePass('confirm_pass')">SHOW</span>
                </div>
                <button type="submit">REGISTER</button>
            </form>
            <p style="text-align: center; margin-top: 15px;">
                BACK TO <a href="{{ url_for('login') }}" style="color: #0096c7; text-decoration: none;">LOGIN</a>
            </p>
        {% elif request.endpoint == 'forgot_password' %}
            <h2>FORGOT PASSWORD</h2>
            <form action="{{ url_for('forgot_password') }}" method="POST">
                <div class="input-group">
                    <label>ENTER YOUR EMAIL</label>
                    <input type="email" name="email" required>
                </div>
                <button type="submit">SEND OTP</button>
            </form>
            <p style="text-align: center; margin-top: 15px;">
                <a href="{{ url_for('login') }}" style="color: #0096c7; text-decoration: none;">BACK TO LOGIN</a>
            </p>
        {% elif request.endpoint == 'verify_otp' %}
            <h2>VERIFY OTP</h2>
            <form action="{{ url_for('verify_otp') }}" method="POST">
                <div class="input-group">
                    <label>ENTER OTP</label>
                    <input type="text" name="otp" required>
                </div>
                <button type="submit">VERIFY</button>
            </form>
        {% elif request.endpoint == 'reset_password' %}
            <h2>RESET PASSWORD</h2>
            <form action="{{ url_for('reset_password') }}" method="POST">
                <div class="input-group">
                    <label>NEW PASSWORD</label>
                    <input type="password" name="password" id="reset_pass" required>
                    <span class="toggle-password" onclick="togglePass('reset_pass')">SHOW</span>
                </div>
                <button type="submit">UPDATE PASSWORD</button>
            </form>
        {% endif %}
    </div>

    <script>
        function togglePass(inputId) {
            var x = document.getElementById(inputId);
            var span = x.nextElementSibling;
            if (x.type === "password") {
                x.type = "text";
                span.textContent = "HIDE";
            } else {
                x.type = "password";
                span.textContent = "SHOW";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['user'] = email
            flash("Login successful!", "success")
            return f"Welcome back, {email}!"
        else:
            flash("Invalid email or password.", "error")
            return render_template_string(HTML_TEMPLATE)
            
    return render_template_string(HTML_TEMPLATE)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template_string(HTML_TEMPLATE)

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            conn.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "error")
            return render_template_string(HTML_TEMPLATE)
        finally:
            conn.close()

    return render_template_string(HTML_TEMPLATE)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            flash("Email not found.", "error")
            return render_template_string(HTML_TEMPLATE)

        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        session['reset_email'] = email

        msg = Message('Password Reset OTP', sender='your-email@gmail.com', recipients=[email])
        msg.body = f"Your OTP for password reset is: {otp}"
        try:
            mail.send(msg)
            flash("OTP sent to your email.", "success")
            return redirect(url_for('verify_otp'))
        except Exception as e:
            flash("Failed to send email. Check SMTP settings.", "error")
            return render_template_string(HTML_TEMPLATE)

    return render_template_string(HTML_TEMPLATE)

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form.get('otp', '')
        if session.get('otp') and session['otp'] == user_otp:
            return redirect(url_for('reset_password'))
        else:
            flash("Invalid OTP.", "error")
    return render_template_string(HTML_TEMPLATE)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password', '')
        hashed_password = generate_password_hash(new_password)
        email = session.pop('reset_email')
        session.pop('otp', None)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (hashed_password, email))
        conn.commit()
        conn.close()

        flash("Password updated successfully. Please log in.", "success")
        return redirect(url_for('login'))

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
