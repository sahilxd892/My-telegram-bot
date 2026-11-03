from flask import Flask, render_template_string
import time
import random
import qrcode

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; margin: 0; }
        h1 { color: #333; margin-bottom: 20px; }
        .box { background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 300px; text-align: center; }
        p { color: #666; font-size: 14px; margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .btn { display: block; width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 4px; margin-top: 15px; text-decoration: none; font-size: 16px; cursor: pointer; }
        .links { margin-top: 15px; font-size: 12px; }
        .links a { color: #007bff; text-decoration: none; margin: 0 5px; }
    </style>
</head>
<body>
    <h1>Login</h1>
    <div class="box">
        <p>Instant delivery guaranteed upon payment verification.</p>
        <form action="#" method="POST">
            <input type="text" placeholder="Email" required>
            <input type="password" placeholder="Password" required>
            <button type="submit" class="btn">Sign In</button>
        </form>
        <div class="links">
            <a href="#">Forgot Password?</a> | <a href="#">Create Account</a>
        </div>
    </div>
</body>
</html>''')




def generate_order_id():
    return "ORD-" + str(int(time.time())) + "-" + str(random.randint(1000, 9999))

def generate_qr(order_id, amount):
    qr_data = f"Order ID: {order_id}, Amount: {amount}"
    qr = qrcode.make(qr_data)
    qr.save(f"qr_{order_id}.png")
order_id = generate_order_id()
generate_qr(order_id, 100)
print(f"Generated Order ID: {order_id}")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
