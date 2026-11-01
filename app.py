from flask import Flask, render_template_string, request

app = Flask(__name__)

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
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
        .glow-card::before, .glow-card::after {
            content: '';
            position: absolute;
            inset: -3px;
            border-radius: 23px;
            background: conic-gradient(from var(--angle), #ff4757, #2ed573, #1e90ff, #fffb00, #ff4757);
            animation: rotate 4s linear infinite;
            z-index: -1;
        }
        .glow-card::after {
            filter: blur(15px);
            opacity: 0.8;
        }
        h2 { color: #fff; margin-bottom: 25px; font-weight: bold; letter-spacing: 1px; }
        .input-group {
            position: relative; margin-bottom: 20px;
        }
        input {
            width: 100%; padding: 14px 40px 14px 15px; background: #16213e;
            border: 1px solid #533483; border-radius: 10px; color: white;
            box-sizing: border-box; font-size: 16px; outline: none;
        }
        input:focus { border-color: #2ed573; }
        .toggle-password {
            position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
            background: none; border: none; color: #888; cursor: pointer; font-size: 16px;
        }
        button {
            width: 100%; background: linear-gradient(to right, #ff4757, #ff6b81); color: white;
            padding: 14px; border: none; border-radius: 10px; cursor: pointer;
            font-size: 18px; font-weight: bold; margin-top: 10px; box-shadow: 0 4px 15px rgba(255,71,87,0.4);
        }
        .links { margin-top: 20px; font-size: 14px; display: flex; justify-content: space-between; }
        .links a { color: #4ecca3; text-decoration: none; }
        .links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="glow-card">
        <h2>LOGIN</h2>
        <form method="POST">
            <div class="input-group">
                <input type="text" name="email" placeholder="Email Address" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="login-pass" placeholder="Password" required>
                <button type="button" class="toggle-password" onclick="togglePass('login-pass')">👁️</button>
            </div>
            <div class="links" style="justify-content: flex-end;">
                <a href="#">Forgot password?</a>
            </div>
            <button type="submit">Login</button>
        </form>
        <div class="links">
            <span>Don't have an account? <a href="/register">Sign up</a></span>
        </div>
    </div>

    <script>
        function togglePass(id) {
            const input = document.getElementById(id);
            if (input.type === "password") {
                input.type = "text";
            } else {
                input.type = "password";
            }
        }
    </script>
</body>
</html>
'''

REGISTER_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
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
        .glow-card::before, .glow-card::after {
            content: '';
            position: absolute;
            inset: -3px;
            border-radius: 23px;
            background: conic-gradient(from var(--angle), #ff4757, #2ed573, #1e90ff, #fffb00, #ff4757);
            animation: rotate 4s linear infinite;
            z-index: -1;
        }
        .glow-card::after {
            filter: blur(15px);
            opacity: 0.8;
        }
        h2 { color: #fff; margin-bottom: 25px; font-weight: bold; letter-spacing: 1px; }
        .input-group {
            position: relative; margin-bottom: 20px;
        }
        input {
            width: 100%; padding: 14px 40px 14px 15px; background: #16213e;
            border: 1px solid #533483; border-radius: 10px; color: white;
            box-sizing: border-box; font-size: 16px; outline: none;
        }
        input:focus { border-color: #2ed573; }
        .toggle-password {
            position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
            background: none; border: none; color: #888; cursor: pointer; font-size: 16px;
        }
        button {
            width: 100%; background: linear-gradient(to right, #2ed573, #26af5a); color: white;
            padding: 14px; border: none; border-radius: 10px; cursor: pointer;
            font-size: 18px; font-weight: bold; margin-top: 10px; box-shadow: 0 4px 15px rgba(46,213,115,0.4);
        }
        .links { margin-top: 20px; font-size: 14px; }
        .links a { color: #4ecca3; text-decoration: none; }
        .links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="glow-card">
        <h2>REGISTER</h2>
        <form method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="input-group">
                <input type="text" name="email" placeholder="Email Address" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="reg-pass" placeholder="Password" required>
                <button type="button" class="toggle-password" onclick="togglePass('reg-pass')">👁️</button>
            </div>
            <div class="input-group">
                <input type="password" name="confirm_password" id="conf-pass" placeholder="Confirm Password" required>
                <button type="button" class="toggle-password" onclick="togglePass('conf-pass')">👁️</button>
            </div>
            <button type="submit">Register</button>
        </form>
        <div class="links">
            <a href="/">Back to Login</a>
        </div>
    </div>

    <script>
        function togglePass(id) {
            const input = document.getElementById(id);
            if (input.type === "password") {
                input.type = "text";
            } else {
                input.type = "password";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        return f'Welcome back, user with email {email}!'
    return render_template_string(LOGIN_HTML)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        return f'Account created for {user}!'
    return render_template_string(REGISTER_HTML)

if __name__ == '__main__':
    app.run(debug=True)
