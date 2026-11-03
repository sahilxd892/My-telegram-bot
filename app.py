from flask import Flask
import time
import random
import qrcode
app = Flask(__name__)
@app.route('/')
def home():
    return "QR Code Generator is working!"

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
