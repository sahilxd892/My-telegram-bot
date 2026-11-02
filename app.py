from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Secure Portal</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .auth-box { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 300px; }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #5c67f2; border: none; border-radius: 4px; color: white; font-size: 16px; cursor: pointer; }
        .toggle-btn { text-align: center; margin-top: 15px; font-size: 14px; }
        .toggle-btn a { color: #5c67f2; text-decoration: none; cursor: pointer; }
        .form-group { display: none; }
        .active-form { display: block; }
    </style>
</head>
<body>

<div class="auth-box">
    <div id="login-form" class="form-group active-form">
        <h2>Login</h2>
        <form action="/login" method="POST">
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="toggle-btn">Don't have an account? <a onclick="toggleForm()">Create Account</a></div>
    </div>

    <div id="register-form" class="form-group">
        <h2>Create Account</h2>
        <form action="/register" method="POST">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="password" name="confirm_password" placeholder="Confirm Password" required>
            <button type="submit">Register</button>
        </form>
        <div class="toggle-btn">Already have an account? <a onclick="toggleForm()">Login here</a></div>
    </div>
</div>

<script>
    function toggleForm() {
        document.getElementById('login-form').classList.toggle('active-form');
        document.getElementById('register-form').classList.toggle('active-form');
    }
</script>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(PAGE_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    return "Logged in successfully!"

@app.route('/register', methods=['POST'])
def register():
    return "Registered successfully!"

if __name__ == '__main__':
    app.run(debug=True)
