from flask import Flask, request, render_template_string

app = Flask(__name__)

dados = {"distancia": 0}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lixeira Inteligente</title>
    <style>
        body { font-family: Arial; background: #f4f6f8; text-align: center; margin: 0; padding: 20px; }
        .container {
            max-width: 600px;
            margin: auto;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .progress-bg {
            width: 100%;
            background-color: #ddd;
            border-radius: 20px;
            height: 35px;
            margin: 20px 0;
        }
        .progress-bar {
            height: 35px;
            border-radius: 20px;
            width: {{ porcentagem }}%;
            background-color: {{ cor }};
            transition: width 0.5s;
        }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗑️ Lixeira Inteligente</h1>
        <p><strong>Márcio José Aguiar da Silva</strong></p>
        <p>Atividade Extensionista III</p>
        
        <h2>{{ distancia }} cm</h2>
        
        <div class="progress-bg">
            <div class="progress-bar"></div>
        </div>
        
        <h3 style="color: {{ cor }};">{{ status }}</h3>
    </div>

    <script>
        setTimeout(() => location.reload(), 2500);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        val = float(dados.get("distancia", 0))
        porcentagem = max(0, min(100, 100 - val))
        
        if porcentagem < 30:
            cor = "green"
            status = "🟢 Lixeira Vazia"
        elif porcentagem < 70:
            cor = "orange"
            status = "🟠 Nível Médio"
        else:
            cor = "red"
            status = "🔴 Lixeira Cheia"
    except:
        val = 0
        porcentagem = 0
        cor = "gray"
        status = "Sem dados"

    return render_template_string(
        HTML_TEMPLATE,
        distancia=round(val, 1),
        porcentagem=porcentagem,
        cor=cor,
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
