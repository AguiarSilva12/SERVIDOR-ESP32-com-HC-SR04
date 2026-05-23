from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# Dados globais
dados = {
    "distancia": 120.0,
    "porta": 0,
    "rssi": -80,
    "ultima_atualizacao": ""
}

def get_horario_brasilia():
    fuso_brasilia = ZoneInfo("America/Sao_Paulo")
    agora = datetime.now(fuso_brasilia)
    return agora.strftime("%H:%M:%S")

dados["ultima_atualizacao"] = get_horario_brasilia()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lixeira Inteligente</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.75)),
                        url('https://i.imgur.com/96reii8.jpeg') no-repeat center center fixed;
            background-size: cover;
            color: white;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .overlay {
            max-width: 700px;
            width: 100%;
        }

        h1 {
            color: #22ff66;
            font-size: 2.2rem;
            margin-bottom: 10px;
            text-shadow: 0 0 15px rgba(34, 255, 102, 0.8);
        }

        .distancia {
            font-size: 4.5rem;
            font-weight: bold;
            margin: 15px 0;
            text-shadow: 0 0 20px rgba(0,0,0,0.9);
        }

        .progress-bg {
            width: 100%;
            background: rgba(255,255,255,0.2);
            height: 28px;
            border-radius: 20px;
            overflow: hidden;
            margin: 20px auto;
            backdrop-filter: blur(5px);
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #22ff66, #ffcc00);
            transition: width 0.8s ease;
            box-shadow: 0 0 15px rgba(34, 255, 102, 0.6);
        }

        .status {
            font-size: 1.8rem;
            margin: 15px 0;
            font-weight: bold;
        }

        .info {
            font-size: 1.35rem;
            margin: 12px 0;
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
        }

        .atualizado {
            font-size: 1.2rem;
            color: #a0d8ff;
            margin-top: 25px;
        }
    </style>
</head>
<body>
    <div class="overlay">
        <h1>🗑️ Lixeira Inteligente</h1>
        <div class="distancia" id="distancia">--- cm</div>
        
        <div class="progress-bg">
            <div class="progress-bar" id="progress"></div>
        </div>
        
        <p class="status" id="status">Aguardando dados...</p>
        <p class="info" id="porta-info">🚪 Porta: ---</p>
        <p class="info" id="rssi-info">📶 Sinal WiFi: --- dBm</p>
        <p class="atualizado">⏰ <span id="tempo">---</span></p>
    </div>

    <script>
        function atualizarDados() {
            fetch('/dados')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('distancia').textContent = data.distancia.toFixed(1) + " cm";
                    
                    const porcentagem = Math.max(0, Math.min(100, 100 - (data.distancia / 1.2)));
                    document.getElementById('progress').style.width = porcentagem + "%";
                    
                    let statusTexto = "";
                    if (porcentagem <= 25) statusTexto = "🟢 Vazia";
                    else if (porcentagem <= 65) statusTexto = "🟡 Meio Cheia";
                    else statusTexto = "🔴 Cheia";
                    document.getElementById('status').textContent = statusTexto;
                    
                    document.getElementById('porta-info').textContent = "🚪 Porta: " + (data.porta === 1 ? "ABERTA" : "FECHADA");
                    document.getElementById('rssi-info').textContent = "📶 Sinal WiFi: " + data.rssi + " dBm";
                    document.getElementById('tempo').textContent = data.ultima_atualizacao;
                })
                .catch(err => console.log("Erro:", err));
        }

        setInterval(atualizarDados, 2000);
        window.onload = atualizarDados;
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/dados")
def get_dados():
    return jsonify(dados)

@app.route("/atualizar/1", methods=["POST"])
@app.route("/update", methods=["POST"])
def update():
    try:
        if request.is_json:
            conteudo = request.get_json()
        else:
            conteudo = request.form.to_dict()

        dados["distancia"] = float(conteudo.get("distancia", 120))
        dados
