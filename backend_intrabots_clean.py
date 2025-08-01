from flask import Flask, request, jsonify
import threading
import requests
import time

app = Flask(__name__)

# Diccionario para manejar múltiples bots
bots_activos = {}

@app.route("/", methods=["GET"])
def home():
    return "Backend IntraBots funcionando (Telegram Real)"

@app.route("/api/crear-bot", methods=["POST"])
def crear_bot():
    data = request.get_json()
    token = data.get("token")
    respuestas = data.get("respuestas", {})  # dict: {"hola": "¡Hola! ¿En qué puedo ayudarte?"}
    
    # Verificar token con getMe
    info = requests.get(f"https://api.telegram.org/bot{token}/getMe")
    if not info.ok or not info.json().get("ok"):
        return jsonify({"status": "error", "message": "Token inválido"}), 400

    if token in bots_activos:
        return jsonify({"status": "ok", "message": "Bot ya activo"}), 200

    # Listener simple con long polling
    def responder():
        offset = None
        while True:
            try:
                url = f"https://api.telegram.org/bot{token}/getUpdates"
                if offset:
                    url += f"?offset={offset}"
                res = requests.get(url).json()

                for update in res.get("result", []):
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "").lower()
                    respuesta = respuestas.get(text)
                    if respuesta:
                        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={
                            "chat_id": chat_id,
                            "text": respuesta
                        })
                time.sleep(1)
            except Exception as e:
                print("Error en listener:", e)
                time.sleep(5)

    hilo = threading.Thread(target=responder, daemon=True)
    hilo.start()
    bots_activos[token] = hilo

    return jsonify({"status": "ok", "message": "Bot creado y funcionando"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)