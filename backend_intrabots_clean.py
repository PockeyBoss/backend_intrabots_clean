
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/crear-bot", methods=["POST"])
def crear_bot():
    data = request.json

    plataforma = data.get("plataforma")       # "Telegram" o "WhatsApp"
    tipo = data.get("tipo")                   # Ej: "atencion", "turnos", etc.
    bienvenida = data.get("bienvenida")
    qa_pairs = data.get("qaPairs")

    if plataforma == "Telegram":
        token = data.get("token")
        print("\n[Telegram Bot Recibido]")
        print(f"Token: {token}")
    elif plataforma == "WhatsApp":
        numero = data.get("numero")
        print("\n[WhatsApp Bot Recibido]")
        print(f"Número: {numero}")
    else:
        return jsonify({"error": "Plataforma no válida"}), 400

    print(f"Tipo de bot: {tipo}")
    print(f"Mensaje de bienvenida: {bienvenida}")
    print("Preguntas y respuestas:")
    print(qa_pairs)

    return jsonify({"mensaje": "Datos recibidos correctamente"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
