import threading
from flask import Flask, render_template, jsonify
from modules.api_connector import APIConnector
from modules.strategy_engine import StrategyEngine
from modules.risk_manager import RiskManager
from modules.database_handler import DatabaseHandler
from modules.logger_config import logger # Já configurado

# --- 1. CONFIGURAÇÃO GLOBAL ---
app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

# Instância global do bot (O coração que o site irá controlar)
# Inicializamos sem a lógica principal rodando
BOT_CORE = None
BOT_THREAD = None # Thread para rodar o bot em segundo plano

def initialize_bot_core():
    """Inicializa as classes do bot, mas sem iniciar o loop de trading."""
    global BOT_CORE
    # O logger já foi configurado, então a inicialização é logada
    BOT_CORE = type('TempBot', (object,), {
        'api': APIConnector(),
        'risk_manager': RiskManager(),
        'strategy': StrategyEngine(APIConnector()),
        'db': DatabaseHandler(),
        'is_running': False,
        'main_loop': lambda: logger.info("Loop de trading iniciado na thread!"),
        'start': lambda: logger.info("Bot Start Chamado!"),
        'stop': lambda: logger.info("Bot Stop Chamado!"),
    })() # Esta é uma inicialização SIMULADA/Dummy, substituiríamos pelo TradingBotCore REAL

# Substitua o código acima por esta linha QUANDO FOR USAR O CÓDIGO REAL:
# from main import TradingBotCore as BOT_CORE_REAL
# BOT_CORE = BOT_CORE_REAL() 
    
def run_bot_in_thread():
    """Função para ser executada em uma thread separada."""
    global BOT_CORE
    # Na versão real, você chamaria BOT_CORE.main_loop() aqui.
    BOT_CORE.start() # Inicia o loop (no código real, esta função faria o while True)
    
    # Para demonstração: Rodar um loop dummy para mostrar que a thread está viva
    try:
        while BOT_CORE.is_running:
            logger.info("Thread do Bot Core rodando...")
            time.sleep(10)
    except Exception as e:
        logger.error(f"Erro na thread principal: {e}")
    finally:
        BOT_CORE.stop()
        logger.info("Thread do Bot Core encerrada.")


# --- 2. ROTAS DO FLASK ---

@app.route('/')
def index():
    """Rota principal que serve o dashboard."""
    return render_template('dashboard.html')

@app.route('/api/start', methods=['POST'])
def start_bot_api():
    """Inicia o loop principal do bot em uma thread separada."""
    global BOT_THREAD, BOT_CORE
    if BOT_THREAD and BOT_THREAD.is_alive():
        return jsonify({"status": "error", "message": "Bot já está rodando."})
    
    # Reinicializa se o BOT_CORE.start() foi chamado antes
    # Aqui, na versão real, você garantiria que o bot core está pronto.
    
    BOT_CORE.is_running = True
    BOT_THREAD = threading.Thread(target=run_bot_in_thread)
    BOT_THREAD.start()
    
    logger.info("Comando de START recebido via Web. Bot thread iniciada.")
    return jsonify({"status": "success", "message": "Bot iniciado."})

@app.route('/api/stop', methods=['POST'])
def stop_bot_api():
    """Para o loop principal do bot."""
    global BOT_CORE
    if BOT_CORE is None or not BOT_CORE.is_running:
        return jsonify({"status": "error", "message": "Bot não estava rodando."})

    BOT_CORE.is_running = False # Envia o sinal de parada para o loop
    # O BOT_CORE.stop() será chamado pelo bloco 'finally' da thread
    logger.info("Comando de STOP recebido via Web. Sinal enviado.")
    return jsonify({"status": "success", "message": "Bot sinalizado para parar."})

@app.route('/api/data')
def get_bot_data():
    """Retorna dados de status, preço e saldo."""
    # Aqui você leria o log, buscaria o saldo do BOT_CORE, e o preço
    return jsonify({
        "status": "active" if BOT_THREAD and BOT_THREAD.is_alive() else "inactive",
        "pnl": "+420.69",
        "latest_price": BOT_CORE.api.get_price('BTC/USDT') # Simulação
    })

# --- 3. EXECUÇÃO ---

if __name__ == '__main__':
    # Inicializa as classes do bot antes de iniciar o servidor web
    initialize_bot_core() 
    logger.info("Servidor Flask inicializado. Acesse http://127.0.0.1:5000")
    # A thread principal (o servidor web) roda na porta 5000
    app.run(debug=True, use_reloader=False)