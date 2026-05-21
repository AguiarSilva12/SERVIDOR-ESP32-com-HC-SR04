from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

# Armazenamento dos dados
dados = {
    "distancia": 25.0,
    "temperatura": 25.0,
    "umidade": 50.0,
    "porta": 0,
    "ir": 0,
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
        .container {
            max-width: 700px;
            margin: auto;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        }
        .progress-bg {
            width: 100%;
            background-color: #334155;
            border-radius: 20px;
            height: 40px;
            margin: 20px 0;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            width: {{ porcentagem }}%;
            background: linear-gradient(90deg, #22c55e, #ef4444);
            transition: width 0.6s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: white;
        }
        h1 { color: #60a5fa; margin-bottom: 10px; }
        .info { margin: 15px 0; font-size: 1.1em; }
        .status { font-size: 1.5em; font-weight: bold; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗑️ Lixeira Inteligente</h1>
        <p><strong>Márcio José Aguiar da Silva</strong></p>
        <p>Atividade Extensionista III</p>
        
        <h2>{{ distancia }} cm</h2>
        
        <div class="progress-bg">
            <div class="progress-bar">{{ porcentagem }}%</div>
        </div>
        
        <div class="status" style="color: {{ cor }};">{{ status }}</div>
        
        <div class="info">
            🌡️ Temperatura: <strong>{{ temperatura }} °C</strong><br>
            💧 Umidade: <strong>{{ umidade }} %</strong><br>
            🚪 Porta: <strong>{{ porta_texto }}</strong><br>
            👀 Infravermelho: <strong>{{ ir_texto }}</strong><br>
            ⏰ Atualizado: {{ ultima_atualizacao }}
        </div>
    </div>
    
    <script>
        setTimeout(() => location.reload(), 3000);  // Atualiza a cada 3 segundos
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        val = float(dados.get("distancia", 0))
        porcentagem = max(0, min(100, 100 - (val / 1.2)))  # 120 cm = 100%
        
        if porcentagem <= 30:
            cor = "#22c55e"
            status = "🟢 Lixeira Vazia"
        elif porcentagem <= 70:
            cor = "#eab308"
            status = "🟡 Nível Médio"
        else:
            cor = "#ef4444"
            status = "🔴 Lixeira Cheia"
    except:
        val = 0
        porcentagem = 0
        cor = "#64748b"
        status = "Sem dados"

    porta_texto = "ABERTA ⚠️" if dados.get("porta") == 1 else "FECHADA ✅"
    ir_texto = "Detectado" if dados.get("ir") == 0 else "Livre"

    return render_template_string(
        HTML_TEMPLATE,
        distancia=round(val, 1),
        porcentagem=round(porcentagem),
        cor=cor,
        status=status,
        temperatura=round(float(dados.get("temperatura", 0)), 1),
        umidade=round(float(dados.get("umidade", 0)), 1),
        porta_texto=porta_texto,
        ir_texto=ir_texto,
        ultima_atualizacao=dados.get("ultima_atualizacao", "")
    )

@app.route("/update", methods=["POST"])
def update():
    try:
        dados["distancia"] = float(request.form.get("distancia", 25.0))
        dados["temperatura"] = float(request.form.get("temperatura", 25.0))
        dados["umidade"] = float(request.form.get("umidade", 50.0))
        dados["porta"] = int(request.form.get("porta", 0))
        dados["ir"] = int(request.form.get("ir", 1))
        dados["ultima_atualizacao"] = time.strftime("%H:%M:%S")
        
        print(f"✅ Dados recebidos - Dist: {dados['distancia']} cm | Temp: {dados['temperatura']}°C")
        return "OK", 200
    except Exception as e:
        print(f"❌ Erro ao receber dados: {e}")
        return "Erro", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
