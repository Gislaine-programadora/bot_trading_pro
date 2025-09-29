import os
from dotenv import load_dotenv

# Esta linha carrega o .env
load_dotenv() 

# --- As chaves API ---
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# ESTA LINHA DEVE ESTAR AQUI para que o risk_manager possa importá-la
INITIAL_CAPITAL = os.getenv("INITIAL_CAPITAL")