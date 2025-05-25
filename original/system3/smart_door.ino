#include <LiquidCrystal.h>

// === Pin Definitions ===
#define PIR_PIN 2           // PIR motion sensor
#define LED_PIN 3           // LED indicator
#define BUZZER_PIN 4        // Buzzer for doorbell
#define BUTTON_PIN 5        // Doorbell button

// === LCD1602 Wiring: RS, E, D4, D5, D6, D7 ===
LiquidCrystal lcd(6, 7, 8, 9, 10, 11);

// === Variables for receiving serial command ===
String inputString = "";
bool stringComplete = false;

unsigned long ledOnTime = 0;
bool ledIsOn = false;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.print("System Ready");
}

void loop() {
  // === Process command from Edge (if available) ===
  if (stringComplete) {
    parseAndExecuteCommand(inputString);
    inputString = "";
    stringComplete = false;
  }

  // === Handle LED timeout (turn off after 5 seconds) ===
  if (ledIsOn && millis() - ledOnTime >= 5000) {
    digitalWrite(LED_PIN, LOW);
    ledIsOn = false;
  }

  // === Upload status: MS:x;BT:y; ===
  int msState = digitalRead(PIR_PIN);
  int btState = (digitalRead(BUTTON_PIN) == LOW) ? 1 : 0;
  Serial.print("MS:");
  Serial.print(msState);
  Serial.print(";BT:");
  Serial.print(btState);
  Serial.println(";");

  delay(500);  // Faster transmission rate
}

// === Serial event: collect one full command line ===
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

// === Parse new format: BUZ:0/1;LED:0/1;LCD:xx.xx; ===
void parseAndExecuteCommand(String command) {
  int buzVal = -1;
  int ledVal = -1;
  String lcdText = "";

  // Extract BUZ value
  int buzIndex = command.indexOf("BUZ:");
  if (buzIndex != -1) {
    buzVal = command.substring(buzIndex + 4, command.indexOf(";", buzIndex)).toInt();
    digitalWrite(BUZZER_PIN, buzVal == 1 ? HIGH : LOW);
  }

  // Extract LED value
  int ledIndex = command.indexOf("LED:");
  if (ledIndex != -1) {
    ledVal = command.substring(ledIndex + 4, command.indexOf(";", ledIndex)).toInt();
    digitalWrite(LED_PIN, ledVal == 1 ? HIGH : LOW);
    if (ledVal == 1) {
      ledOnTime = millis();  // start timeout
      ledIsOn = true;
    } else {
      ledIsOn = false;
    }
  }

  // Extract LCD text
  int lcdIndex = command.indexOf("LCD:");
  if (lcdIndex != -1) {
    int endIndex = command.indexOf(";", lcdIndex);
    if (endIndex != -1) {
      lcdText = command.substring(lcdIndex + 4, endIndex);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("LCD:");
      lcd.setCursor(0, 1);
      lcd.print(lcdText);
    }
  }
}

// === Doorbell melody function ===
void playMelody() {
  int melody[] = {659, 523, 659, 523};
  int durations[] = {8, 4, 8, 4};

  for (int i = 0; i < 4; i++) {
    int duration = 1000 / durations[i];
    tone(BUZZER_PIN, melody[i], duration);
    delay(duration * 1.3);
    noTone(BUZZER_PIN);
  }
}
