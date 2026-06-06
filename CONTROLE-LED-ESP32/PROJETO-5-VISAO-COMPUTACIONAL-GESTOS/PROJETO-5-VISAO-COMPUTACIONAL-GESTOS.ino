#define PINO_LED 2

void setup() {
  Serial.begin(115200);

  pinMode(PINO_LED, OUTPUT);
  digitalWrite(PINO_LED, LOW);

  Serial.println("ESP32 pronto");
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando == 'L') {
      digitalWrite(PINO_LED, HIGH);
      Serial.println("LED ligado");
    }

    else if (comando == 'D') {
      digitalWrite(PINO_LED, LOW);
      Serial.println("LED desligado");
    }
  }
}