#include <WiFi.h>
#include <HTTPClient.h>

// --- Wi-Fi ---
const char* ssid = "MARCIO";
const char* password = "1234567890";

// --- Sensores ---
const int trigPin = 3;      // HC-SR04
const int echoPin = 2;
const int doorPin = 4;      // Reed Switch (Porta)

const char* serverName = "https://servidor-esp32-com-hc-sr04-production.up.railway.app/update";

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(doorPin, INPUT_PULLUP);   // Importante: Pull-up interno

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado!");
}

void loop() {
  // Medição de distância
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000);
  float distancia = duration * 0.0343 / 2;

  // Leitura da porta
  bool portaAberta = digitalRead(doorPin) == HIGH;  // HIGH = aberta (depende da ligação)

  Serial.printf("📏 Distancia: %.1f cm | Porta: %s\n", 
                distancia, portaAberta ? "ABERTA" : "FECHADA");

  // Envio para o servidor
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String postData = "distancia=" + String(distancia, 1) + 
                     "&porta=" + String(portaAberta ? 1 : 0);

    int httpResponseCode = http.POST(postData);
    
    if (httpResponseCode > 0) {
      Serial.println("✅ Enviado com sucesso!");
    }
    http.end();
  }

  delay(3000);
}
