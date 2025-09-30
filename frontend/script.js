const backendUrl = "https://bot-trading-pro-1.onrender.com";

const statusEl = document.getElementById("bot-status");
const logEl = document.getElementById("log");

document.getElementById("start-btn").addEventListener("click", () => sendCommand("start"));
document.getElementById("stop-btn").addEventListener("click", () => sendCommand("stop"));
document.getElementById("order-btn").addEventListener("click", () => sendCommand("order_test"));

async function sendCommand(command) {
    statusEl.textContent = "A processar...";
    statusEl.className = "status loading";

    try {
        const response = await fetch(`${backendUrl}/${command}`);
        const data = await response.json();

        logEl.innerHTML += `<div>> ${command}: ${data.message}</div>`;
        logEl.scrollTop = logEl.scrollHeight;

        if (command === "start") {
            statusEl.textContent = "Bot em execução";
            statusEl.className = "status running";
        } else if (command === "stop") {
            statusEl.textContent = "Bot parado";
            statusEl.className = "status stopped";
        } else {
            statusEl.textContent = "Bot em execução";
            statusEl.className = "status running";
        }
    } catch (error) {
        logEl.innerHTML += `<div style="color:red;">Erro: ${error.message}</div>`;
        statusEl.textContent = "Erro ao comunicar com backend";
        statusEl.className = "status stopped";
    }
}
