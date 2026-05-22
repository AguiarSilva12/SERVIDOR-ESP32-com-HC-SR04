from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

# ================== DADOS ==================
dados = {
    "distancia": 25.0,
    "porta": 0,
    "rssi": -50,
    "ultima_atualizacao": time.strftime("%H:%M:%S")
}

# ================== HTML ==================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lixeira Inteligente</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: #0f172a; 
            color: white; 
            text-align: center; 
            margin: 0; 
            padding: 20px; 
        }
        .container {
            max-width: 700px;
            margin: auto;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
        }
        .progress-bg {
            width: 100%;
            background-color: #334155;
            border-radius: 20px;
            height: 40px;
            margin: 20px 0;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            width: {{ porcentagem }}%;
            background: linear-gradient(90deg, #22c55e, #ef4444);
            display: flex;
