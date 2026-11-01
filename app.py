from flask import Flask, render_template_string, request

app = Flask(__name__)

# FULLY CORRECTED HTML AND CSS TEMPLATES WITH IMPORTED REQUEST

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        @property {
            syntax: '<angle>';
            inherits: false;
            initial-value: 0deg;
        }
        @keyframes rotate {
            0% { --angle: 0deg; }
            100% { --angle: 360deg; }
        }
        body {
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #0a0a16 0%, #1a1a2e 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-sizing: border-box;
        }
        .glow-card {
            position: relative;
            background: #0f3460;
            padding: 40px 30px;
            border-radius: 20px;
            width: 100%;
            max-width: 360px;
            margin: auto;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        .glow-card::before {
            content: '';
            position: absolute;
            inset: -6px;
            border-radius: 24px;
            background: conic-gradient(from var(--angle), #00d2ff, #0052ff, #00d2ff, #00f2fe, #00d2ff);
            animation: rotate 10s linear infinite;
            z-index: -1;
        }
        h2 {
            color: #fff;
            margin-bottom: 30px;
            font-weight: bold;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-size: 24px;
        }
        .input-group {
            margin-bottom: 25px;
            text-align: left;
        }
        input {
            width: 100%;
            padding: 15px;
            background: #16213e;
            border: 2px solid transparent;
            border-radius: 12px;
            color: white;
            box-sizing: border-box;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }
        input:focus {
            border-color: #00d2ff;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.6);
        }
        button {
            width: 100%;
            background: linear-gradient(to right, #00d2ff, #2563eb);
            color: white;
            padding: 16px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
            text-transform: uppercase;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
        }
        button:active {
            transform: scale(0.98);
        }
        .link-container {
            margin-top: 25px;
            font-size: 14px;
        }
        .link-container a {
            color: #00d2ff;
            text-decoration: none;
            text-transform: uppercase;
            font-weight: 500;
            display: inline-block;
        }
        .link-container a:hover {
            text-decoration: underline;
        }
        .forgot-password {
            text-align: right;
            margin-bottom: 15px;
        }
        .forgot-password a {
            color: #00d2ff;
            text-decoration: none;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="glow-card">
        <h2>{{ title }}</h2>
        <form method="POST">
            {% if form_type == 'login' %}
                <div class="input-group">
                    <input type="text" name="email" placeholder="EMAIL ADDRESS" required>
                </div>
                <div class="input-group">
                    <input type="password" name="password" placeholder="PASSWORD" required>
                </div>
                <div class="forgot-password">
                    <a href="#">FORGOT PASSWORD?</a>
                </div>
                <button type="submit">LOGIN</button>
                <div class="link-container">
                    <span>DON'T HAVE AN ACCOUNT? <a href="/register">SIGN UP</a></span>
                </div>
            {% elif form_type == 'register' %}
                <div class="input-group">
                    <input type="text" name="username" placeholder="USERNAME" required>
                </div>
                <div class="input-group">
                    <input type="text" name="email" placeholder="EMAIL ADDRESS" required>
                </div>
                <div class="input-group">
                    <input type="password" name="password" placeholder="PASSWORD" required>
                </div>
                <div class="input-group">
                    <input type="password" name="confirm_password" placeholder="CONFIRM PASSWORD" required>
                </div>
                <button type="submit">REGISTER</button>
                <div class="link-container">
                    <a href="/">BACK TO LOGIN</a>
                </div>
            {% endif %}
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        return f'WELCOME BACK, USER WITH EMAIL {email}!'
    return render_template_string(HTML_TEMPLATE, title='LOGIN', form_type='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('username')
        return f'ACCOUNT CREATED FOR {user}!'
    return render_template_string(HTML_TEMPLATE, title='REGISTER', form_type='register')

if __name__ == '__main__':
    app.run(debug=True)
