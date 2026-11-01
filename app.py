from flask import Flask, render_template_string, request

app = Flask(__name__)

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 50%, #A1C4FD 100%);
            font-family: 'Segoe UI', Tahoma, Verdana, sans-serif;
        }
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 320px;
            text-align: center;
        }
        h2 {
            color: #333;
            margin-bottom: 25px;
        }
        input[type="text"], input[type="email"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 16px;
        }
        .uppercase-input {
            text-transform: uppercase;
        }
        button {
            width: 100%;
            background: linear-gradient(to right, #ff758c, #ff7eb3);
            color: white;
            padding: 12px;
            margin: 15px 0;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
        }
        button:hover {
            opacity: 0.9;
        }
        .links {
            margin-top: 15px;
            font-size: 14px;
        }
        .links a {
            color: #ff758c;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" class="uppercase-input" name="email" placeholder="EMAIL ADDRESS" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="links">
            <a href="#">Create account</a> | <a href="#">Forgot password?</a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        return f'Hello {user}!'
    return render_template_string(LOGIN_HTML)

if __name__ == '__main__':
    app.run(debug=True)
