from flask import Flask, request, render_template_string

app = Flask(__name__)

dados = {"distancia": 0, "porta": 0, "rssi": -50}

MAX_ALTURA = 120.0   

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
            text-align: center;
            margin: 0;
            padding: 15px;
            min-height: 100vh;
        }
        .container {
            max-width: 620px;
            margin: 20px auto;
            padding: 25px 20px;
            background: url('https://i.imgur.com/FgI0DSY.jpeg') center/cover no-repeat;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
            color: white;
            position: relative;
            min-height: 500px;
        }
        .container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.68);
            border-radius: 25px;
            z-index: 1;
        }
        .content { position: relative; z-index: 2; }
        
        .wifi-indicator {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(0,0,0,0.6);
            padding: 6px 12px;
            border-radius: 12px;
            font-size: 0.9em;
            z-index: 3;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        h1 { margin: 10px 0 5px 0; font-size: 1.8em; text-shadow: 0 3px 10px rgba(0,0,0,0.9); }
        
        .progress-bg {
            width: 100%;
            height: 52px;
            background-color: rgba(255,255,255,0.25);
            border-radius: 30px;
            margin: 20px 0;
            overflow: hidden;
            position: relative;
        }
        .progress-bar {
            height: 100%;
            width: {{ porcentagem }}%;
            background: linear-gradient(90deg, {{ cor }}, {{ cor2 }});
            transition: width 0.9s ease-in-out;
            border-radius: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.35em;
            text-shadow: 0 2px 5px rgba(0,0,0,0.8);
            position: absolute;
        }
        .status { font-size: 1.6em; font-weight: bold; margin: 10px 0; }
        
        .porta-status {
            margin-top: 25px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .porta-imagem {
            width: 110px;
            height: 110px;
            border-radius: 20px;
            object-fit: cover;
            box-shadow: 0 5px 20px rgba(0,0,0,0.6);
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi-indicator">
            📶 <span>{{ rssi }} dBm</span>
        </div>
        
        <div class="content">
            <h1>🗑️ Lixeira Inteligente</h1>
            <p><strong>Márcio José Aguiar da Silva</strong></p>
            <p>Atividade Extensionista III</p>
            
            <h2>{{ distancia }} cm</h2>
            
            <div class="progress-bg">
                <div class="progress-bar">{{ porcentagem }}%</div>
            </div>
            
            <div class="status" style="color: {{ cor }};">
                {{ status }}
            </div>
            
            <div class="porta-status">
                <img src="{{ porta_imagem }}" class="porta-imagem" alt="Status da Porta">
                <strong>{{ porta_texto }}</strong>
            </div>
        </div>
    </div>

    <script>
        // Atualização automática
        setTimeout(() => location.reload(), 3000);
        
        // Alerta sonoro a partir de 95%
        if ({{ porcentagem }} >= 95) {
            const alertSound = new Audio('https://www.soundjay.com/buttons/beep-07.mp3');
            
            function playAlert() {
                alertSound.currentTime = 0;
                alertSound.play().catch(() => {});
            }
            
            // Toca imediatamente
            playAlert();
            
            // Repete a cada 6 segundos
            setInterval(playAlert, 6000);
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        distancia = float(dados.get("distancia", 0))
        porta = int(dados.get("porta", 0))
        rssi = int(dados.get("rssi", -50))
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
            
    except:
        distancia = 0
        ocupacao = 0
        rssi = -50
        cor = "#cbd5e1"
        cor2 = "#e2e8f0"
        status = "Sem dados"
        porta_imagem = ""
        porta_texto = "Sem dados da porta"

    return render_template_string(
        HTML_TEMPLATE,
        distancia=round(distancia, 1),
        porcentagem=round(ocupacao),
        cor=cor,
        cor2=cor2,
        status=status,
        porta_imagem=porta_imagem,
        porta_texto=porta_texto,
        rssi=rssi
    )

@app.route("/update", methods=["POST"])
def update():
    dist = request.form.get("distancia")
    porta = request.form.get("porta")
    rssi = request.form.get("rssi")
    if dist:
        dados["distancia"] = dist
        if porta is not None:
            dados["porta"] = porta
        if rssi is not None:
            dados["rssi"] = rssi
        print(f"✅ Recebido: {dist} cm | Porta: {porta} | RSSI: {rssi}")
        return "OK", 200
    return "Erro", 400
