from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import json

app = Flask(__name__)

ARQUIVO_DADOS = "dados.txt"

# ====================== DADOS PADRÃO ======================
dados_padrao = {
    "distancia": 120.0,
    "nivel": 0,
    "porta": 0,
    "rssi": -80,
    "alarme": 0,
    "trava": 0,
    "destravar": 0,
    "tempo_porta_aberta": 0,
    "ultima_atualizacao": ""
}

# ====================== HORÁRIO ======================
def get_horario_brasilia():

    fuso_brasilia = ZoneInfo("America/Sao_Paulo")

    agora = datetime.now(fuso_brasilia)

    return agora.strftime("%H:%M:%S")

# ====================== CARREGAR DADOS ======================
def carregar_dados():

    if os.path.exists(ARQUIVO_DADOS):

        try:

            with open(ARQUIVO_DADOS, "r") as f:

                return json.load(f)

        except:

            return dados_padrao.copy()

    return dados_padrao.copy()

# ====================== SALVAR DADOS ======================
def salvar_dados(novos_dados):

    try:

        with open(ARQUIVO_DADOS, "w") as f:

            json.dump(novos_dados, f, indent=2)

    except Exception as e:

        print("❌ Erro ao salvar:", e)

# ====================== HTML ======================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Lixeira Inteligente</title>

<style>

body {

    font-family: Arial, sans-serif;

    background:
    linear-gradient(rgba(0,0,0,0.65),
    rgba(0,0,0,0.75)),
    url('https://i.imgur.com/96reii8.jpeg')
    no-repeat center center fixed;

    background-size: cover;

    color: white;

    text-align: center;

    margin: 0;

    padding: 20px;

    min-height: 100vh;
}

.overlay {

    max-width: 700px;

    margin: auto;
}

h1 {

    color: #22ff66;
}

.distancia {

    font-size: 4.5rem;

    font-weight: bold;

    margin: 15px 0;
}

.progress-bg {

    width: 100%;

    background: rgba(255,255,255,0.2);

    height: 32px;

    border-radius: 20px;

    overflow: hidden;

    margin: 25px auto;
}

.progress-bar {

    height: 100%;

    background:
    linear-gradient(90deg,#22ff66,#ffaa00,#ff2222);

    transition: width 0.9s ease;
}

.status {

    font-size: 1.9rem;

    margin: 15px 0;

    font-weight: bold;
}

.info {

    font-size: 1.35rem;

    margin: 12px 0;
}

.porta-alerta {

    animation: pisca 0.8s infinite;

    color: #ff4444;

    font-weight: bold;
}

.btn-trava {

    margin-top: 20px;

    padding: 14px 25px;

    font-size: 1rem;

    border: none;

    border-radius: 10px;

    cursor: pointer;

    background: #ff4444;

    color: white;

    font-weight: bold;

    transition: 0.3s;
}

.btn-trava:hover {

    opacity: 0.85;
}

@keyframes pisca {

    0% {opacity:1;}

    50% {opacity:0.4;}

    100% {opacity:1;}
}

</style>

</head>

<body>

<div class="overlay">

<p class="titulo-projeto">

Atividade Extensionista III - Projeto de Eletrônica<br>

Aluno: Marcio Jose Aguiar da Silva

</p>

<h1>🗑️ Lixeira Inteligente</h1>

<div class="distancia"
     id="distancia">

--- cm

</div>

<div class="progress-bg">

<div class="progress-bar"
     id="progress">

</div>

</div>

<p class="status"
   id="status">

Aguardando dados...

</p>

<p class="info"
   id="nivel-info">

📊 Nível: ---%

</p>

<p class="info"
   id="porta-info">

🚪 Porta: ---

</p>

<p class="info"
   id="trava-info">

🔒 Trava: ---

</p>

<p class="info"
   id="tempo-aberta">

⏱️ Tempo Aberta: 0 segundos

</p>

<p class="info"
   id="rssi-info">

📶 WiFi: --- dBm

</p>

<p class="atualizado">

⏰ <span id="tempo">---</span>

</p>

<button
class="btn-trava"
id="btnTrava"
onclick="destravarPorta()"
style="display:none;">

🔓 Liberar Porta

</button>

</div>

<script>

function atualizarDados() {

    fetch('/dados')

    .then(r => r.json())

    .then(data => {

        // ===== DISTÂNCIA =====
        document.getElementById('distancia')
        .textContent =
        data.distancia.toFixed(1) + " cm";

        // ===== NÍVEL =====
        const perc =
        Math.max(0,
        Math.min(100,
        data.nivel));

        document.getElementById('progress')
        .style.width =
        perc + "%";

        document.getElementById('nivel-info')
        .textContent =
        `📊 Nível: ${perc}%`;

        // ===== STATUS =====
        let status = "";

        if (perc < 70)
            status = "🟢 DISPONÍVEL";

        else if (perc <= 85)
            status = "🔴 ALERTA";

        else
            status = "⛔ LOTADA";

        document.getElementById('status')
        .textContent = status;

        // ===== PORTA =====
        const portaEl =
        document.getElementById('porta-info');

        if (data.porta === 1) {

            portaEl.textContent =
            "🚪 Porta: ABERTA";

            if (data.alarme === 1)
                portaEl.classList.add('porta-alerta');

        } else {

            portaEl.textContent =
            "🚪 Porta: FECHADA";

            portaEl.classList.remove('porta-alerta');
        }

        // ===== TRAVA =====
        const travaEl =
        document.getElementById('trava-info');

        const btnTrava =
        document.getElementById('btnTrava');

        if (data.trava === 1) {

            // ===== TRAVA ATIVA =====
            if (data.destravar === 0) {

                travaEl.textContent =
                "🔒 Trava: ACIONADA";

                btnTrava.innerHTML =
                "🔓 Liberar Porta";

                btnTrava.style.background =
                "#ff4444";
            }

            // ===== LIBERADA REMOTAMENTE =====
            else {

                travaEl.textContent =
                "🔓 Trava: LIBERADA REMOTAMENTE";

                btnTrava.innerHTML =
                "✅ Porta Liberada";

                btnTrava.style.background =
                "#22bb33";
            }

            btnTrava.style.display =
            "inline-block";

        }
        else {

            travaEl.textContent =
            "🔓 Trava: DESLIGADA";

            btnTrava.style.display =
            "none";
        }

        // ===== TEMPO =====
        document.getElementById('tempo-aberta')
        .textContent =
        `⏱️ Tempo Aberta:
        ${data.tempo_porta_aberta}
        segundos`;

        // ===== WIFI =====
        document.getElementById('rssi-info')
        .textContent =
        `📶 WiFi:
        ${data.rssi} dBm`;

        // ===== HORÁRIO =====
        document.getElementById('tempo')
        .textContent =
        data.ultima_atualizacao;

    });
}

// ====================== BOTÃO DESTRAVAR ======================
function destravarPorta() {

    fetch('/destravar', {

        method: 'POST'

    })

    .then(r => r.json())

    .then(data => {

        const btnTrava =
        document.getElementById('btnTrava');

        btnTrava.innerHTML =
        "✅ Comando Enviado";

        btnTrava.style.background =
        "#22bb33";

        alert("🔓 Porta liberada remotamente!");

    });

}

setInterval(atualizarDados, 1500);

window.onload = atualizarDados;

</script>

</body>
</html>
"""

# ====================== PÁGINA ======================
@app.route("/")
def index():

    return render_template_string(HTML_TEMPLATE)

# ====================== DADOS JSON ======================
@app.route("/dados")
def get_dados():

    return jsonify(carregar_dados())

# ====================== DESTRAVAR PORTA ======================
@app.route("/destravar", methods=["POST"])
def destravar():

    dados = carregar_dados()

    dados["destravar"] = 1

    salvar_dados(dados)

    print("🔓 PORTA LIBERADA REMOTAMENTE")

    return jsonify({
        "status": "ok",
        "destravar": 1
    })

# ====================== RESETAR COMANDO ======================
@app.route("/resetar", methods=["POST"])
def resetar():

    dados = carregar_dados()

    dados["destravar"] = 0

    salvar_dados(dados)

    print("♻️ COMANDO RESETADO")

    return "OK"

# ====================== RECEBER DADOS ESP32 ======================
@app.route("/atualizar/1", methods=["POST"])
@app.route("/update", methods=["POST"])

def update():

    try:

        if request.is_json:

            conteudo = request.get_json()

        else:

            conteudo = request.form.to_dict()

        tempo_aberto = int(
            conteudo.get(
            "tempo_porta_aberta", 0)
        )

        dados_atuais = carregar_dados()

        novos_dados = {

            "distancia":
            float(conteudo.get(
            "distancia", 120)),

            "nivel":
            int(conteudo.get(
            "nivel", 0)),

            "porta":
            int(conteudo.get(
            "porta", 0)),

            "rssi":
            int(conteudo.get(
            "rssi", -90)),

            "alarme":
            int(conteudo.get(
            "alarme", 0)),

            "trava":
            int(conteudo.get(
            "trava", 0)),

            "destravar":
            dados_atuais.get(
            "destravar", 0),

            "tempo_porta_aberta":
            tempo_aberto,

            "ultima_atualizacao":
            get_horario_brasilia()
        }

        salvar_dados(novos_dados)

        print(
        f"✅ Nível: {novos_dados['nivel']}% | "
        f"Trava: {novos_dados['trava']} | "
        f"Destravar: {novos_dados['destravar']}"
        )

        return "OK", 200

    except Exception as e:

        print("❌ Erro:", e)

        return "Erro", 400

# ====================== INICIAR SERVIDOR ======================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    print(f"🚀 Servidor rodando na porta {port}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
