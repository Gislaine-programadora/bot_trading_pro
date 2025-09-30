
const API_URL = "https://bot-trading-pro-1.onrender.com"; // Backend Flask no Render

// Carregar status do bot
async function carregarStatus() {
  try {
    const resposta = await fetch(`${API_URL}/api/status`);
    const dados = await resposta.json();
    document.getElementById("status").textContent = JSON.stringify(dados, null, 2);
  } catch (erro) {
    document.getElementById("status").textContent = "Erro ao conectar ao servidor.";
  }
}

// Iniciar Bot
async function iniciarBot() {
  try {
    const resposta = await fetch(`${API_URL}/api/start`, { method: "POST" });
    const dados = await resposta.json();
    alert("✅ Bot iniciado: " + JSON.stringify(dados));
    carregarStatus();
  } catch (erro) {
    alert("Erro ao iniciar bot.");
  }
}

// Parar Bot
async function pararBot() {
  try {
    const resposta = await fetch(`${API_URL}/api/stop`, { method: "POST" });
    const dados = await resposta.json();
    alert("🛑 Bot parado: " + JSON.stringify(dados));
    carregarStatus();
  } catch (erro) {
    alert("Erro ao parar bot.");
  }
}

// Enviar Ordem de Teste
async function enviarOrdem() {
  try {
    const resposta = await fetch(`${API_URL}/api/order`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: "BTC/USDT", side: "buy", amount: 0.001 })
    });
    const dados = await resposta.json();
    alert("📈 Ordem enviada: " + JSON.stringify(dados));
  } catch (erro) {
    alert("Erro ao enviar ordem.");
  }
}

async function startBot() {
  const response = await fetch("https://seu-backend-python.com/start");
  const data = await response.json();
  console.log(data);
}

async function stopBot() {
  const response = await fetch("https://seu-backend-python.com/stop");
  const data = await response.json();
  console.log(data);
}

// Carregar status ao abrir página
carregarStatus();
