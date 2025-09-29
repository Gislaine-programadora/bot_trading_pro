# Lista de ativos que o bot deve monitorar
WATCHLIST = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']

# Parâmetros da estratégia
RSI_PERIOD = 14
MOVING_AVERAGE_PERIOD = 50

# Parâmetros de risco
RISK_PER_TRADE_PERCENT = 0.01  # Ex: arriscar no máximo 1% do capital por trade
STOP_LOSS_DEFAULT_PERCENT = 0.02 # Stop Loss padrão de 2%

# Configuração da corretora
EXCHANGE_ID = 'binance' # Ou 'mercadobitcoin', 'bybit', etc.