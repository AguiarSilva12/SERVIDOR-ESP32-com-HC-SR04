from flask import Flask, request, render_template_string
import time
import json

app = Flask(__name__)

# Dados globais (em memória)
dados = {
    "distancia": 120.0,
    "porta": 0,
    "rssi": -80,
    "ultima_atualizacao": time.strftime("%H:%M:%S"),
    "ip_esp": "Desconhecido"
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
        .distancia { font-size: 3.5rem; font-weight: bold; margin: 10px 0; }
        .progress-bg {
            width: 100%;
            background: #334155;
            height: 40px;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px auto;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #22c55e, #eab308);
            transition: width 0.6s ease;
        }
        .status { font-size: 1.4rem; margin: 15px 0; }
        .info { margin: 8px 0; font-size: 1.1rem; }
        .atualizado { color: #94a3b8; font-size: 0.95rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗑️ Lixeira Inteligente</h1>
        <div class="distancia">{{ distancia }} cm</div>
        
        <div class="progress-bg">
            <div class="progress-bar" style="width: {{ porcentagem }}%;"></div>
        </div>
        
        <p class="status">{{ status }}</p>
        <p class="info">🚪 Porta: <strong>{{ porta_texto }}</strong></p>
        <p class="info">📶 Sinal WiFi: <strong>{{ rssi }} dBm</strong></p>
        <p class="atualizado">⏰ Última atualização: {{ ultima_atualizacao }}</p>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    val = float(dados.get("distancia", 120))
    
    # Calcula porcentagem (considerando profundidade aproximada de 120cm)
    porcentagem = max(0, min(100, 100 - (val / 1.2)))
    
    if porcentagem <= 25:
        status = "🟢 Vazia"
    elif porcentagem <= 65:
        status = "🟡 Meio Cheia"
    else:
        status = "🔴 Cheia"
    
    porta_texto = "ABERTA" if dados.get("porta") == 1 else "FECHADA"
    
    return render_template_string(
        HTML_TEMPLATE,
        distancia=round(val, 1),
        porcentagem=round(porcentagem),
        status=status,
        porta_texto=porta_texto,
        rssi=dados.get("rssi"),
        ultima_atualizacao=dados.get("ultima_atualizacao")
    )

# ==================== ROTA PARA O ESP32 ====================
@app.route("/atualizar/1", methods=["POST"])
@app.route("/update", methods=["POST"])  # mantido para compatibilidade
def update():
    try:
        if request.is_json:
            # ESP32 envia JSON
            conteudo = request.get_json()
        else:
            # fallback para form data
            conteudo = request.form.to_dict()

        dados["distancia"] = float(conteudo.get("distancia", 120))
        dados["porta"] = int(conteudo.get("porta", 0))
        dados["rssi"] = int(conteudo.get("rssi", -90))
        dados["ultima_atualizacao"] = time.strftime("%H:%M:%S")
        
        print(f"✅ Dados recebidos: Dist={dados['distancia']:.1f}cm | Porta={'Aberta' if dados['porta']==1 else 'Fechada'}")
        
        return "OK", 200

    except Exception as e:
        print("❌ Erro ao receber dados:", e)
        return "Erro", 400

# Rota de status (opcional - útil para debug)
@app.route("/status")
def status():
    return {
        "status": "online",
        "ultima_atualizacao": dados["ultima_atualizacao"],
        "distancia": dados["distancia"]
    }

if __name__ == "__main__":
    print("🚀 Servidor Flask rodando em http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
