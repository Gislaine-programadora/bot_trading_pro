import sqlite3
import datetime

# Nome do arquivo do banco de dados (será criado na raiz do projeto)
DB_NAME = 'trading_data.db'

class DatabaseHandler:
    """
    Gerencia a conexão e as operações CRUD (Create, Read, Update, Delete) 
    para armazenar dados de trades e a carteira do bot.
    """
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._conectar()
        self._criar_tabelas()

    def _conectar(self):
        """ Estabelece a conexão com o arquivo SQLite. """
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()
            print(f"Banco de dados SQLite conectado: {DB_NAME}")
        except sqlite3.Error as e:
            print(f"ERRO ao conectar ao banco de dados: {e}")

    def _criar_tabelas(self):
        """ Cria as tabelas de `trades` e `wallet` se elas não existirem. """
        
        # Tabela para registrar cada trade executado
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                price REAL NOT NULL,
                fee REAL,
                status TEXT
            );
        """)

        # Tabela para rastrear a posição atual da carteira
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallet (
                asset TEXT PRIMARY KEY,
                available_balance REAL NOT NULL,
                locked_balance REAL NOT NULL,
                last_updated TEXT
            );
        """)
        self.conn.commit()
        print("Tabelas de Trades e Wallet verificadas/criadas.")

    def log_trade(self, symbol, side, type, amount, price, fee=0.0, status="FILLED"):
        """
        Registra uma transação no banco de dados.
        """
        timestamp = datetime.datetime.now().isoformat()
        try:
            self.cursor.execute("""
                INSERT INTO trades (timestamp, symbol, side, type, amount, price, fee, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (timestamp, symbol, side, type, amount, price, fee, status))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"ERRO ao registrar trade: {e}")
            return False

    def update_wallet(self, asset: str, balance: float, locked: float = 0.0):
        """
        Atualiza o saldo de um ativo na tabela 'wallet'.
        """
        timestamp = datetime.datetime.now().isoformat()
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO wallet (asset, available_balance, locked_balance, last_updated)
                VALUES (?, ?, ?, ?);
            """, (asset, balance, locked, timestamp))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"ERRO ao atualizar carteira: {e}")
            
    def close(self):
        """ Fecha a conexão com o banco de dados. """
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")

# --- Exemplo de Integração no main.py (Futuro) ---
# Você precisará chamar o `log_trade` após cada `execute_order` bem-sucedido 
# e chamar `update_wallet` após obter o saldo da API.