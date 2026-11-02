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
transactions = {}  # {email: {'amount': ..., 'utr': ..., 'date': ...}}

def extract_details_from_email(email_body):
    # ईमेल से जानकारी निकालने का लॉजिक (उदाहरण के लिए)
    amount_match = re.search(r'Rs\.?\s*([\d.]+)', email_body, re.IGNORECASE)
    utr_match = re.search(r'UTR\s*[:#]?\s*(\d+)', email_body, re.IGNORECASE)
    
    amount = amount_match.group(1) if amount_match else "N/A"
    utr = utr_match.group(1) if utr_match else "UNKNOWN_UTR"
    
    return amount, utr

def check_email_for_payment(email_user, email_pass, target_email):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")

        # पेमेंट कंफर्मेशन ईमेल की खोज
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
                        'status': 'SUCCESS'
                    }
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>PORTAL</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #f4f4f9; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 20px; text-transform: uppercase; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; text-transform: uppercase; }
        button { width: 100%; padding: 10px; background-color: #3498db; border: none; border-radius: 4px; color: white; font-size: 16px; cursor: pointer; font-weight: bold; }
        .toggle-btn { text-align: center; margin-top: 15px; font-size: 14px; }
        .toggle-btn a { color: #3498db; text-decoration: none; cursor: pointer; }
        .form-group { display: none; }
        .active-form { display: block; }
        .nav { margin-bottom: 20px; width: 100%; max-width: 500px; display: flex; justify-content: space-between; }
        .nav a { color: #333; text-decoration: none; font-weight: bold; }
        .status-card { background: #e8f8f5; border: 2px solid #2ecc71; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .status-row { display: flex; justify-content: space-between; margin-bottom: 10px; }
        .status-value { font-weight: bold; color: #27ae60; }
        .api-box { background: #eee; padding: 10px; border-radius: 4px; word-break: break-all; font-weight: bold; margin-top: 10px; }
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
            <input type="text" name="email" placeholder="EMAIL ADDRESS" required>
            <input type="password" name="password" placeholder="PASSWORD" required>
            <button type="submit">LOGIN</button>
        </form>
        <div class="toggle-btn">DON'T HAVE AN ACCOUNT? <a onclick="toggleForm()">CREATE ACCOUNT</a></div>
    </div>

    <div id="register-form" class="form-group">
        <h2>CREATE ACCOUNT</h2>
        <form action="/register" method="POST">
            <input type="text" name="name" placeholder="FULL NAME" required>
            <input type="text" name="email" placeholder="EMAIL ADDRESS" required>
            <input type="password" name="password" placeholder="PASSWORD" required>
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
        <div class="api-box">YOUR API KEY: {{ api_key }}</div>
        
        <form action="/check-payment" method="POST" style="margin-top: 20px;">
            <button type="submit">CHECK EMAIL FOR PAYMENT</button>
        </form>

        {% if transaction %}
        <div class="status-card">
            <h3 style="text-align: center; color: #27ae60;">PAYMENT SUCCESSFUL</h3>
            <hr>
            <div class="status-row"><span>AMOUNT PAID:</span> <span class="status-value">RS. {{ transaction.get('amount') }}</span></div>
            <div class="status-row"><span>UTR NUMBER:</span> <span class="status-value">{{ transaction.get('utr') }}</span></div>
            <div class="status-row"><span>PAYMENT MODE:</span> <span class="status-value">UPI</span></div>
            <div class="status-row"><span>DATE & TIME:</span> <span class="status-value">{{ transaction.get('date') }}</span></div>
            <div class="status-row"><span>STATUS:</span> <span class="status-value" style="color: green;">{{ transaction.get('status') }}</span></div>
        </div>
        {% else %}
        <p>NO PAYMENT RECORD FOUND YET.</p>
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
    
    users[email] = {'name': name, 'password': password, 'api_key': api_key}
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
    return render_template_string(BASE_TEMPLATE, name=user['name'], api_key=user['api_key'], transaction=transaction)

@app.route('/check-payment', methods=['POST'])
def check_payment():
    if 'email' not in session:
        return redirect(url_for('index'))
    email = session['email']
    # यहाँ यूजर का वास्तविक ऐप पासवर्ड चाहिए होगा, जो अभी हमने स्टोर नहीं किया है
    # टेस्टिंग के लिए आप यहाँ अपना ऐप पासवर्ड डाल सकते हैं
    check_email_for_payment("your_email@gmail.com", "your_app_password", email)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
