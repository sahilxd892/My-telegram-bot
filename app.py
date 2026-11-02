from flask import Flask, render_template_string, request, redirect, url_for, session
import imaplib
import email
from email.header import decode_header

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# इन-मेory यूजर और पेमेंट डेटाबेस
users = {}
payment_statuses = {}  # {email: "Pending" or "Paid"}

# ईमेल कॉन्फ़िगरेशन (इसे सुरक्षित रखने के लिए एनवायरनमेंट वेरिएबल का उपयोग करें)
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"  # जीमेल के लिए ऐप पासवर्ड का उपयोग करें

def check_payment_email(user_email):
    try:
        # IMAP सर्वर से कनेक्ट करें
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # पेमेंट से संबंधित ईमेल खोजें
        query = f'(SUBJECT "Payment received" TO "{user_email}")'
        status, messages = mail.search(None, query)
        
        if messages[0]:
            payment_statuses[user_email] = "Paid"
        else:
            if user_email not in payment_statuses:
                payment_statuses[user_email] = "Pending"
                
        mail.logout()
    except Exception as e:
        print(f"Error checking email: {e}")
        if user_email not in payment_statuses:
            payment_statuses[user_email] = "Pending"

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; display: flex; height: 100vh; background-color: #f4f4f9; }
        .sidebar { width: 220px; background-color: #2c3e50; color: white; display: flex; flex-direction: column; padding-top: 20px; }
        .sidebar h2 { text-align: center; }
        .sidebar a { padding: 15px; color: white; text-decoration: none; border-bottom: 1px solid #34495e; }
        .sidebar a:hover { background-color: #34495e; }
        .main-content { flex: 1; padding: 30px; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .status-paid { color: green; font-weight: bold; }
        .status-pending { color: orange; font-weight: bold; }
        .btn { display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>

<div class="sidebar">
    <h2>Portal Menu</h2>
    <a href="/dashboard">Dashboard</a>
    <a href="/settings">API & Email Settings</a>
    <a href="/logout" style="color: #e74c3c;">Logout</a>
</div>

<div class="main-content">
    <div class="card">
        <h1>Welcome, {{ name }}!</h1>
        <p>Email: {{ email }}</p>
    </div>

    <div class="card">
        <h2>Payment Verification</h2>
        <p>Current Status: 
            <span class="{% if status == 'Paid' %}status-paid{% else %}status-pending{% endif %}">
                {{ status }}
            </span>
        </p>
        <form action="/check-payment" method="POST">
            <button type="submit" class="btn">Check Email for Payment</button>
        </form>
    </div>
</div>

</body>
</html>
'''

AUTH_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Secure Portal</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .auth-box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 320px; }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #3498db; border: none; border-radius: 4px; color: white; font-size: 16px; cursor: pointer; }
        .toggle-btn { text-align: center; margin-top: 15px; font-size: 14px; }
        .toggle-btn a { color: #3498db; text-decoration: none; cursor: pointer; }
        .form-group { display: none; }
        .active-form { display: block; }
    </style>
</head>
<body>

<div class="auth-box">
    <div id="login-form" class="form-group active-form">
        <h2>Login</h2>
        <form action="/login" method="POST">
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="toggle-btn">Don't have an account? <a onclick="toggleForm()">Create Account</a></div>
    </div>

    <div id="register-form" class="form-group">
        <h2>Create Account</h2>
        <form action="/register" method="POST">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
        <div class="toggle-btn">Already have an account? <a onclick="toggleForm()">Login here</a></div>
    </div>
</div>

<script>
    function toggleForm() {
        document.getElementById('login-form').classList.toggle('active-form');
        document.getElementById('register-form').classList.toggle('active-form');
    }
</script>

</body>
</html>
'''

SETTINGS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Settings</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; display: flex; height: 100vh; background-color: #f4f4f9; }
        .sidebar { width: 220px; background-color: #2c3e50; color: white; display: flex; flex-direction: column; padding-top: 20px; }
        .sidebar a { padding: 15px; color: white; text-decoration: none; border-bottom: 1px solid #34495e; }
        .main-content { flex: 1; padding: 30px; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { padding: 10px 20px; background-color: #2ecc71; border: none; color: white; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>

<div class="sidebar">
    <a href="/dashboard">Dashboard</a>
    <a href="/settings">Settings</a>
    <a href="/logout" style="color: #e74c3c;">Logout</a>
</div>

<div class="main-content">
    <div class="card">
        <h2>API & Email Configuration</h2>
        <form action="/update-settings" method="POST">
            <label>IMAP Email:</label>
            <input type="email" name="email" value="{{ email }}" required>
            <label>App Password:</label>
            <input type="password" name="password" placeholder="Enter App Password" required>
            <button type="submit">Save Settings</button>
        </form>
    </div>
</div>

</body>
</html>
'''

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(AUTH_TEMPLATE)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    users[email] = {'name': name, 'password': password}
    payment_statuses[email] = "Pending"
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if email in users and users[email]['password'] == password:
        session['email'] = email
        return redirect(url_for('dashboard'))
    return "Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('index'))
    email = session['email']
    user_info = users[email]
    status = payment_statuses.get(email, "Pending")
    return render_template_string(DASHBOARD_TEMPLATE, name=user_info['name'], email=email, status=status)

@app.route('/check-payment', methods=['POST'])
def check_payment():
    if 'email' not in session:
        return redirect(url_for('index'))
    check_payment_email(session['email'])
    return redirect(url_for('dashboard'))

@app.route('/settings')
def settings():
    if 'email' not in session:
        return redirect(url_for('index'))
    return render_template_string(SETTINGS_TEMPLATE, email=EMAIL_USER)

@app.route('/update-settings', methods=['POST'])
def update_settings():
    global EMAIL_USER, EMAIL_PASS
    EMAIL_USER = request.form['email']
    EMAIL_PASS = request.form['password']
    return redirect(url_for('settings'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
