from flask import Flask, render_template_string, request

app = Flask(__name__)

# UPDATED CSS AND HTML TEMPLATES WITH HIGHLY VISIBLE BORDER AND CAPITALIZED TEXT

BASE_STYLE = '''
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
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: linear-gradient(135deg, #0a0a16 0%, #1a1a2e 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .glow-card {
        position: relative;
        background: #0f3460;
        padding: 40px;
        border-radius: 20px;
        width: 320px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .glow-card::before {
        content: '';
        position: absolute;
        inset: -6px;
        border-radius: 24px;
        background: conic-gradient(from var(--angle), #00d2ff, #0052ff, #00d2ff, #00f2fe, #00d2ff);
        animation: rotate 8s linear infinite; /* Slower rotation */
        z-index: -1;
    }
    h2 {
        color: #fff;
        margin-bottom: 30px;
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .input-group {
        margin-bottom: 25px;
        text-align: left;
    }
    input {
        width: 100%;
        padding: 15px;
        background: #16213e;
        border: 2px solid transparent; /* Invisible border when empty */
        border-radius: 12px;
        color: white;
        box-sizing: border-box;
        font-size: 16px;
        outline: none;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        text-transform: uppercase; /* Typed text strictly uppercase */
    }
    input::placeholder {
        color: #666; /* Visible placeholder */
        text-transform: uppercase; /* Placeholder strictly uppercase */
        opacity: 1;
    }
    input:focus {
        border-color: #00d2ff; /* Bright blue border on click */
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
        transition: transform 0.1s;
    }
    button:active {
        transform: scale(0.98);
    }
    .links {
        margin-top: 25px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
    }
    .links a {
        color: #00d2ff;
        text-decoration: none;
        text-transform: uppercase;
        font-weight: 500;
    }
    .links a:hover {
        text-decoration: underline;
    }
</style>
'''

LOGIN_HTML = f'''
<!DOCTYPE html>
<html>
<head>
    <title>LOGIN</title>
    {BASE_STYLE}
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

REGISTER_HTML = f'''
<!DOCTYPE html>
<html>
<head>
    <title>REGISTER</title>
    {BASE_STYLE}
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
