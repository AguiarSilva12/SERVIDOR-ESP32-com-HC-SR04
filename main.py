from flask import Flask, request, render_template_string

app = Flask(__name__)

dados = {"distancia": 0}

MAX_ALTURA = 120.0   

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lixeira Inteligente</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 620px;
            margin: 40px auto;
            padding: 35px;
            background: url('https://i.imgur.com/gz0mqnB.jpeg') center/cover no-repeat;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
            color: white;
            position: relative;
            min-height: 460px;
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
        
        h1 { margin-bottom: 8px; text-shadow: 0 3px 10px rgba(0,0,0,0.9); }
        .progress-bg {
            width: 100%;
            height: 48px;
            background-color: rgba(255,255,255,0.25);
            border-radius: 30px;
            margin: 25px 0;
            overflow: hidden;
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
            font-size: 1.2em;
            text-shadow: 0 2px 5px rgba(0,0,0,0.7);
        }
        .status {
            font-size: 1.65em;
            font-weight: bold;
            margin: 15px 0;
            text-shadow: 0 3px 8px rgba(0,0,0,0.9);
        }
    </style>
</head>
<body>
    <div class="container">
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
        </div>
    </div>

    <script>
        setTimeout(() => location.reload(), 3000);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        distancia = float(dados.get("distancia", 0))
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
    except:
        distancia = 0
        ocupacao = 0
        cor = "#cbd5e1"
        cor2 = "#e2e8f0"
        status = "Sem dados"

    return render_template_string(
        HTML_TEMPLATE,
        distancia=round(distancia, 1),
        porcentagem=round(ocupacao),
        cor=cor,
        cor2=cor2,
        status=status
    )

@app.route("/update", methods=["POST"])
def update():
    dist = request.form.get("distancia")
    if dist:
        dados["distancia"] = dist
        print(f"✅ Recebido: {dist} cm")
        return "OK", 200
    return "Erro", 400
