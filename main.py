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
        return jsonify({"erro": "Apenas a Lixeira 1"}), 400

    try:
        # Aceita tanto JSON quanto Form Data
        if request.is_json:
            dados = request.get_json()
        else:
            dados = request.form

        lixeiras[1]["distancia"] = float(dados.get("distancia"))
        lixeiras[1]["porta"] = int(dados.get("porta", 0))
        lixeiras[1]["rssi"] = int(dados.get("rssi", -70))
        lixeiras[1]["ultima_atualizacao"] = time.strftime("%H:%M:%S")

        print(f"✅ Lixeira 1 atualizada: {lixeiras[1]['distancia']} cm")
        return jsonify({"status": "sucesso"}), 200

    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({"erro": str(e)}), 400


# ====================== TEMPLATES (mesmo de antes) ======================
# ... (HOME_TEMPLATE e DETAIL_TEMPLATE mantidos iguais) ...

# Cole aqui os templates que você já tem (HOME_TEMPLATE e DETAIL_TEMPLATE)

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE, lixeiras=lixeiras)

@app.route("/lixeira/<int:id>")
def detalhe_lixeira(id):
    # ... (seu código anterior aqui) ...
    pass  # mantenha o que você já tem

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
