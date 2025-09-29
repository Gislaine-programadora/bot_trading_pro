from config.settings import RISK_PER_TRADE_PERCENT, STOP_LOSS_DEFAULT_PERCENT
from config.config import INITIAL_CAPITAL # Carregamos o capital do .env

class RiskManager:
    """
    Gerencia o tamanho da posição e as regras de Stop Loss/Take Profit.
    """
    def __init__(self):
        # O saldo aqui deve ser obtido do APIConnector no futuro
        # Por enquanto, usamos o capital inicial do .env
        self.current_capital = float(INITIAL_CAPITAL)
        print(f"Gestor de Risco inicializado. Capital: ${self.current_capital:,.2f}")

    def calculate_position_size(self, symbol: str, price: float):
        """
        Calcula o tamanho da posição (em USD ou quantidade de moeda) 
        com base no risco definido.
        """
        # 1. Calcular o risco máximo em USD
        max_risk_usd = self.current_capital * RISK_PER_TRADE_PERCENT
        
        # 2. Definir o Stop Loss (Em porcentagem)
        # Assumindo que o Stop Loss será de 2%
        sl_percent = STOP_LOSS_DEFAULT_PERCENT
        
        # 3. Calcular o tamanho da posição (alocação)
        # Fórmula simplificada: Posição = Risco Máximo / Risco por unidade
        # Se você arrisca 1% (Risco Máximo) e tem um SL de 2% (Risco por unidade),
        # você pode alocar 1% / 2% = 50% do capital (Simplificado para fins de demonstração)
        
        # Usaremos uma alocação simples de 10% do capital por trade:
        allocation_usd = self.current_capital * 3000
        
        # 4. Converter USD para a quantidade da moeda
        amount_coin = allocation_usd / price
        
        print(f"Tamanho de Posição: Alocação USD: ${allocation_usd:,.2f} | Moeda: {amount_coin:.6f}")
        return amount_coin

    def set_stop_loss_price(self, entry_price: float, side: str):
        """
        Calcula o preço do Stop Loss (SL) com base na porcentagem de risco.
        """
        sl_percent = STOP_LOSS_DEFAULT_PERCENT
        
        if side == 'BUY':
            # SL para Compra (abaixo do preço de entrada)
            sl_price = entry_price * (1 - sl_percent)
        elif side == 'SELL':
            # SL para Venda (acima do preço de entrada)
            sl_price = entry_price * (1 + sl_percent)
        else:
            return None
            
        return sl_price