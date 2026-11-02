from flask import Flask, render_template_string, request, redirect, url_for, session
import imaplib
import email
from email.header import decode_header
import uuid
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# डेटाबेस (इन-मेमोरी)
users = {}  # {email: {'password': password, 'api_key': api_key, 'name': name}}
transactions = {}  # {email: {'amount': ..., 'utr': ..., 'date': ..., 'status': ...}}

def extract_details_from_email(email_body):
    amount_match = re.search(r'Rs\.?\s*([\d.]+)', email_body, re.IGNORECASE)
    utr_match = re.search(r'UTR\s*[:#]?\s*(\d+)', email_body, re.IGNORECASE)
    
    amount = amount_match.group(1) if amount_match else "N/A"
    utr = utr_match.group(1) if utr_match else "UNKNOWN_UTR"
    
    return amount, utr

def check_email_for_payment(imap_user, app_pass, target_email):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(imap_user, app_pass)
        mail.select("inbox")

        query = '(SUBJECT "Payment received")'
        status, messages = mail.search(None, query)
        
        if messages[0]:
            latest_email_id = messages[0].split()[-1]
            status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    amount, utr = extract_details_from_email(body)
                    transactions[target_email] = {
                        'amount': amount,
                        'utr': utr,
                        'date': datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        'status': 'PAID'
                    }
                    mail.logout()
                    return
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")
    
    # यदि ईमेल नहीं मिला, तो पेंडिंग स्टेटस सेट करें
    if target_email not in transactions:
        transactions[target_email] = {
            'amount': '0.00', 'utr': 'N/A', 
            'date': datetime.now().strftime("%d %b %Y, %I:%M %p"), 
            'status': 'PENDING'
        }

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>PORTAL</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #fff; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 20px; text-transform: uppercase; }
        .container { background: #262626; padding: 30px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.5); width: 100%; max-width: 500px; margin-bottom: 20px; }
        h2, h3 { text-align: center; color: #00ffcc; margin-top: 0; }
        label { display: block; margin-top: 15px; font-weight: bold; color: #aaa; }
        input { width: 100%; padding: 12px; margin-top: 5px; border: 1px solid #444; border-radius: 6px; box-sizing: border-box; background: #333; color: #fff; font-size: 16px; text-transform: none; }
        button { width: 100%; padding: 12px; margin-top: 20px; background-color: #00b4d8; border: none; border-radius: 6px; color: white; font-size: 16px; cursor: pointer; font-weight: bold; transition: background 0.3s; }
        button:hover { background-color: #0096c7; }
        .toggle-btn { text-align: center; margin-top: 20px; font-size: 14px; }
        .toggle-btn a { color: #00ffcc; text-decoration: none; cursor: pointer; font-weight: bold; }
        .form-group { display: none; }
        .active-form { display: block; }
        .nav { margin-bottom: 20px; width: 100%; max-width: 500px; display: flex; justify-content: space-between; background: #262626; padding: 15px 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .nav a { color: #00ffcc; text-decoration: none; font-weight: bold; }
        .status-card { background: #333; border: 2px solid #444; padding: 25px; border-radius: 12px; margin-top: 20px; }
        .status-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-weight: bold; border-bottom: 1px solid #444; padding-bottom: 10px; }
        .status-value { color: #00ffcc; }
        .api-box { background: #1a1a1a; padding: 15px; border-radius: 6px; word-break: break-all; font-weight: bold; margin-top: 10px; text-align: center; border: 1px solid #00ffcc; color: #00ffcc; }
        .config-box { background: #262626; border: 1px solid #555; padding: 20px; border-radius: 10px; margin-top: 20px; }
    </style>
</head>
<body>

{% if 'email' in session %}
<div class="nav">
    <a href="/dashboard">DASHBOARD</a>
    <a href="/logout">LOGOUT</a>
</div>
{% endif %}

<div class="container">
    {% if not session.get('email') %}
    <div id="login-form" class="form-group active-form">
        <h2>LOGIN</h2>
        <form action="/login" method="POST">
            <label>EMAIL ADDRESS</label>
            <input type="text" name="email" required>
            <label>PASSWORD</label>
            <input type="password" name="password" required>
            <button type="submit">LOGIN</button>
        </form>
        <div class="toggle-btn">DON'T HAVE AN ACCOUNT? <a onclick="toggleForm()">CREATE ACCOUNT</a></div>
    </div>

    <div id="register-form" class="form-group">
        <h2>CREATE ACCOUNT</h2>
        <form action="/register" method="POST">
            <label>FULL NAME</label>
            <input type="text" name="name" required>
            <label>EMAIL ADDRESS</label>
            <input type="text" name="email" required>
            <label>PASSWORD</label>
            <input type="password" name="password" required>
            <button type="submit">REGISTER</button>
        </form>
        <div class="toggle-btn">ALREADY HAVE AN ACCOUNT? <a onclick="toggleForm()">LOGIN HERE</a></div>
    </div>
    <script>
        function toggleForm() {
            document.getElementById('login-form').classList.toggle('active-form');
            document.getElementById('register-form').classList.toggle('active-form');
        }
    </script>
    {% else %}
        {% if request.path == '/dashboard' %}
        <h2>DASHBOARD</h2>
        <p>WELCOME, {{ name }}!</p>
        <div>YOUR API KEY:</div>
        <div class="api-box">{{ api_key }}</div>
        
        <div class="config-box">
            <h3>EMAIL CONFIGURATION</h3>
            <form action="/update-config" method="POST">
                <label>GMAIL ADDRESS</label>
                <input type="text" name="imap_user" placeholder="your_email@gmail.com" value="{{ config.get('imap_user', '') }}" required>
                <label>APP PASSWORD</label>
                <input type="password" name="app_pass" placeholder="generated app password" value="{{ config.get('app_pass', '') }}" required>
                <button type="submit">SAVE CONFIGURATION</button>
            </form>
        </div>

        <form action="/check-payment" method="POST" style="margin-top: 20px;">
            <button type="submit" style="background-color: #2ec4b6;">CHECK EMAIL FOR PAYMENT</button>
        </form>

        {% if transaction %}
        <div class="status-card">
            <h3>TRANSACTION STATUS</h3>
            <hr style="border: 0; border-top: 1px solid #444; margin-bottom: 15px;">
            <div class="status-row"><span>AMOUNT PAID:</span> <span class="status-value">RS. {{ transaction.get('amount') }}</span></div>
            <div class="status-row"><span>UTR NUMBER:</span> <span class="status-value">{{ transaction.get('utr') }}</span></div>
            <div class="status-row"><span>PAYMENT MODE:</span> <span class="status-value">UPI</span></div>
            <div class="status-row"><span>DATE & TIME:</span> <span class="status-value">{{ transaction.get('date') }}</span></div>
            <div class="status-row"><span>STATUS:</span> <span class="status-value" style="color: {% if transaction.get('status') == 'PAID' %}#00ffcc{% else %}#ff4d4d{% endif %};">{{ transaction.get('status') }}</span></div>
        </div>
        {% endif %}
        {% endif %}
    {% endif %}
</div>

</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(BASE_TEMPLATE)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name'].upper()
    email = request.form['email'].lower()
    password = request.form['password']
    api_key = str(uuid.uuid4()).upper()
    
    users[email] = {
        'name': name, 'password': password, 'api_key': api_key,
        'config': {'imap_user': '', 'app_pass': ''}
    }
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email'].lower()
    password = request.form['password']
    
    if email in users and users[email]['password'] == password:
        session['email'] = email
        return redirect(url_for('dashboard'))
    return "INVALID CREDENTIALS", 401

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('index'))
    email = session['email']
    user = users[email]
    transaction = transactions.get(email)
    return render_template_string(BASE_TEMPLATE, name=user['name'], api_key=user['api_key'], transaction=transaction, config=user['config'])

@app.route('/update-config', methods=['POST'])
def update_config():
    if 'email' not in session:
        return redirect(url_for('index'))
    email = session['email']
    users[email]['config']['imap_user'] = request.form['imap_user']
    users[email]['config']['app_pass'] = request.form['app_pass']
    return redirect(url_for('dashboard'))

@app.route('/check-payment', methods=['POST'])
def check_payment():
    if 'email' not in session:
        return redirect(url_for('index'))
    email = session['email']
    config = users[email]['config']
    check_email_for_payment(config['imap_user'], config['app_pass'], email)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
