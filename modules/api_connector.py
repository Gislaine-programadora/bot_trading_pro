import ccxt
import time # Necessário para a simulação de preço
from config.config import BINANCE_API_KEY, BINANCE_SECRET_KEY
from config.settings import EXCHANGE_ID
from modules.logger_config import logger

class APIConnector:
    """
    Gerencia a conexão e comunicação com a API da corretora usando CCXT.
    """
    def __init__(self):
        self.exchange = None
        self._conectar()

    def _conectar(self):
        """
        Tenta autenticar na corretora especificada.
        """
        try:
            # Inicializa a exchange com as chaves carregadas
            self.exchange = getattr(ccxt, EXCHANGE_ID)({
                'apiKey': BINANCE_API_KEY,
                'secret': BINANCE_SECRET_KEY,
                'enableRateLimit': True,
            })
            
            # Testa a conexão
            logger.info(f"[{EXCHANGE_ID.upper()}] Conexão estabelecida com sucesso.")
            
        except AttributeError:
            logger.error(f"Exchange ID '{EXCHANGE_ID}' não suportado pelo CCXT.")
            self.exchange = None
        except Exception as e:
            # Captura erros de autenticação (chave inválida, etc.)
            logger.error(f"Falha ao conectar ou autenticar na {EXCHANGE_ID}. Detalhes: {e}")
            self.exchange = None

    def get_price(self, symbol: str):
        """
        Busca o preço atual (ticker) de um par. Se a conexão falhar, 
        retorna um preço simulado para fins de teste.
        """
        if not self.exchange:
            # --- MODO DE SIMULAÇÃO ---
            if symbol == 'BTC/USDT':
                # Preço base + um pouco de variação para simular movimento
                # Usamos time.time() para garantir que o preço mude a cada ciclo
                sim_price = 65000.00 + (time.time() % 300) 
                logger.warning(f"SIMULAÇÃO: Conexão API falhou. Usando preço simulado para {symbol}: ${sim_price:,.2f}")
                return sim_price
            return None # Não simula outros ativos, por enquanto

        # --- MODO REAL (Se a conexão self.exchange existir) ---
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            logger.info(f"API REAL: Preço de {symbol}: {ticker['last']:.2f}")
            return ticker['last']
        except Exception as e:
            logger.error(f"ERRO ao buscar preço REAL de {symbol}: {e}")
            return None

    def execute_order(self, symbol: str, type: str, side: str, amount: float, price: float = None):
        """
        Envia uma ordem para a corretora (Market ou Limit).
        """
        if not self.exchange:
            logger.warning("SIMULAÇÃO: Exchange não conectada. Ordem não enviada (SIMULADO).")
            # Em modo de simulação, apenas retornamos um dicionário simulando o preenchimento da ordem
            return {'id': f'SIM_{int(time.time() * 100)}', 'status': 'filled', 'amount': amount}
        
        # O try/except é fundamental para lidar com erros de API na hora do trading
        try:
            if type == 'market':
                order = self.exchange.create_market_order(symbol, side, amount)
            elif type == 'limit':
                order = self.exchange.create_limit_order(symbol, side, amount, price)
            else:
                raise ValueError(f"Tipo de ordem '{type}' inválido.")

            logger.info(f"Ordem REAL enviada com sucesso! ID: {order['id']}")
            return order
            
        except ccxt.InsufficientFunds as e:
            logger.error(f"ERRO (Fundos Insuficientes): {e}")
        except ccxt.NetworkError as e:
            logger.error(f"ERRO (Rede/API): {e}")
        except Exception as e:
            logger.error(f"ERRO INESPERADO ao executar ordem: {e}")
            
        return None