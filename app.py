from flask import Flask, render_template_string, request

app = Flask(__name__)

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>LOGIN</title>
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
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .glow-card {
            position: relative;
            background: #0f3460; padding: 40px; border-radius: 20px;
            width: 320px; text-align: center;
        }
        .glow-card::before {
            content: '';
            position: absolute;
            inset: -3px;
            border-radius: 23px;
            background: conic-gradient(from var(--angle), #00d2ff, #2563eb, #00d2ff);
            animation: rotate 4s linear infinite;
            z-index: -1;
        }
        h2 { color: #fff; margin-bottom: 25px; font-weight: bold; letter-spacing: 1px; }
        .input-group {
            margin-bottom: 20px;
        }
        input {
            width: 100%; padding: 14px 15px; background: #16213e;
            border: 1px solid #2563eb; border-radius: 10px; color: white;
            box-sizing: border-box; font-size: 16px; outline: none;
        }
        input::placeholder {
            color: #888;
            text-transform: uppercase;
        }
        button {
            width: 100%; background: linear-gradient(to right, #00d2ff, #2563eb); color: white;
            padding: 14px; border: none; border-radius: 10px; cursor: pointer;
            font-size: 18px; font-weight: bold; margin-top: 10px;
            text-transform: uppercase;
        }
        .links { margin-top: 20px; font-size: 14px; display: flex; justify-content: space-between; }
        .links a { color: #00d2ff; text-decoration: none; text-transform: uppercase; }
        .links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="glow-card">
        <h2>LOGIN</h2>
        <form method="POST">
            <div class="input-group">
                <input type="text" name="email" placeholder="EMAIL ADDRESS" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="PASSWORD" required>
            </div>
            <div class="links" style="justify-content: flex-end;">
                <a href="#">FORGOT PASSWORD?</a>
            </div>
            <button type="submit">LOGIN</button>
        </form>
        <div class="links">
            <span>DON'T HAVE AN ACCOUNT? <a href="/register">SIGN UP</a></span>
        </div>
    </div>
</body>
</html>
'''

REGISTER_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>REGISTER</title>
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
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .glow-card {
            position: relative;
            background: #0f3460; padding: 40px; border-radius: 20px;
            width: 320px; text-align: center;
        }
        .glow-card::before {
            content: '';
            position: absolute;
            inset: -3px;
            border-radius: 23px;
            background: conic-gradient(from var(--angle), #00d2ff, #2563eb, #00d2ff);
            animation: rotate 4s linear infinite;
            z-index: -1;
        }
        h2 { color: #fff; margin-bottom: 25px; font-weight: bold; letter-spacing: 1px; }
        .input-group {
            margin-bottom: 20px;
        }
        input {
            width: 100%; padding: 14px 15px; background: #16213e;
            border: 1px solid #2563eb; border-radius: 10px; color: white;
            box-sizing: border-box; font-size: 16px; outline: none;
        }
        input::placeholder {
            color: #888;
            text-transform: uppercase;
        }
        button {
            width: 100%; background: linear-gradient(to right, #00d2ff, #2563eb); color: white;
            padding: 14px; border: none; border-radius: 10px; cursor: pointer;
            font-size: 18px; font-weight: bold; margin-top: 10px;
            text-transform: uppercase;
        }
        .links { margin-top: 20px; font-size: 14px; }
        .links a { color: #00d2ff; text-decoration: none; text-transform: uppercase; }
        .links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="glow-card">
        <h2>REGISTER</h2>
        <form method="POST">
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
        </form>
        <div class="links">
            <a href="/">BACK TO LOGIN</a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        return f'WELCOME BACK, USER WITH EMAIL {email}!'
    return render_template_string(LOGIN_HTML)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        return f'ACCOUNT CREATED FOR {user}!'
    return render_template_string(REGISTER_HTML)

if __name__ == '__main__':
    app.run(debug=True)
