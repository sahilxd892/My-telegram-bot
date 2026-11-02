from flask import Flask, render_template_string, request, redirect, url_for, session
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Mock in-memory user database
users_db = {}

# CSS Template for uniform retro dark UI
BASE_STYLE = """
<style>
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: 'Courier New', Courier, monospace;
    }
    body {
        background-color: #121212;
        color: #00ffcc;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    .container {
        background-color: #1e1e1e;
        border: 2px solid #00ffcc;
        padding: 30px;
        border-radius: 8px;
        width: 100%;
        max-width: 500px;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
    }
    .dashboard-container {
        max-width: 800px;
    }
    h2, h3 {
        text-align: center;
        margin-bottom: 20px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .form-group {
        margin-bottom: 15px;
    }
    label {
        display: block;
        margin-bottom: 5px;
        font-size: 12px;
        color: #a0a0a0;
        text-transform: uppercase;
    }
    input[type="text"], input[type="email"], input[type="password"] {
        width: 100%;
        padding: 10px;
        background-color: #2b2b2b;
        border: 1px solid #00ffcc;
        color: #ffffff;
        border-radius: 4px;
        text-transform: uppercase;
    }
    input::placeholder {
        text-transform: none;
        color: #666;
    }
    button, .btn {
        width: 100%;
        padding: 12px;
        background-color: #00bcd4;
        border: none;
        color: #ffffff;
        font-weight: bold;
        cursor: pointer;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    button:hover, .btn:hover {
        background-color: #008ba3;
    }
    .link-box {
        text-align: center;
        margin-top: 15px;
        font-size: 12px;
    }
    .link-box a {
        color: #00ffcc;
        text-decoration: none;
    }
    .section-card {
        border: 1px solid #333;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #181818;
        border-radius: 6px;
    }
    .api-key-box {
        background-color: #111;
        padding: 10px;
        border: 1px dashed #00ffcc;
        text-align: center;
        color: #00ffcc;
        font-weight: bold;
        word-break: break-all;
        margin-bottom: 15px;
    }
    .status-success {
        border: 2px solid #00ff00;
        background-color: #052205;
        color: #ffffff;
        text-align: center;
        padding: 20px;
        border-radius: 8px;
    }
    .checkmark {
        font-size: 48px;
        color: #00ff00;
        line-height: 1;
        margin-bottom: 10px;
    }
    .thank-you-msg {
        color: #00ff00;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    .details-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #222;
        font-size: 14px;
    }
    .details-label {
        color: #888;
        text-transform: uppercase;
    }
    .details-val {
        font-weight: bold;
        color: #fff;
    }
    .status-badge {
        color: #00ff00;
        font-weight: bold;
    }
    .header-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
    .header-nav a {
        color: #ff5555;
        text-decoration: none;
        font-size: 12px;
        text-transform: uppercase;
    }
    .alert {
        color: #ff5555;
        text-align: center;
        margin-bottom: 10px;
        font-size: 12px;
    }
</style>
"""

# HTML Templates
LOGIN_TEMPLATE = BASE_STYLE + """
<div class="container">
    <h2>LOGIN</h2>
    {% if error %}<div class="alert">{{ error }}</div>{% endif %}
    <form method="POST" action="/login">
        <div class="form-group">
            <label>EMAIL ADDRESS</label>
            <input type="email" name="email" required placeholder="your_email@gmail.com">
        </div>
        <div class="form-group">
            <label>PASSWORD</label>
            <input type="password" name="password" required placeholder="••••••••">
        </div>
        <button type="submit">LOGIN</button>
    </form>
    <div class="link-box">
        DON'T HAVE AN ACCOUNT? <a href="/register">CREATE ACCOUNT</a>
    </div>
</div>
"""

REGISTER_TEMPLATE = BASE_STYLE + """
<div class="container">
    <h2>CREATE ACCOUNT</h2>
    {% if error %}<div class="alert">{{ error }}</div>{% endif %}
    <form method="POST" action="/register">
        <div class="form-group">
            <label>FULL NAME</label>
            <input type="text" name="full_name" required placeholder="JOHN DOE">
        </div>
        <div class="form-group">
            <label>EMAIL ADDRESS</label>
            <input type="email" name="email" required placeholder="your_email@gmail.com">
        </div>
        <div class="form-group">
            <label>PASSWORD</label>
            <input type="password" name="password" required placeholder="••••••••">
        </div>
        <button type="submit">REGISTER</button>
    </form>
    <div class="link-box">
        ALREADY HAVE AN ACCOUNT? <a href="/login">LOGIN HERE</a>
    </div>
</div>
"""

DASHBOARD_TEMPLATE = BASE_STYLE + """
<div class="container dashboard-container">
    <div class="header-nav">
        <span>WELCOME, {{ user.full_name.upper() }}!</span>
        <a href="/logout">LOGOUT</a>
    </div>

    <h2>DASHBOARD</h2>

    <!-- API CONFIGURATION SECTION -->
    <div class="section-card">
        <h3>API CONFIGURATION</h3>
        <label>YOUR API KEY:</label>
        <div class="api-key-box">{{ user.api_key }}</div>

        <form method="POST" action="/save-config">
            <div class="form-group">
                <label>GMAIL ADDRESS</label>
                <input type="email" name="gmail_address" value="{{ user.gmail_address or '' }}" placeholder="your_email@gmail.com" required>
            </div>
            <div class="form-group">
                <label>APP PASSWORD</label>
                <input type="password" name="app_password" value="{{ user.app_password or '' }}" placeholder="generated app password" required>
            </div>
            <button type="submit">SAVE CONFIGURATION</button>
        </form>
    </div>

    <!-- PAYMENT CHECK SECTION -->
    <div class="section-card">
        <form method="POST" action="/check-payment">
            <button type="submit" style="background-color: #00e676; color: #000;">CHECK EMAIL FOR PAYMENT</button>
        </form>
    </div>

    <!-- TRANSACTION STATUS DISPLAY -->
    {% if transaction %}
    <div class="section-card status-success">
        <div class="checkmark">✓</div>
        <div class="thank-you-msg">THANK YOU FOR PAYMENT OF ₹{{ "%.2f"|format(transaction.amount) }}</div>
        
        <div class="details-row">
            <span class="details-label">STATUS:</span>
            <span class="details-val status-badge">● SUCCESS</span>
        </div>
        <div class="details-row">
            <span class="details-label">AMOUNT PAID:</span>
            <span class="details-val">₹{{ "%.2f"|format(transaction.amount) }}</span>
        </div>
        <div class="details-row">
            <span class="details-label">TRANSACTION ID:</span>
            <span class="details-val">{{ transaction.tx_id }}</span>
        </div>
        <div class="details-row">
            <span class="details-label">UTR NUMBER:</span>
            <span class="details-val">{{ transaction.utr }}</span>
        </div>
        <div class="details-row">
            <span class="details-label">PAYMENT MODE:</span>
            <span class="details-val">UPI</span>
        </div>
        <div class="details-row">
            <span class="details-label">DATE & TIME:</span>
            <span class="details-val">{{ transaction.datetime }}</span>
        </div>
    </div>
    {% elif checked %}
    <div class="section-card" style="text-align: center; color: #ffbb00;">
        NO PAYMENT FOUND IN EMAIL INBOX.
    </div>
    {% endif %}

    <!-- SUPPORT SECTION -->
    <div class="section-card">
        <h3>SUPPORT & HELP</h3>
        <p style="font-size: 13px; color: #ccc; text-align: center; margin-bottom: 10px;">
            NEED HELP WITH INTEGRATION OR PAYMENT VERIFICATION?
        </p>
        <div class="details-row">
            <span class="details-label">EMAIL SUPPORT:</span>
            <span class="details-val">SUPPORT@GAYEWAY.RENDER.COM</span>
        </div>
        <div class="details-row">
            <span class="details-label">TELEGRAM:</span>
            <span class="details-val">@PAYMENT_GATEWAY_SUPPORT</span>
        </div>
        <div class="details-row">
            <span class="details-label">RESPONSE TIME:</span>
            <span class="details-val">24/7 AUTOMATED / 2HRS HUMAN</span>
        </div>
    </div>
</div>
"""

def parse_payment_email(gmail_user, app_password):
    """Connect to Gmail via IMAP and extract UPI payment details."""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, app_password)
        mail.select("inbox")

        # Search for unread or recent payment emails
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()

        if not email_ids:
            mail.logout()
            return None

        # Fetch latest email
        latest_id = email_ids[-1]
        status, data = mail.fetch(latest_id, "(RFC822)")

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body += part.get_payload(decode=True).decode(errors='ignore')
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')

                # Regex pattern matching for UPI payment emails
                amount_match = re.search(r'(?:Rs\.|\\u20b9)\\s*([\\d\\.]+)', body, re.IGNORECASE)
                utr_match = re.search(r'(?:UTR|Ref No|RRN)[\\s:]*([0-9]{10,12})', body, re.IGNORECASE)
                tx_id_match = re.search(r'(?:Transaction ID|Txn ID|ID)[\\s:]*([A-Za-z0-9]+)', body, re.IGNORECASE)

                if amount_match:
                    amount = float(amount_match.group(1))
                    utr = utr_match.group(1) if utr_match else "N/A"
                    tx_id = tx_id_match.group(1) if tx_id_match else "N/A"

                    date_str = msg.get("Date")
                    try:
                        formatted_date = datetime.strptime(date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S").strftime("%d %b %Y, %I:%M %p")
                    except:
                        formatted_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

                    mail.logout()
                    return {
                        "amount": amount,
                        "utr": utr,
                        "tx_id": tx_id,
                        "datetime": formatted_date
                    }
        mail.logout()
    except Exception as e:
        print("Error connecting to email:", e)
        return None
    return None

@app.route("/")
def index():
    if "user_email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email_input = request.form.get("email").strip().lower()
        password = request.form.get("password")
        full_name = request.form.get("full_name").strip()

        if email_input in users_db:
            return render_template_string(REGISTER_TEMPLATE, error="EMAIL ALREADY REGISTERED")

        users_db[email_input] = {
            "full_name": full_name,
            "password": password,
            "api_key": f"D1AC9D3A-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}",
            "gmail_address": "",
            "app_password": ""
        }
        session["user_email"] = email_input
        return redirect(url_for("dashboard"))

    return render_template_string(REGISTER_TEMPLATE)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_input = request.form.get("email").strip().lower()
        password = request.form.get("password")

        user = users_db.get(email_input)
        if user and user["password"] == password:
            session["user_email"] = email_input
            return redirect(url_for("dashboard"))
        return render_template_string(LOGIN_TEMPLATE, error="INVALID EMAIL OR PASSWORD")

    return render_template_string(LOGIN_TEMPLATE)

@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("login"))
    user = users_db.get(session["user_email"])
    return render_template_string(DASHBOARD_TEMPLATE, user=user, transaction=None, checked=False)

@app.route("/save-config", methods=["POST"])
def save_config():
    if "user_email" not in session:
        return redirect(url_for("login"))
    user = users_db.get(session["user_email"])
    user["gmail_address"] = request.form.get("gmail_address").strip()
    user["app_password"] = request.form.get("app_password").strip()
    return redirect(url_for("dashboard"))

@app.route("/check-payment", methods=["POST"])
def check_payment():
    if "user_email" not in session:
        return redirect(url_for("login"))
    user = users_db.get(session["user_email"])

    tx_data = parse_payment_email(user["gmail_address"], user["app_password"])

    return render_template_string(DASHBOARD_TEMPLATE, user=user, transaction=tx_data, checked=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
