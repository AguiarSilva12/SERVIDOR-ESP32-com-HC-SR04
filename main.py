from flask import Flask, request, render_template_string

app = Flask(__name__)

# Simulando dados de 5 lixeiras
lixeiras = {
    1: {"distancia": 16.1, "porta": 1, "rssi": -65, "nome": "Lixeira 01"},
    2: {"distancia": 45.0, "porta": 0, "rssi": -72, "nome": "Lixeira 02"},
    3: {"distancia": 8.5,  "porta": 0, "rssi": -58, "nome": "Lixeira 03"},
    4: {"distancia": 95.0, "porta": 1, "rssi": -80, "nome": "Lixeira 04"},
    5: {"distancia": 30.0, "porta": 0, "rssi": -68, "nome": "Lixeira 05"},
}

MAX_ALTURA = 120.0

# ====================== TEMPLATE DA TELA PRINCIPAL ======================
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lixeiras Inteligentes</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        h1 { text-align: center; margin-bottom: 30px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        }
        .card:hover {
            transform: scale(1.05);
            background: rgba(255,255,255,0.2);
        }
        .card h3 { margin: 10px 0; }
        .progress-small {
            height: 12px;
            background: #333;
            border-radius: 10px;
            margin: 10px 0;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #22c55e, #ef4444);
        }
    </style>
</head>
<body>
    <h1>🗑️ Lixeiras Inteligentes</h1>
    <div class="grid">
        {% for id, data in lixeiras.items() %}
        <div class="card" onclick="window.location.href='/lixeira/{{ id }}'">
            <h3>{{ data.nome }}</h3>
            <p>{{ data.distancia }} cm</p>
            <div class="progress-small">
                <div class="progress-fill" style="width: {{ (100 - (data.distancia / 120 * 100))|round }}%;"></div>
            </div>
            <small>📶 {{ data.rssi }} dBm</small>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# ====================== TEMPLATE DETALHADO (atual) ======================
DETAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ nome }}</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: white; margin:0; padding:15px; }
        .container { max-width: 620px; margin: 20px auto; padding: 25px 20px; background: url('https://i.imgur.com/SUA_IMAGEM_DIRETA.jpg') center/cover no-repeat; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); position: relative; min-height: 500px; }
        .container::before { content:''; position:absolute; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.68); border-radius:25px; z-index:1; }
        .content { position: relative; z-index: 2; text-align:center; }
        .wifi { position: absolute; top:15px; right:15px; background:rgba(0,0,0,0.6); padding:6px 12px; border-radius:12px; z-index:3; }
        .progress-bg { height:52px; background:rgba(255,255,255,0.25); border-radius:30px; margin:20px 0; position:relative; overflow:hidden; }
        .progress-bar { height:100%; width:{{ porcentagem }}%; background:linear-gradient(90deg, {{ cor }}, {{ cor2 }}); display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:1.35em; position:absolute; }
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi">📶 {{ rssi }} dBm</div>
        <div class="content">
            <h1>🗑️ {{ nome }}</h1>
            <p><strong>Márcio José Aguiar da Silva</strong></p>
            <p>Atividade Extensionista III</p>
            
            <h2>{{ distancia }} cm</h2>
            
            <div class="progress-bg">
                <div class="progress-bar">{{ porcentagem }}%</div>
            </div>
            
            <div style="font-size:1.6em; font-weight:bold; color:{{ cor }}; margin:10px 0;">
                {{ status }}
            </div>
            
            <div style="margin-top:25px;">
                <img src="{{ porta_imagem }}" width="110" height="110" style="border-radius:20px; box-shadow:0 5px 20px rgba(0,0,0,0.6);">
                <p><strong>{{ porta_texto }}</strong></p>
            </div>
        </div>
    </div>

    <script>
        setTimeout(() => location.reload(), 4000);
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE, lixeiras=lixeiras)

@app.route("/lixeira/<int:id>")
def detalhe_lixeira(id):
    if id not in lixeiras:
        return "Lixeira não encontrada", 404
    
    data = lixeiras[id]
    distancia = float(data["distancia"])
    porta = int(data["porta"])
    ocupacao = max(0, min(100, 100 - (distancia / MAX_ALTURA * 100)))
    
    if ocupacao <= 20:
        cor = "#22c55e"; cor2 = "#4ade80"; status = "🟢 Lixeira Vazia"
    elif ocupacao <= 40:
        cor = "#86efac"; cor2 = "#a3e635"; status = "🟢 Quase Vazia"
    elif ocupacao <= 60:
        cor = "#eab308"; cor2 = "#facc15"; status = "🟡 Nível Médio"
    elif ocupacao <= 80:
        cor = "#f97316"; cor2 = "#fb923c"; status = "🟠 Quase Cheia"
    else:
        cor = "#ef4444"; cor2 = "#f87171"; status = "🔴 Lixeira Cheia"
    
    if porta == 0:
        porta_imagem = "https://i.imgur.com/rAWpErV.jpeg"
        porta_texto = "✅ Porta Fechada"
    else:
        porta_imagem = "https://i.imgur.com/4IKIN7A.jpeg"
        porta_texto = "⚠️ Porta Aberta"
    
    return render_template_string(DETAIL_TEMPLATE,
        nome=data["nome"],
        distancia=round(distancia, 1),
        porcentagem=round(ocupacao),
        cor=cor,
        cor2=cor2,
        status=status,
        porta_imagem=porta_imagem,
        porta_texto=porta_texto,
        rssi=data["rssi"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
