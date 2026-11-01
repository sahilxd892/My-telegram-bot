import random
from flask import Flask, render_template_string, request, session, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sahilxd892@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'hgimjdjpspvodquk'     # Replace with your app password

mail = Mail(app)

# HTML Templates with Embedded CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a16; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #0f3460; padding: 40px; border-radius: 20px; width: 100%; max-width: 360px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #00d2ff; }
        h2 { margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px; }
        .input-group { margin-bottom: 20px; text-align: left; }
        input { width: 100%; padding: 12px; background: #16213e; border: 1px solid #00d2ff; border-radius: 8px; color: white; box-sizing: border-box; outline: none; }
        button { width: 100%; background: linear-gradient(to right, #00d2ff, #2563eb); color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; text-transform: uppercase; }
        .error { color: #ff4d4d; margin-bottom: 15px; font-size: 14px; }
        .link-container { margin-top: 20px; font-size: 14px; }
        .link-container a { color: #00d2ff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>{{ title }}</h2>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="error">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            {% if form_type == 'login' %}
                <div class="input-group"><input type="email" name="email" placeholder="EMAIL ADDRESS" required></div>
                <div class="input-group"><input type="password" name="password" placeholder="PASSWORD" required></div>
                <button type="submit">LOGIN</button>
                <div class="link-container"><a href="{{ url_for('forgot_password') }}">FORGOT PASSWORD?</a></div>
                <div class="link-container">DON'T HAVE AN ACCOUNT? <a href="{{ url_for('register') }}">SIGN UP</a></div>
            {% elif form_type == 'register' %}
                <div class="input-group"><input type="text" name="username" placeholder="USERNAME" required></div>
                <div class="input-group"><input type="email" name="email" placeholder="EMAIL ADDRESS" required></div>
                <div class="input-group"><input type="password" name="password" placeholder="PASSWORD" required></div>
                <button type="submit">REGISTER</button>
                <div class="link-container"><a href="{{ url_for('login') }}">BACK TO LOGIN</a></div>
            {% elif form_type == 'forgot_password' %}
                <div class="input-group"><input type="email" name="email" placeholder="ENTER YOUR EMAIL" required></div>
                <button type="submit">SEND OTP</button>
                <div class="link-container"><a href="{{ url_for('login') }}">BACK TO LOGIN</a></div>
            {% elif form_type == 'verify_otp' %}
                <div class="input-group"><input type="text" name="otp" placeholder="ENTER 6-DIGIT OTP" required maxlength="6"></div>
                <button type="submit">VERIFY & LOGIN</button>
            {% endif %}
        </form>
    </div>
</body>
</html>
'''

# Mock user database
USERS = {'test@example.com': {'password': 'password123', 'username': 'Tester'}}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in USERS and USERS[email]['password'] == password:
            session['user'] = email
            return f"Welcome back, {USERS[email]['username']}!"
        flash('Invalid email or password.')
    return render_template_string(HTML_TEMPLATE, title='LOGIN', form_type='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        if email not in USERS:
            USERS[email] = {'password': password, 'username': username}
            flash('Account created! Please log in.')
            return redirect(url_for('login'))
        flash('Email already registered.')
    return render_template_string(HTML_TEMPLATE, title='REGISTER', form_type='register')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if email in USERS:
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            session['reset_email'] = email
            
            # Hide raw email using sender alias formatting
            msg = Message('Your Password Reset OTP',
                          sender=('MyProject Support', app.config['MAIL_USERNAME']),
                          recipients=[email])
            msg.body = f'Your 6-digit OTP for password reset is: {otp}'
            try:
                mail.send(msg)
                return redirect(url_for('verify_otp'))
            except Exception as e:
                flash('Failed to send OTP. Please try again.')
        else:
            flash('Email not found.')
    return render_template_string(HTML_TEMPLATE, title='FORGOT PASSWORD', form_type='forgot_password')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if user_otp == session.get('otp'):
            session['user'] = session['reset_email']
            session.pop('otp', None)
            session.pop('reset_email', None)
            return "OTP verified! You are now logged in."
        flash('Invalid OTP. Please try again.')
    return render_template_string(HTML_TEMPLATE, title='VERIFY OTP', form_type='verify_otp')

if __name__ == '__main__':
    app.run(debug=True)
