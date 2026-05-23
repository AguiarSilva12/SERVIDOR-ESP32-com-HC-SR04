from flask import Flask, request, render_template_string, jsonify
import time

app = Flask(__name__)

# Dados globais
dados = {
    "distancia": 120.0,
    "porta": 0,
    "rssi": -80,
    "ultima_atualizacao": time.strftime("%H:%M:%S")
}

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
            background: #0f172a; 
            color: white; 
            text-align: center; 
            margin: 0;
            padding: 20px;
        }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { color: #22c55e; }
        .distancia { font-size: 3.8rem; font-weight: bold; margin: 10px 0; }
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
        .status { font-size: 1.5rem; margin: 15px 0; font-weight: bold; }
        .info { margin: 10px 0; font-size: 1.15rem; }
        .atualizado { color: #94a3b8; font-size: 1rem; }
        .atualizando { color: #60a5fa; }
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
        <p class="atualizado">⏰ Última atualização: <span id="tempo">---</span></p>
    </div>

    <script>
        let ultimaAtualizacao = Date.now();

        function atualizarDados() {
            fetch('/dados')
                .then(response => response.json())
                .then(data => {
                    // Atualiza distância
                    document.getElementById('distancia').textContent = data.distancia.toFixed(1) + " cm";
                    
                    // Atualiza barra de progresso
                    const porcentagem = Math.max(0, Math.min(100, 100 - (data.distancia / 1.2)));
                    document.getElementById('progress').style.width = porcentagem + "%";
                    
                    // Atualiza status
                    let statusTexto = "";
                    if (porcentagem <= 25) statusTexto = "🟢 Vazia";
                    else if (porcentagem <= 65) statusTexto = "🟡 Meio Cheia";
                    else statusTexto = "🔴 Cheia";
                    document.getElementById('status').textContent = statusTexto;
                    
                    // Atualiza porta
                    document.getElementById('porta').textContent = data.porta === 1 ? "ABERTA" : "FECHADA";
                    
                    // Atualiza RSSI
                    document.getElementById('rssi').textContent = data.rssi;
                    
                    // Atualiza hora
                    document.getElementById('tempo').textContent = data.ultima_atualizacao;
                    
                    ultimaAtualizacao = Date.now();
                })
                .catch(err => console.log("Erro ao buscar dados:", err));
        }

        // Atualiza a cada 2 segundos
        setInterval(atualizarDados, 2000);
        
        // Primeira atualização imediata
        window.onload = atualizarDados;
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

# Rota que retorna os dados em JSON (usada pelo JavaScript)
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
        dados["ultima_atualizacao"] = time.strftime("%H:%M:%S")
        
        print(f"✅ Recebido → Dist: {dados['distancia']:.1f}cm | Porta: {'Aberta' if dados['porta']==1 else 'Fechada'}")
        return "OK", 200

    except Exception as e:
        print("❌ Erro:", e)
        return "Erro", 400


if __name__ == "__main__":
    print("🚀 Servidor rodando em http://0.0.0.0:5000")
    print("📡 Acesse no navegador: http://SEU_IP:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
