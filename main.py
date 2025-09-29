import time
from modules.api_connector import APIConnector
from modules.strategy_engine import StrategyEngine
from modules.risk_manager import RiskManager
from modules.database_handler import DatabaseHandler
from modules.logger_config import logger # <-- NOVA IMPORTAÇÃO
from config.settings import WATCHLIST

class TradingBotCore:
    def __init__(self):
        self.api = APIConnector()
        self.risk_manager = RiskManager()
        self.strategy = StrategyEngine(self.api)
        self.db = DatabaseHandler()
        self.is_running = False
        logger.info("\n--- CORE DO BOT PRONTO PARA INICIAR ---")

    def start(self):
        """ Inicia o loop principal de execução. """
        self.is_running = True
        logger.info("\n>>> BOT ATIVO. INICIANDO CICLOS DE TRADING...")
        self.main_loop()

    def stop(self):
        """ Para o bot de forma limpa. """
        self.is_running = False
        logger.info("\n<<< BOT PARADO. Encerrando operações...")
        self.db.close() # Garante que o banco de dados é fechado

    def main_loop(self):
        """ O loop infinito onde a mágica acontece. """
        while self.is_running:
            try:
                for symbol in WATCHLIST:
                    # 1. Obter o preço atual
                    current_price = self.api.get_price(symbol)
                    
                    if current_price is None:
                        logger.warning(f"Não foi possível obter preço para {symbol}. Pulando ciclo.")
                        continue 
                        
                    logger.info(f"Monitorando {symbol} @ ${current_price:,.2f}")

                    # 2. Gerar sinal de trading
                    signal = self.strategy.generate_signal(symbol, current_price)

                    if signal == 'BUY':
                        # 3. Calcular tamanho da posição e SL/TP
                        amount_to_buy = self.risk_manager.calculate_position_size(symbol, current_price)
                        sl_price = self.risk_manager.set_stop_loss_price(current_price, 'BUY')
                        
                        # 4. Executar Ordem (Usando Ordem a Mercado para simplicidade)
                        order_result = self.api.execute_order(symbol, 'market', 'buy', amount_to_buy)
                        
                        if order_result and order_result.get('status') == 'filled':
                            logger.info(f"COMPRA EXECUTADA! Ordem ID: {order_result['id']}. SL Definido: ${sl_price:,.2f}")
                            # 5. Logar o trade (A ser aprimorado com dados reais da ordem)
                            self.db.log_trade(symbol, 'buy', 'market', amount_to_buy, current_price)

                    elif signal == 'SELL':
                         # Lógica para vender (similar à compra)
                         amount_to_sell_usd = 50 
                         amount_to_sell = amount_to_sell_usd / current_price 
                         order_result = self.api.execute_order(symbol, 'market', 'sell', amount_to_sell)
                         
                         if order_result and order_result.get('status') == 'filled':
                            logger.info(f"VENDA EXECUTADA! Ordem ID: {order_result['id']}")
                            self.db.log_trade(symbol, 'sell', 'market', amount_to_sell, current_price)

                # Espera 10 segundos antes do próximo ciclo
                time.sleep(10) 

            except Exception as e:
                logger.critical(f"\nERRO CRÍTICO no Loop Principal: {e}")
                self.stop() # Parada de emergência

# --- EXECUÇÃO ---
if __name__ == "__main__":
    bot_core = TradingBotCore()
    
    try:
        bot_core.start()
        
        # O bot vai rodar por 60 segundos em modo de simulação
        logger.info("Rodando simulação por 60 segundos...")
        time.sleep(60) 

    except KeyboardInterrupt:
        logger.info("\nInterrupção do usuário (Ctrl+C).")
    finally:
        bot_core.stop()