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

  // === Upload status: MS:x;BT:y; every 500ms ===
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

// === Parse command from Edge in format: BT:x;MS:y; ===
void parseAndExecuteCommand(String command) {
  int btValue = -1;
  int msValue = -1;

  // Extract BT value
  int btIndex = command.indexOf("BT:");
  if (btIndex != -1) {
    btValue = command.substring(btIndex + 3, command.indexOf(";", btIndex)).toInt();
  }

  // Extract MS value
  int msIndex = command.indexOf("MS:");
  if (msIndex != -1) {
    msValue = command.substring(msIndex + 3).toInt();
  }

  // === Control LED based on MS ===
  if (msValue == 0) {
    digitalWrite(LED_PIN, LOW);
    ledIsOn = false;
  } else if (msValue >= 1 && msValue <= 3) {
    digitalWrite(LED_PIN, HIGH);
    ledIsOn = true;
    ledOnTime = millis();  // Start LED timer
  }

  // === Ring the doorbell if BT == 1 ===
  if (btValue == 1) {
    playMelody();
  }

  // === Update LCD content based on MS ===
  lcd.clear();
  lcd.setCursor(0, 0);
  switch (msValue) {
    case 1:
      lcd.print("Warning, please");
      lcd.setCursor(0, 1);
      lcd.print("leave!");
      break;
    case 2:
      lcd.print("Welcome to");
      lcd.setCursor(0, 1);
      lcd.print("smart room!");
      break;
    case 3:
      lcd.print("We need HD!");
      break;
    default:
      lcd.print("System Ready");
      break;
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
