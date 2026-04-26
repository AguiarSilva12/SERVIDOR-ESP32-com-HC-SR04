from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Armazenamos como número para a lógica da barra
dados = {"distancia": 0}

HTML_TEMPLATE = '''
<html>
    <head>
        <title>Monitor Railway</title>
        <meta charset="UTF-8">
        <style>
            .container { width: 80%; margin: auto; text-align: center; font-family: Arial; }
            .progress-bg { width: 100%; background-color: #ddd; border-radius: 20px; height: 30px; margin-top: 20px; }
            .progress-bar { 
                height: 30px; 
                background-color: #4CAF50; 
                border-radius: 20px; 
                transition: width 0.5s ease-in-out; 
                width: {{ porcentagem }}%; 
            }
        </style>
    </head>
    <body class="container">
        <h1>Sensor HC-SR04</h1>
        <div style="font-size: 40px;">
            Distância: <b style="color: blue;">{{ distancia }} cm</b>
        </div>
        
        <div class="progress-bg">
            <div class="progress-bar"></div>
        </div>
        <p>Alcance visual: 0 a 100cm</p>

        <script>setTimeout(function(){location.reload();}, 2000);</script>
    </body>
</html>
'''

@app.route('/')
def index():
    # Calcula porcentagem para a barra (limite de 100cm para o exemplo)
    try:
        val = float(dados["distancia"])
        porcentagem = min(val, 100) # Limita a barra em 100%
    except:
        val, porcentagem = 0, 0
        
    return render_template_string(HTML_TEMPLATE, distancia=val, porcentagem=porcentagem)

@app.route('/update', methods=['POST'])
def update():
    # O Railway exige que o ESP32 envie como Form Data ou JSON
    dist = request.form.get('distancia')
    if dist:
        dados["distancia"] = dist
        print(f"Log: Recebido {dist}cm") # Aparece nos logs do Railway
        return "Recebido", 200
    return "Erro no dado", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
