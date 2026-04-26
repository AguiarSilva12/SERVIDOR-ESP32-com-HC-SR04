```python
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
        body {
            font-family: Arial;
            background: #f4f6f8;
            text-align: center;
        }

        .container {
            width: 80%;
            margin: auto;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }

        .progress-bg {
            width: 100%;
            background-color: #ddd;
            border-radius: 20px;
            height: 30px;
        }

        .progress-bar {
            height: 30px;
            border-radius: 20px;
            width: {{ porcentagem }}%;
            background-color: {{ cor }};
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>🗑️ Lixeira Inteligente</h1>

        <p>Autor: Márcio José Aguiar da Silva</p>
        <p>Atividade Extensionista III - Projeto de Eletrônica (754834)</p>

        <h2>{{ distancia }} cm</h2>

        <div class="progress-bg">
            <div class="progress-bar"></div>
        </div>

        <h3 style="color: {{ cor }};">{{ status }}</h3>
    </div>

    <script>
        setTimeout(() => location.reload(), 2000);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        val = float(dados["distancia"])

        porcentagem = max(0, min(100, 100 - val))

        if porcentagem < 30:
            cor = "green"
            status = "Lixeira Vazia"
        elif porcentagem < 70:
            cor = "orange"
            status = "Nível Médio"
        else:
            cor = "red"
            status = "Lixeira Cheia"

    except:
        val = 0
        porcentagem = 0
        cor = "gray"
        status = "Sem dados"

    return render_template_string(
        HTML_TEMPLATE,
        distancia=round(val, 2),
        porcentagem=porcentagem,
        cor=cor,
        status=status
    )

@app.route("/update", methods=["POST"])
def update():
    dist = request.form.get("distancia")

    if dist:
        dados["distancia"] = dist
        print("Recebido:", dist)
        return "OK", 200

    return "Erro", 400
```
