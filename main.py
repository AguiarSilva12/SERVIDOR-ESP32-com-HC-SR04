from flask import Flask, render_template_string, request, jsonify
import random
import time

app = Flask(__name__)

MAX_ALTURA = 120.0

# ====================== DADOS ======================
lixeiras = {
    1: {"distancia": 25.0, "porta": 0, "rssi": -68, "nome": "Lixeira 01", "ultima_atualizacao": time.strftime("%H:%M:%S")}
}

def gerar_dados_aleatorios():
    return round(random.uniform(8.0, 110.0), 1), random.randint(-85, -55)

for i in range(2, 6):
    dist, rssi = gerar_dados_aleatorios()
    lixeiras[i] = {
        "distancia": dist,
        "porta": 0,
        "rssi": rssi,
        "nome": f"Lixeira 0{i}",
        "ultima_atualizacao": "Aleatório"
    }

# ====================== ROTA DO ESP32 ======================
@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar_lixeira(id):
    if id != 1:
        return jsonify({"erro": "Apenas Lixeira 1"}), 400

    try:
        # Aceita tanto JSON quanto Form Data
        if request.is_json:
            dados = request.get_json()
        else:
            dados = request.form.to_dict()

        lixeiras[1]["distancia"] = float(dados.get("distancia"))
        lixeiras[1]["porta"] = int(dados.get("porta", 0))
        lixeiras[1]["rssi"] = int(dados.get("rssi", -70))
        lixeiras[1]["ultima_atualizacao"] = time.strftime("%H:%M:%S")

        print(f"✅ Atualização recebida: {lixeiras[1]['distancia']} cm")
        return jsonify({"status": "sucesso"}), 200

    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({"erro": str(e)}), 400


# ====================== TEMPLATES ======================
HOME_TEMPLATE = """ ... (coloque aqui seu HOME_TEMPLATE completo) ... """

DETAIL_TEMPLATE = """ ... (coloque aqui seu DETAIL_TEMPLATE completo) ... """


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

    # Cores e status
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

    porta_imagem = "https://i.imgur.com/rAWpErV.jpeg" if porta == 0 else "https://i.imgur.com/4IKIN7A.jpeg"
    porta_texto = "✅ Porta Fechada" if porta == 0 else "⚠️ Porta Aberta"

    return render_template_string(DETAIL_TEMPLATE,
        nome=data["nome"], distancia=round(distancia, 1), porcentagem=round(ocupacao),
        cor=cor, cor2=cor2, status=status,
        porta_imagem=porta_imagem, porta_texto=porta_texto, rssi=data["rssi"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
