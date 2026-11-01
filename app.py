from flask import Flask, render_template_string, request

app = Flask(__name__)

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card {
            background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 300px; text-align: center;
        }
        h2 { color: #333; margin-bottom: 20px; font-weight: bold; }
        input {
            width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 8px;
            box-sizing: border-box; font-size: 16px;
        }
        .uppercase-input { text-transform: uppercase; }
        button {
            width: 100%; background-color: #ff4757; color: white; padding: 12px; border: none;
            border-radius: 8px; cursor: pointer; font-size: 18px; margin-top: 15px;
        }
        button:hover { background-color: #ff6b81; }
        .forgot-link {
            text-align: right; margin-bottom: 15px; font-size: 14px;
        }
        .forgot-link a { color: #57606f; text-decoration: none; }
        .forgot-link a:hover { text-decoration: underline; }
        .create-account { margin-top: 15px; font-size: 14px; }
        .create-account a { color: #ff4757; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>LOGIN</h2>
        <form method="POST">
            <input type="text" class="uppercase-input" name="email" placeholder="EMAIL ADDRESS" required>
            <input type="text" class="uppercase-input" name="password" placeholder="PASSWORD" required>
            <div class="forgot-link">
                <a href="#">Forgot password?</a>
            </div>
            <button type="submit">Login</button>
        </form>
        <div class="create-account">
            <a href="/register">Create account</a>
        </div>
    </div>
</body>
</html>
'''

REGISTER_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
    <style>
        body {
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;
            background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card {
            background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 300px; text-align: center;
        }
        h2 { color: #333; margin-bottom: 20px; font-weight: bold; }
        input {
            width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 8px;
            box-sizing: border-box; font-size: 16px;
        }
        .uppercase-input { text-transform: uppercase; }
        button {
            width: 100%; background-color: #2ed573; color: white; padding: 12px; border: none;
            border-radius: 8px; cursor: pointer; font-size: 18px; margin-top: 10px;
        }
        button:hover { background-color: #7bed9f; }
        .links { margin-top: 15px; font-size: 14px; }
        .links a { color: #57606f; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>REGISTER</h2>
        <form method="POST">
            <input type="text" class="uppercase-input" name="username" placeholder="USERNAME" required>
            <input type="text" class="uppercase-input" name="email" placeholder="EMAIL ADDRESS" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="password" name="confirm_password" placeholder="Confirm Password" required>
            <button type="submit">Register</button>
        </form>
        <div class="links">
            <a href="/">Back to Login</a>
        </div>
    </div>
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
