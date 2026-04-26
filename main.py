```python
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Armazena a distância recebida
dados = {"distancia": 0}

HTML_TEMPLATE = '''
<html>
<head>
    <title>Lixeira Inteligente</title>
    <meta charset="UTF-8">
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

        h1 {
            color: #333;
        }

        .info {
            font-size: 18px;
            color: #555;
            margin-bottom: 20px;
        }

        .distancia {
            font-size: 45px;
            margin: 20px 0;
        }

        .progress-bg {
            width: 100%;
            background-color: #ddd;
            border-radius: 20px;
            height: 35px;
        }

        .progress-bar {
            height: 35px;
            border-radius: 20px;
            width: {{ porcentagem }}%;
            background-color: {{ cor }};
            transition: width 0.5s, background-color 0.5s;
        }

        .status {
            margin-top: 15px;
            font-size: 22px;
            font-weight: bold;
            color: {{ cor }};
        }

        .rodape {
            margin-top: 30px;
            font-size: 14px;
            color: #777;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>🗑️ Lixeira Inteligente</h1>

        <div class="info">
            Atividade Extensionista III - Projeto de Eletrônica (754834)<br>
            Autor: <b>Márcio José Aguiar da Silva</b>
        </div>

        <div class="distancia">
            {{ distancia }} cm
        </div>

        <div class="progress-bg">
            <div class="progress-bar"></div>
        </div>

        <div class="status">
            {{ status }}
        </div>

        <p>Capacidade: 0 a 100%</p>

        <div class="rodape">
            Atualização automática a cada 2 segundos
        </div>
    </div>

    <script>
        setTimeout(() => location.reload(), 2000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    try:
        val = float(dados["distancia"])

        # Inverte: quanto menor a distância, mais cheia a lixeira
        porcentagem = max(0, min(100, 100 - val))

        # Define cor e status
        if porcentagem < 30:
            cor = "green"
            status = "🟢 Lixeira Vazia"
        elif porcentagem < 70:
            cor = "orange"
            status = "🟡 Nível Médio"
        else:
            cor = "red"
            status = "🔴 Lixeira Cheia"

    except:
        val, porcentagem, cor, status = 0, 0, "gray", "Sem dados"

    return render_template_string(
        HTML_TEMPLATE,
        distancia=round(val, 2),
        porcentagem=porcentagem,
        cor=cor,
        status=status
    )

@app.route('/update', methods=['POST'])
def update():
    dist = request.form.get('distancia')

    if dist:
        dados["distancia"] = dist
        print(f"Recebido: {dist} cm")
        return "OK", 200

    return "Erro", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
```
