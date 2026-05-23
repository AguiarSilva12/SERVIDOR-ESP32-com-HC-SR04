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

# Horário inicial
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
            background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.92)),
                        url('https://i.imgur.com/96reii8.jpeg') no-repeat center center fixed;
            background-size: cover;
            color: white;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 620px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.70);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(8px);
        }
        h1 {
            color: #22c55e;
            text-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
        }
        .distancia {
            font-size: 3.8rem;
            font-weight: bold;
            margin: 15px 0;
            text-shadow: 0 0 15px rgba(0,0,0,0.8);
        }
        .progress-bg {
            width: 100%;
            background: #334155;
            height: 45px;
            border-radius: 15px;
            overflow: hidden;
            margin: 25px auto;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #22c55e, #eab308);
            transition: width 0.8s ease;
        }
        .status {
            font-size: 1.6rem;
            margin: 20px 0;
            font-weight: bold;
        }
        .info {
            margin: 12px 0;
            font-size: 1.2rem;
        }
        .atualizado {
            color: #a5b4fc;
            font-size: 1.05rem;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗑️ Lixeira Inteligente</h1>
        <div class="distancia" id="distancia">--- cm</div>
      
        <div class="progress-bg">
            <div class="progress-bar" id="progress"></div>
        </div>
      
        <p class="status" id="status">Aguardando dados...</p>
        <p class="info">🚪 Porta: <strong id="porta">---</strong></p>
        <p class="info">📶 Sinal WiFi: <strong id="rssi">---</strong> dBm</p>
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
                    
                    document.getElementById('porta').textContent = data.porta === 1 ? "ABERTA" : "FECHADA";
                    document.getElementById('rssi').textContent = data.rssi;
                    document.getElementById('tempo').textContent = data.ultima_atualizacao;
                })
                .catch(err => console.log("Erro ao buscar dados:", err));
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

# ==================== ROTA PARA O ESP32 ====================
@app.route("/atualizar/1", methods=["POST"])
@app.route("/update", methods=["POST"])
def update():
    try:
        if request.is_json:
            conteudo = request.get_json()
        else:
            conteudo = request.form.to_dict()

        dados["distancia"] = float(conteudo.get("distancia", 120))
        dados["porta"] = int(conteudo.get("porta", 0))
        dados["rssi"] = int(conteudo.get("rssi", -90))
        dados["ultima_atualizacao"] = get_horario_brasilia()
        
        print(f"✅ Recebido → Dist: {dados['distancia']:.1f}cm | Porta: {'Aberta' if dados['porta']==1 else 'Fechada'}")
        return "OK", 200

    except Exception as e:
        print("❌ Erro:", e)
        return "Erro", 400


if __name__ == "__main__":
    print("🚀 Servidor rodando em http://0.0.0.0:5000")
    print("📡 Acesse no navegador: http://SEU_IP:
