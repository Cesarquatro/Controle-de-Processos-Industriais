int pino_sensor = 15;
float leitura = 0;
float map_valor = 0;

void setup() {
  Serial.begin(115200);
  pinMode(pino_sensor, INPUT);
}

void loop() {
  leitura = analogRead(pino_sensor);               // Lê o valor analógico (0 a 4095)
  map_valor = (leitura / 4095.0) * 4.80;           // Mapeia para 0 - 4,80 V
  Serial.print(map_valor);
  Serial.println(" V");
  delay(100);
}
