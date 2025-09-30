import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import ccxt
from dotenv import load_dotenv

# Carregar variáveis de ambiente (.env)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Estado do bot
bot_status = {
    "running": False,
    "last_order": None
}

# Configuração da Binance via CCXT
binance = ccxt.binance({
    "apiKey": os.getenv("BINANCE_API_KEY"),
    "secret": os.getenv("BINANCE_API_SECRET"),
    "enableRateLimit": True,
    "options": {"defaultType": "spot"}  # Pode mudar para "future" se for Futuros
})

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
    amount = float(data.get("amount", 0.001))

    try:
        # Criar ordem de mercado na Binance
        order = binance.create_market_order(symbol, side, amount)

        bot_status["last_order"] = order
        return jsonify({"message": "📈 Ordem executada com sucesso", "order": order})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)