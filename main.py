from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import json

app = Flask(__name__)

# Caminho para salvar os dados
ARQUIVO_DADOS = "dados.txt"

# Estrutura padrão atualizada
dados_padrao = {
    "distancia": 120.0,
    "nivel": 0,
    "porta": 0,
    "rssi": -80,
    "alarme": 0,                    # Novo: Alarme de porta aberta
    "tempo_porta_aberta": 0,        # Tempo em segundos que a porta está aberta
    "ultima_atualizacao": ""
}

def get_horario_brasilia():
    fuso_brasilia = ZoneInfo("America/Sao_Paulo")
    agora = datetime.now(fuso_brasilia)
    return agora.strftime("%H:%M:%S")

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r") as f:
                return json.load(f)
        except:
            return dados_padrao.copy()
    else:
        valores = dados_padrao.copy()
        valores["ultima_atualizacao"] = get_horario_brasilia()
        return valores

def salvar_dados(novos_dados):
    try:
        with open(ARQUIVO_DADOS, "w") as f:
            json.dump(novos_dados, f)
    except Exception as e:
        print("❌ Erro ao salvar:", e)

# ====================== TEMPLATE HTML ATUALIZADO ======================
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
        .overlay { max-width: 700px; width: 100%; }
        .titulo-projeto {
            color: #a0d8ff;
            font-size: 1.35rem;
            margin-bottom: 8px;
        }
        h1 {
            color: #22ff66;
            font-size: 2.2rem;
            margin-bottom: 10px;
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
            background: linear-gradient(90deg, #22ff66, #ffaa00);
            transition: width 0.9s ease;
        }
        .status { font-size: 1.9rem; margin: 15px 0; font-weight: bold; }
        .info { font-size: 1.35rem; margin: 12px 0; }
        .atualizado { font-size: 1.2rem; color: #a0d8ff; margin-top: 30px; }

        /* Alerta de Porta Aberta */
        .porta-alerta {
            animation: pisca-vermelho 0.8s infinite;
            color: #ff4444;
            font-weight: bold;
        }
        @keyframes pisca-vermelho {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
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
       
        <div class="distancia" id="distancia">--- cm</div>
        <div class="progress-bg">
            <div class="progress-bar" id="progress"></div>
        </div>
        <p class="status" id="status">Aguardando dados...</p>
        <p class="info" id="nivel-info">📊 Nível: ---%</p>
        
        <p class="info" id="porta-info">🚪 Porta: ---</p>
        <p class="info" id="tempo-aberta">⏱️ Tempo Aberta: --- segundos</p>
        
        <p class="info" id="rssi-info">📶 Sinal WiFi: --- dBm</p>
        <p class="atualizado">⏰ <span id="tempo">---</span></p>
    </div>

    <script>
        function atualizarDados() {
            fetch('/dados')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('distancia').textContent = data.distancia.toFixed(1) + " cm";
                    
                    const porcentagem = Math.max(0, Math.min(100, data.nivel));
                    document.getElementById('progress').style.width = porcentagem + "%";
                    document.getElementById('nivel-info').textContent = "📊 Nível: " + porcentagem + "%";

                    let statusTexto = "";
                    if (porcentagem <= 25) statusTexto = "🟢 Quase Vazia";
                    else if (porcentagem <= 60) statusTexto = "🟡 Meio Cheia";
                    else if (porcentagem <= 85) statusTexto = "🟠 Cheia";
                    else statusTexto = "🔴 Muito Cheia - Esvaziar!";
                    document.getElementById('status').textContent = statusTexto;

                    // Porta com alarme visual
                    const portaElement = document.getElementById('porta-info');
                    if (data.porta === 1) {
                        portaElement.textContent = "🚪 Porta: ABERTA";
                        if (data.alarme === 1) {
                            portaElement.classList.add('porta-alerta');
                        } else {
                            portaElement.classList.remove('porta-alerta');
                        }
                    } else {
                        portaElement.textContent = "🚪 Porta: FECHADA";
                        portaElement.classList.remove('porta-alerta');
                    }

                    // Tempo que a porta está aberta
                    document.getElementById('tempo-aberta').textContent = 
                        "⏱️ Tempo Aberta: " + data.tempo_porta_aberta + " segundos";

                    document.getElementById('rssi-info').textContent = "📶 Sinal WiFi: " + data.rssi + " dBm";
                    document.getElementById('tempo').textContent = data.ultima_atualizacao;
                })
                .catch(err => console.log("Erro ao buscar dados:", err));
        }

        setInterval(atualizarDados, 1500);
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
    return jsonify(carregar_dados())

@app.route("/atualizar/1", methods=["POST"])
@app.route("/update", methods=["POST"])
def update():
    try:
        if request.is_json:
            conteudo = request.get_json()
        else:
            conteudo = request.form.to_dict()

        novos_dados = {
            "distancia": float(conteudo.get("distancia", 120)),
            "nivel": int(conteudo.get("nivel", 0)),
            "porta": int(conteudo.get("porta", 0)),
            "rssi": int(conteudo.get("rssi", -90)),
            "alarme": int(conteudo.get("alarme", 0)),                    # Novo
            "tempo_porta_aberta": int(conteudo.get("tempo_porta_aberta", 0)),  # Novo
            "ultima_atualizacao": get_horario_brasilia()
        }
      
        salvar_dados(novos_dados)
       
        print(f"✅ Recebido → Nível: {novos_dados['nivel']}% | Porta: {'ABERTA' if novos_dados['porta'] else 'FECHADA'} | Alarme: {novos_dados['alarme']}")
        return "OK", 200

    except Exception as e:
        print("❌ Erro ao processar dados:", e)
        return "Erro", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor rodando na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
