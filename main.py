from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Variável global para armazenar a última distância recebida
dados = {"distancia": "Aguardando..."}

HTML_TEMPLATE = '''
<html>
    <head><title>Monitor Railway</title><meta charset="UTF-8"></head>
    <body style="text-align: center; font-family: Arial;">
        <h1>Sensor HC-SR04 no Railway</h1>
        <div style="font-size: 40px; margin-top: 20px;">
            Distância: <b style="color: blue;">{{ distancia }} cm</b>
        </div>
        <script>setTimeout(function(){location.reload();}, 2000);</script>
    </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, distancia=dados["distancia"])

@app.route('/update', methods=['POST'])
def update():
    dist = request.form.get('distancia')
    if dist:
        dados["distancia"] = dist
        return "Recebido", 200
    return "Erro", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
