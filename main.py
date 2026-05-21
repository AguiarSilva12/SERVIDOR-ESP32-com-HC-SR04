from flask import Flask, render_template_string, request, jsonify
import random
import time

app = Flask(__name__)

MAX_ALTURA = 120.0

# ====================== DADOS DAS LIXEIRAS ======================
lixeiras = {
    1: {
        "distancia": 25.0,
        "porta": 0,
        "rssi": -68,
        "nome": "Lixeira 01",
        "ultima_atualizacao": time.strftime("%H:%M:%S")
    }
}

def gerar_dados_aleatorios():
    distancia = round(random.uniform(8.0, 110.0), 1)
    rssi = random.randint(-85, -55)
    return distancia, rssi

for i in range(2, 6):
    distancia, rssi = gerar_dados_aleatorios()
    lixeiras[i] = {
        "distancia": distancia,
        "porta": 0,
        "rssi": rssi,
        "nome": f"Lixeira 0{i}",
        "ultima_atualizacao": "Aleatório"
    }

# ====================== ROTA PARA ESP32 ======================
@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar_lixeira(id):
    if id != 1:
        return jsonify({"erro": "Apenas Lixeira 1"}), 400

    try:
        dados = request.get_json(force=True)
        
        lixeiras[1]["distancia"] = float(dados.get("distancia"))
        lixeiras[1]["porta"] = int(dados.get("porta", 0))
        lixeiras[1]["rssi"] = int(dados.get("rssi", -70))
        lixeiras[1]["ultima_atualizacao"] = time.strftime("%H:%M:%S")

        print(f"✅ Lixeira 1 atualizada: {lixeiras[1]['distancia']} cm")
        return jsonify({"status": "sucesso"}), 200

    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({"erro": str(e)}), 400


# ====================== HOME TEMPLATE (com refresh) ======================
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lixeiras Inteligentes</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body {font-family: Arial, sans-serif; background: #0f172a; color: white; margin: 0; padding: 20px; min-height: 100vh;}
        h1 { text-align: center; margin-bottom: 30px; }
        .grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1400px; margin: 0 auto;}
        .card {background: rgba(255,255,255,0.1); border-radius: 20px; padding: 20px; text-align: center; cursor: pointer; transition: all 0.3s; box-shadow: 0 8px 20px rgba(0,0,0,0.4);}
        .card:hover {transform: scale(1.05); background: rgba(255,255,255,0.2);}
        .card h3 { margin: 10px 0; }
        .progress-small {height: 12px; background: #333; border-radius: 10px; margin: 10px 0; overflow: hidden;}
        .progress-fill {height: 100%; background: linear-gradient(90deg, #22c55e, #ef4444);}
        .time {font-size: 0.8em; color: #94a3b8;}
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
            <small>📶 {{ data.rssi }} dBm</small><br>
            <small class="time">Atualizado: {{ data.ultima_atualizacao }}</small>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# ====================== ROTAS ======================
@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE, lixeiras=lixeiras)

# (Mantenha sua rota /lixeira/<id> anterior aqui)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
