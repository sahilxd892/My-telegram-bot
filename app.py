import os
from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'secret_key_123'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sahilxd892@gmail.com' 
app.config['MAIL_PASSWORD'] = 'hgimjdjpspvodquk'
app.config['MAIL_DEFAULT_SENDER'] = 'sahilxd892@gmail.com'

mail = Mail(app)

CSS_STYLES = '''
<style>
  :root {
    --primary-color: #4a90e2;
    --bg-color: #121212;
    --card-bg: #1e1e26;
    --text-color: #e0e0e0;
    --accent-color: #00bcd4;
  }
  body {
    background-color: var(--bg-color);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
  }
  .auth-card {
    background-color: var(--card-bg);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    width: 100%;
    max-width: 400px;
    border: 1px solid #333;
  }
  h2 { color: var(--text-color); text-align: center; margin-bottom: 25px; font-weight: 600; }
  .input-group { position: relative; margin-bottom: 20px; }
  .input-group input {
    width: 100%; padding: 12px 15px; background-color: #2a2a36;
    border: 1px solid #444; border-radius: 8px; color: var(--text-color);
    font-size: 16px; box-sizing: border-box; transition: border-color 0.3s;
  }
  .input-group input:focus { outline: none; border-color: var(--accent-color); }
  .input-group label {
    position: absolute; left: 15px; top: 50%; transform: translateY(-50%);
    color: #888; pointer-events: none; transition: 0.3s ease all;
    background-color: #2a2a36; padding: 0 5px;
  }
  .input-group input:focus ~ label, .input-group input:not(:placeholder-shown) ~ label {
    top: 0; font-size: 12px; color: var(--accent-color);
  }
  button {
    width: 100%; padding: 12px; background-color: var(--primary-color);
    border: none; border-radius: 8px; color: white; font-size: 16px;
    font-weight: bold; cursor: pointer; transition: background-color 0.3s;
  }
  button:hover { background-color: #357abd; }
  .footer-links { text-align: center; margin-top: 15px; }
  .footer-links a { color: var(--accent-color); text-decoration: none; font-size: 14px; }
  .footer-links a:hover { text-decoration: underline; }
  .flash-msg { padding: 10px; border-radius: 6px; margin-bottom: 15px; text-align: center; font-size: 14px; }
  .flash-error { background-color: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
  .flash-success { background-color: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }
</style>
'''

def render_page(title, body_content):
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="auth-card">
            {{% with messages = get_flashed_messages(with_categories=true) %}}
                {{% if messages %}}
                    {{% for category, message in messages %}}
                        <div class="flash-msg flash-{{ category }}">{{ message }}</div>
                    {{% endfor %}}
                {{% endif %}}
            {{% endwith %}}
            {body_content}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash("Registration successful!", "success")
        return redirect(url_for('login'))
    
    content = f'''
    <h2>Register</h2>
    <form method="POST">
        <div class="input-group">
            <input type="text" name="username" id="username" placeholder=" " required>
            <label for="username">Username</label>
        </div>
        <div class="input-group">
            <input type="email" name="email" id="email" placeholder=" " required>
            <label for="email">Email Address</label>
        </div>
        <div class="input-group">
            <input type="password" name="password" id="password" placeholder=" " required>
            <label for="password">Password</label>
        </div>
        <button type="submit">REGISTER</button>
    </form>
    <div class="footer-links">
        <p>Already have an account? <a href="{url_for('login')}">Login</a></p>
    </div>
    '''
    return render_page("Register", content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        flash("Login successful!", "success")
        return redirect(url_for('index'))
        
    content = f'''
    <h2>Login</h2>
    <form method="POST">
        <div class="input-group">
            <input type="email" name="email" id="email" placeholder=" " required>
            <label for="email">Email Address</label>
        </div>
        <div class="input-group">
            <input type="password" name="password" id="password" placeholder=" " required>
            <label for="password">Password</label>
        </div>
        <button type="submit">LOGIN</button>
    </form>
    <div class="footer-links">
        <p><a href="{url_for('forgot_password')}">Forgot Password?</a></p>
        <p>Don't have an account? <a href="{url_for('register')}">Sign Up</a></p>
    </div>
    '''
    return render_page("Login", content)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            msg = Message("Password Reset OTP", recipients=[email])
            msg.body = "Your OTP is 123456"
            mail.send(msg)
            flash("OTP sent to your email.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Failed to send email.", "error")
    
    content = f'''
    <h2>Forgot Password</h2>
    <form method="POST">
        <div class="input-group">
            <input type="email" name="email" id="email" placeholder=" " required>
            <label for="email">Enter your email</label>
        </div>
        <button type="submit">SEND OTP</button>
    </form>
    <div class="footer-links">
        <p><a href="{url_for('login')}">Back to Login</a></p>
    </div>
    '''
    return render_page("Forgot Password", content)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
