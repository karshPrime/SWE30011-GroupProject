
#include <LiquidCrystal.h>

//- Pin Definitions --------------------------------------------------------------------------------

#define PIR_PIN 2           // PIR motion sensor
#define LED_PIN 3           // LED indicator
#define BUZZER_PIN 4        // Buzzer for doorbell
#define BUTTON_PIN 5        // Doorbell button

LiquidCrystal lcd(6, 7, 8, 9, 10, 11);


//- Setup ------------------------------------------------------------------------------------------

void setup()
{
    pinMode(PIR_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    Serial.begin(9600);

    lcd.begin(16, 2);
    lcd.print("System Ready");

    bootMelody();
}


//- Main Loop --------------------------------------------------------------------------------------

void loop()
{
    static unsigned long ledOnTime = 0;
    static bool ledIsOn = false;

    // Parse serial input
    if (Serial.available())
    {
        String input = Serial.readStringUntil('\n');
        input.trim(); // remove extra spaces or newline

        if (input.startsWith("LCD")) { printCityAndTemperature(input); }
        else if (input == "alert")   { alertMelody(); }
    }

    if (digitalRead(PIR_PIN))
    {
        Serial.println("MS:1;");
        digitalWrite(LED_PIN, HIGH);
        ledOnTime = millis();
        ledIsOn = true;
    }

    if (!digitalRead(BUTTON_PIN))
    {
        Serial.println("BT:1;");
        buttonMelody();
    }

    if (ledIsOn && millis() - ledOnTime >= 50)
    {
        ledIsOn = false;
        digitalWrite(LED_PIN, LOW);
    }

    delay(100); // Faster transmission rate
}


//- LCD Control ------------------------------------------------------------------------------------

void printCityAndTemperature(String input)
{
    lcd.clear();

    int colonIndex = input.indexOf(':');
    int equalIndex = input.indexOf('=');

    if (colonIndex == -1 || equalIndex == -1 || equalIndex <= colonIndex)
    {
        lcd.setCursor(0, 0);
        lcd.print("Invalid input");
        return;
    }

    // Extract the city name
    String city = input.substring(colonIndex + 1, equalIndex);
    city.trim();
    lcd.setCursor(0, 0);
    lcd.print(city + ":");

    // Extract the temperature
    String temperature = input.substring(equalIndex + 1);
    temperature.trim();
    lcd.setCursor(0, 1);
    lcd.print(temperature + " celsius");
}


//- Buzzer Melody ----------------------------------------------------------------------------------

void melodyPlay(int *melody, int *durations, int len)
{
    for (int i = 0; i < len; i++)
    {
        int duration = 1000 / durations[i];
        tone(BUZZER_PIN, melody[i], duration);
        delay(duration * 1.1);
        noTone(BUZZER_PIN);
    }
}

void alertMelody()
{
    int melody[] = { 659, 523, 659, 523 };
    int durations[] = { 8, 4, 8, 4 };

    melodyPlay(melody, durations, 4);
}

void bootMelody()
{
    int melody[] = { 262, 294, 330 };  // C4, D4, E4
    int durations[] = { 4, 4, 4 };

    melodyPlay(melody, durations, 3);
}

void buttonMelody()
{
    int melody[] = { 600, 600, 600, 1000 };
    int durations[] = { 4, 4, 4, 6 };

    melodyPlay(melody, durations, 4);
}

