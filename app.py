from flask import Flask, render_template_string, request

app = Flask(__name__)

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login Page</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <br>
    <a href="#">Create new account</a> | <a href="#">Forgot password?</a>
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
