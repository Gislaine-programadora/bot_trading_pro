🤖 CoinGPT Pro - Bot de Trading Algorítmico
Parabéns! Este projeto evoluiu de um script local para um sistema robusto de trading algorítmico, capaz de operar tanto no terminal quanto em uma interface web moderna e profissional.

O CoinGPT Pro é projetado para interagir em tempo real com a plataforma Binance, adaptando-se para o envio de ordens de mercado reais usando sua API Key.

✨ Vantagens Principais e Arquitetura
Este bot oferece duas grandes vantagens operacionais:

1. 🌐 Modo Web (Produção e Controle 24/7)
O bot pode ser iniciado e controlado através de uma interface web elegante (o Dashboard).

Arquivo de Início: web_app.py (servidor Flask).

Vantagem: Permite iniciar/parar o core de trading remotamente, visualizar o status e os logs em tempo real, e enviar ordens rápidas. Ideal para execução contínua em nuvem (Render).

2. 💻 Modo Terminal (Desenvolvimento e Debug)
O bot pode ser iniciado diretamente através da linha de comando, mostrando os logs diretamente no terminal.

Arquivo de Início: main.py.

Vantagem: Ideal para debug, testes locais e execução rápida sem a sobrecarga do servidor web.

🛠️ Tecnologias e Frameworks
Categoria

Tecnologia

Uso Principal

Linguagem Principal

Python

Core de trading, lógica algorítmica e backend (Flask).

Web Framework

Flask

Servidor web leve para expor APIs e servir o Dashboard.

Frontend

HTML, CSS, JavaScript

Dashboard moderno, responsivo e interativo.

Estilização

Bootstrap 5

Componentes e design profissional (Dark Mode).

Conexão API

CCXT

Comunicação unificada e estável com a Binance.

Banco de Dados

SQLite (via database_handler)

Armazenamento local de histórico de ordens e logs.

Hospedagem

Render.com

Execução contínua (Processo contínuo/Web Service).

📂 Estrutura do Projeto
A organização modular garante que cada componente do bot (API, Risco, Estratégia) possa ser desenvolvido e testado de forma independente.

bot_trading_pro/
├── config/                 # Arquivos de Configuração (Settings, .env)
├── data/                   # Arquivos gerados (Logs, Base de Dados SQLite)
├── modules/                # Módulos principais de lógica
│   ├── api_connector.py    # Conexão e Simulação com a Binance (CCXT)
│   ├── logger_config.py    # Configuração de Logs (saída para console e bot.log)
│   ├── risk_manager.py     # Lógica de Gestão de Risco (Stop Loss, Take Profit)
│   ├── strategy_engine.py  # Lógica de Geração de Sinais de Compra/Venda
│   └── database_handler.py # Gerenciamento do histórico e dados
├── web/                    # Interface Web
│   ├── static/             # Assets (CSS, JS)
│   │   ├── css/
│   │   └── js/
│   └── templates/          # Arquivos HTML (dashboard.html)
├── main.py                 # Ponto de entrada do Bot (Modo Terminal)
├── web_app.py              # Ponto de entrada do Servidor Web (Modo Produção/Render)
├── requirements.txt        # Dependências Python
├── Procfile                # Comando de Início para Render (web: gunicorn web_app:app)
└── package.json            # Scripts de Deploy e Metadados

🚀 Como Iniciar
1. Instalação de Dependências
Certifique-se de que o Python 3.x está instalado e execute o seguinte comando no seu ambiente virtual:

npm run build
# Ou, diretamente:
pip install -r requirements.txt

2. Configuração de API
Preencha seu arquivo .env com as chaves reais da Binance (ou deixe-o em branco para o modo de simulação/teste).

3. Execução
Modo Produção (Web/Render)
Inicia o servidor Flask para acessar o Dashboard via navegador.

npm start
# Ou, diretamente:
python web_app.py

Acesse http://127.0.0.1:5000 (localmente) ou o URL de produção.

Modo Terminal
Inicia o loop de trading diretamente no terminal (ignora o servidor web).

python main.py

🔗 Live Demo (Deploy na Nuvem)
Você pode acessar e interagir com o Dashboard de controle ativo na URL do Render:

URL Pública: https://bot-trading-pro-1.onrender.com