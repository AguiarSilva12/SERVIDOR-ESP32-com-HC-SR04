from flask import Flask, request, render_template_string

app = Flask(__name__)

# Dicionário de dados inicializado
dados = { "distancia": 0.0, "porta": 0, "rssi": -50 }
MAX_ALTURA = 120.0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lixeira Inteligente</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; text-align: center; margin: 0; padding: 15px; min-height: 100vh; }
        .container { max-width: 620px; margin: 20px auto; padding: 25px 20px; background: url('https://i.imgur.com/SUA_IMAGEM_DIRETA.jpg') center/cover no-repeat; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); color: white; position: relative; min-height: 500px; }
        .container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.68); border-radius: 25px; z-index: 1; }
        .content { position: relative; z-index: 2; }
        .wifi-indicator { position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.6); padding: 6px 12px; border-radius: 12px; font-size: 0.9em; z-index: 3; display: flex; align-items: center; gap: 6px; }
        h1 { margin: 10px 0 5px 0; font-size: 1.8em; text-shadow: 0 3px 10px rgba(0,0,0,0.9); }
        .progress-bg { width: 100%; height: 52px; background-color: rgba(255,255,255,0.25); border-radius: 30px; margin: 20px 0; overflow: hidden; position: relative; }
        .progress-bar { height: 100%; width: {{ porcentagem }}%; background-color: {{ 'red' if porcentagem >= 95 else 'orange' if porcentagem >= 75 else 'green' }}; transition: width 0.5s ease; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 50%; transform: translateY(-50%); font-weight: bold; color: white; text-shadow: 1px 1px 3px black; }
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi-indicator">📶 RSSI: {{ dados.rssi }} dBm</div>
        <div class="content">
            <h1>Lixeira Inteligente</h1>
            <p>Status da Porta: {{ 'Aberta' if dados.porta == 1 else 'Fechada' }}</p>
            <p>Distância Atual: {{ dados.distancia }} cm</p>
            
            <div class="progress-bg">
                <div class="progress-bar"></div>
                <div class="progress-text">{{ porcentagem }}% Cheia</div>
            </div>
        </div>
    </div>

    <script>
        // Elemento de áudio configurado com um som de bipe online padrão
        const alarme = new Audio('google.com');
        alarme.loop = true; // Repete o som enquanto a lixeira estiver cheia

        const porcentagem = {{ porcentagem }};

        // Função para ativar/desativar o som baseado na porcentagem
        function verificarAlarme() {
            if (porcentagem >= 95) {
                // O navegador exige interação do usuário antes de tocar áudio automaticamente
                alarme.play().catch(e => console.log("Aguardando clique do usuário para ativar som."));
            } else {
                alarme.pause();
                alarme.currentTime = 0;
            }
        }

        // Tenta tocar o alarme ao carregar a página
        window.addEventListener('load', verificarAlarme);
        // Toca também ao primeiro clique do usuário na tela (desbloqueio do navegador)
        window.addEventListener('click', verificarAlarme);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Cálculo da porcentagem baseada na distância medida pelo sensor
    if dados["distancia"] >= MAX_ALTURA:
        porcentagem = 0
    elif dados["distancia"] <= 10: # Lixeira cheia próxima a 10cm do sensor
        porcentagem = 100
    else:
        porcentagem = int(((MAX_ALTURA - dados["distancia"]) / MAX_ALTURA) * 100)
    
    porcentagem = max(0, min(100, porcentagem)) # Limita entre 0 e 100
    return render_template_string(HTML_TEMPLATE, dados=dados, porcentagem=porcentagem)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    # Rota para receber os dados via ESP32 / ESP8266
    dados["distancia"] = float(request.form.get('distancia', dados["distancia"]))
    dados["porta"] = int(request.form.get('porta', dados["porta"]))
    dados["rssi"] = int(request.form.get('rssi', dados["rssi"]))
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
