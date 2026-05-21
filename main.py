HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lixeiras Inteligentes</title>
    <meta http-equiv="refresh" content="3">   <!-- Atualiza a cada 3 segundos -->
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
