//Digital Pins
//Motor Override Pins
#define MOTOR_OVERRIDE_BUTTON_PIN 12
#define MOTOR_OVERRIDE_LED_PIN 11

//RGB LED Pins
#define RED_RGB_LED_PIN 10
#define GREEN_RGB_LED_PIN 9

//Motor Control Pins
#define MOTOR_PIN_ENABLE 5
#define DIR_LEFT 3

//Analogue Pins
#define TEMP_SENSE_PIN A1

//Constants
const int tempReadInterval = 1000;         // Read Temperature every second
const int motorTempToggleInterval = 5000;  // Only act every 5 seconds


//Varibales
bool motorState = LOW;
bool motorOverride = LOW;

//Button Variables
bool lastButtonState = LOW;
unsigned long debounceDuration = 50;  // 50 milliseconds
unsigned long lastTimeButtonStateChanged = 0;

//Temperature controlled variables
unsigned long lastTimeTempRead = 0;
int motorStartTemp = 23;
unsigned long lastTimeMotorTempToggled = 0;

void setup() {
  Serial.begin(9600);

  //Set Pin Modes
  //Motor Override Pin
  pinMode(MOTOR_OVERRIDE_BUTTON_PIN, INPUT);
  pinMode(MOTOR_OVERRIDE_LED_PIN, OUTPUT);

  //Turns Fan on and off
  pinMode(MOTOR_PIN_ENABLE, OUTPUT);

  //RGB LED Pins
  pinMode(RED_RGB_LED_PIN, OUTPUT);
  digitalWrite(RED_RGB_LED_PIN, HIGH);
  pinMode(GREEN_RGB_LED_PIN, OUTPUT);

  //Fan Direction
  pinMode(DIR_LEFT, OUTPUT);
  digitalWrite(DIR_LEFT, HIGH);
}

void loop() {
  check_serial();
  check_override_button();
  check_temp();
}

//Checks the temperature and acts if above set limit
void check_temp() {
 if (millis() - lastTimeTempRead > tempReadInterval) {
    lastTimeTempRead = millis();
    int sensorValue = analogRead(TEMP_SENSE_PIN);
    float voltage = sensorValue * (5.0 / 1023.0);  //Calculate Voltage
    float temperatureK = voltage * 100.0;        // Convert voltage to Kelvin
    float temperatureC = temperatureK - 273.15;  // Convert Kelvin to Celsius
    temperatureC = round(temperatureC * 10.0) / 10.0;
    Serial.print("Temperature:");
    Serial.println(temperatureC, 1);

    //Calculate here so its only done once
    bool temp_exceeded = (temperatureC > motorStartTemp);
    //Lock the temperature control if within the interval, stops motor turning on an off repeatedly untill
    //the temperature stabilises below specified range.
    if (millis() - lastTimeMotorTempToggled > motorTempToggleInterval) {
      if (temp_exceeded && !motorState) {
        set_motor(HIGH);
        Serial.print("Temperature Control:");
        Serial.println(HIGH);
        lastTimeMotorTempToggled = millis();
      } else if (!motorOverride && motorState && !temp_exceeded) {
        set_motor(LOW);
        Serial.print("Temperature Control:");
        Serial.println(LOW);
        lastTimeMotorTempToggled = millis();
      }
    }
  }
}

//Changes the state of the motor from whats specified and toggles RGB LED accordingly.
void set_motor(bool state) {
  motorState = state;
  digitalWrite(MOTOR_PIN_ENABLE, state);
  //RGB Pins
  digitalWrite(GREEN_RGB_LED_PIN, state);
  digitalWrite(RED_RGB_LED_PIN, !state);
}

//Toggles whether motor override is on or off, I.E the motor override light bulb and whether the motor is on itself
void toggle_motor_override() {
  motorOverride = !motorOverride;
  Serial.print("Motor Override:");
  Serial.println(motorOverride);
  digitalWrite(MOTOR_OVERRIDE_LED_PIN, motorOverride);
  set_motor(motorOverride);
}

//Checks the motor override button to see if has been clicked and calls toggle_motor_override if it has been
void check_override_button() {
  //Lock the checking behind a debounce duration to allow the button to stabilise back to LOW state.
  if (millis() - lastTimeButtonStateChanged > debounceDuration) {
    byte buttonState = digitalRead(MOTOR_OVERRIDE_BUTTON_PIN);
    if (buttonState != lastButtonState) {
      lastTimeButtonStateChanged = millis();
      lastButtonState = buttonState;
      if (buttonState == HIGH) {
        toggle_motor_override();
      }
    }
  }
}

//Checks the serial and acts accordingly.
// 'm' - toggles motor override
// 'txx' - Sets temperature for when motor should turn on i.e 't24' turns motor on at 24 degrees
void check_serial() {
  if (Serial.available() > 0) {
    char instruction = Serial.read();
    //Toggle motor override
    if (instruction == 'm') {
      toggle_motor_override();
    } else if (instruction == 't') {
      String tempStr = "";
      delay(5); //Add tiny delay to allow it to buffer up
      while (Serial.available() > 0) {
        char nextChar = Serial.read();
        if (isdigit(nextChar)) {  //Ensure it is a digit (0 - 10)
          tempStr += nextChar;
        } else {
          break;  //Not a digit, stop reading.
        }
      }
      if (tempStr.length() > 0) {
        motorStartTemp = tempStr.toInt();
        Serial.print("Set start temperature:");
        Serial.println(motorStartTemp);
      }
    }
  }
}