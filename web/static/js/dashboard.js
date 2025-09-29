let botActive = false;

function updateStatus(active) {
    const statusElement = document.getElementById('bot-status');
    botActive = active;
    if (active) {
        statusElement.textContent = 'ATIVO';
        statusElement.className = 'header-status status-active';
    } else {
        statusElement.textContent = 'INATIVO';
        statusElement.className = 'header-status status-inactive';
    }
}

function log(message, level = 'INFO') {
    const logFeed = document.getElementById('log-feed');
    const now = new Date().toLocaleTimeString();
    let color = 'text-light';
    if (level === 'ERROR') color = 'text-danger';
    if (level === 'WARNING') color = 'text-warning';
    if (level === 'SIGNAL') color = 'text-info';

    const newLog = document.createElement('p');
    newLog.className = `${color} mb-0`;
    newLog.innerHTML = `[${now}] <strong>${level}</strong>: ${message}`;
    logFeed.prepend(newLog); // Adiciona no topo
}

// ----------------------------------------------------------------
// FUNÇÕES QUE CHAMAM O PYTHON (O Flask responderá a estas chamadas)
// ----------------------------------------------------------------

async function startBot() {
    if (botActive) {
        log('Bot já está ativo.', 'WARNING');
        return;
    }
    log('Enviando comando de INÍCIO para o servidor...', 'INFO');
    
    // Chama o endpoint /api/start no nosso servidor Flask
    const response = await fetch('/api/start', { method: 'POST' });
    const data = await response.json();
    
    if (data.status === 'success') {
        updateStatus(true);
        log('Bot Core iniciado e rodando!', 'INFO');
    } else {
        log(`Falha ao iniciar: ${data.message}`, 'ERROR');
    }
}

async function stopBot() {
    if (!botActive) {
        log('Bot já está inativo.', 'WARNING');
        return;
    }
    log('Enviando comando de PARADA para o servidor...', 'INFO');
    
    const response = await fetch('/api/stop', { method: 'POST' });
    const data = await response.json();
    
    if (data.status === 'success') {
        updateStatus(false);
        log('Bot Core parado com sucesso.', 'INFO');
    } else {
        log(`Falha ao parar: ${data.message}`, 'ERROR');
    }
}

function sendMarketOrder(side) {
    // ... (Lógica de envio de ordem similar à anterior, mas com Fetch)
    log(`${side} de mercado simulada.`, 'SIGNAL');
}

// ----------------------------------------------------------------
// FUNÇÕES DE ATUALIZAÇÃO DE DADOS (Polling)
// ----------------------------------------------------------------

// Simula a busca de dados do backend (a cada 2 segundos)
async function fetchBotData() {
    // Aqui você faria uma chamada para buscar o preço, saldo e logs
    // const response = await fetch('/api/data');
    // const data = await response.json();
    
    // Simulação de atualização de preço
    const priceBTC = (65000 + (Math.random() * 50)).toFixed(2);
    document.getElementById('quote-BTC/USDT').textContent = `$ ${priceBTC}`;
    
    // Simulação de log
    if (botActive && Math.random() < 0.2) {
        log(`[Simulação] Preço atualizado: ${priceBTC}`, 'INFO');
    }

    // Você deve manter o status em sincronia
    // updateStatus(data.is_active); 
}

// Roda a atualização de dados a cada 2 segundos
setInterval(fetchBotData, 2000); 

// Inicializa o estado
document.addEventListener('DOMContentLoaded', () => {
    updateStatus(false);
});