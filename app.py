from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); width: 250px; }
        p { color: #666; font-size: 14px; margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; display: block; box-sizing: border-box; }
        .password-container { position: relative; width: 100%; }
        .password-container input { padding-right: 40px; }
        #eye-icon { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; user-select: none; }
        .btn { display: block; width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .forgot-link { text-align: right; margin-top: 5px; font-size: 12px; }
        .forgot-link a { color: #007bff; text-decoration: none; }
        .create-link { text-align: center; margin-top: 15px; font-size: 12px; }
        .create-link a { color: #007bff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="box">
        <p>Login</p>
        <form action="#" method="POST">
            <input type="text" placeholder="Email" required>
            <div class="password-container">
                <input type="password" id="password" placeholder="Password" required>
                <span id="eye-icon" onclick="togglePassword()">👁️</span>
            </div>
            <button type="submit" class="btn">Sign In</button>
        </form>
        <div class="forgot-link">
            <a href="#">Forgot Password?</a>
        </div>
        <div class="create-link">
            <a href="#">Create Account</a>
        </div>
    </div>
    <script>
        function togglePassword() {
            var passwordInput = document.getElementById("password");
            var eyeIcon = document.getElementById("eye-icon");
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                eyeIcon.textContent = "🙈";
            } else {
                passwordInput.type = "password";
                eyeIcon.textContent = "👁️";
            }
        }
    </script>
</body>
</html>


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
