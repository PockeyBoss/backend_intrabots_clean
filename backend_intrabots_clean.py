import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Backend IntraBots funcionando"

@app.route('/api/crear-bot', methods=['POST'])
def crear_bot():
    data = request.get_json()
    print("Datos recibidos:", data)
    return jsonify({"status": "ok", "mensaje": "Bot creado correctamente"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)