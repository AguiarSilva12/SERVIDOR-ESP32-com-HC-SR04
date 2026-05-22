from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

dados = {
    "distancia": 25.0,
    "porta": 0,
    "rssi": -50,
    "ultima_atualizacao": time.strftime("%H:%M:%S")
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Lixeira Inteligente</title>
<style>
body { font-family: Arial; background: #0f172a; color: white; text-align: center; }
.container { padding: 20px; }

.progress-bg {
    width: 100%;
    background: #333;
    height: 30px;
    border-radius: 10px;
}

.progress-bar {
    height: 100%;
    width: {{ porcentagem }}%;
    background: green;
}
</style>
</head>

<body>

<div class="container">
<h1>🗑️ Lixeira</h1>

<h2>{{ distancia }} cm</h2>

<div class="progress-bg">
<div class="progress-bar"></div>
</div>

<p>Status: {{ status }}</p>
<p>🚪 Porta: {{ porta_texto }}</p>
<p>📶 WiFi: {{ rssi }}</p>
<p>⏰ {{ ultima_atualizacao }}</p>

</div>

</body>
</html>
"""   # ✅ IMPORTANTE: FECHADO AQUI

@app.route("/")
def index():
    val = float(dados.get("distancia", 0))
    porcentagem = max(0, min(100, 100 - (val / 1.2)))

    if porcentagem <= 30:
        status = "🟢 Vazia"
    elif porcentagem <= 70:
        status = "🟡 Média"
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

@app.route("/update", methods=["POST"])
def update():
    try:
        dados["distancia"] = float(request.form.get("distancia", 0))
        dados["porta"] = int(request.form.get("porta", 0))
        dados["rssi"] = int(request.form.get("rssi", -100))
        dados["ultima_atualizacao"] = time.strftime("%H:%M:%S")

        return "OK", 200

    except Exception as e:
        print("Erro:", e)
        return "Erro", 400
