import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='data/logs/bot.log', level=logging.INFO):
    """Configura o sistema de logging do bot."""
    
    # Cria o diretório de logs se não existir
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configuração básica do logger
    logger = logging.getLogger('TradingBot')
    logger.setLevel(level)

    # 1. Handler para o arquivo de log (Rolling File Handler)
    # Roda o arquivo de log para um máximo de 1MB e mantém 3 arquivos de backup
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024, # 1 MB
        backupCount=3
    )
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # 2. Handler para o console (terminal)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    # Adiciona os handlers ao logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Inicializa o logger para ser importado em outros módulos
logger = setup_logging()