from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; margin: 0; }
        .box { background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 300px; text-align: center; }
        p { color: #666; font-size: 14px; margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .btn { display: block; width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 4px; margin-top: 15px; text-decoration: none; font-size: 16px; cursor: pointer; }
        .forgot-link { text-align: right; margin-top: 5px; font-size: 12px; }
        .forgot-link a, .create-link a { color: #007bff; text-decoration: none; }
        .create-link { text-align: center; margin-top: 15px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="box">
        <p>Login</p>
        <form action="#" method="POST">
            <input type="text" placeholder="Email" required>
            <input type="password" placeholder="Password" required>
            <div class="forgot-link">
                <a href="#">Forgot Password?</a>
            </div>
            <button type="submit" class="btn">Sign In</button>
            <div class="create-link">
                <a href="#">Create Account</a>
            </div>
        </form>
    </div>
</body>
</html>''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
