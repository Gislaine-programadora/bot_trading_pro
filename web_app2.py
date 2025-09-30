from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir acesso do frontend (Vercel)

# Estado do bot (simulação inicial)
bot_status = {
    "running": False,
    "last_order": None
}

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify(bot_status)

@app.route("/api/start", methods=["POST"])
def start_bot():
    global bot_status
    if not bot_status["running"]:
        bot_status["running"] = True
        return jsonify({"message": "Bot iniciado com sucesso 🚀", "status": bot_status})
    else:
        return jsonify({"message": "Bot já está em execução ⚠️", "status": bot_status})

@app.route("/api/stop", methods=["POST"])
def stop_bot():
    global bot_status
    if bot_status["running"]:
        bot_status["running"] = False
        return jsonify({"message": "Bot parado com sucesso 🛑", "status": bot_status})
    else:
        return jsonify({"message": "Bot já estava parado ⚠️", "status": bot_status})

@app.route("/api/order", methods=["POST"])
def place_order():
    global bot_status
    data = request.get_json()
    symbol = data.get("symbol", "BTC/USDT")
    side = data.get("side", "buy")
    amount = data.get("amount", 0.001)

    # Aqui entraria a lógica real de envio de ordem (ex: via Binance API com CCXT)
    order_info = {
        "symbol": symbol,
        "side": side,
        "amount": amount,
        "status": "executed"
    }

    bot_status["last_order"] = order_info
    return jsonify({"message": "📈 Ordem processada com sucesso", "order": order_info})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
