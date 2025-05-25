//required libraries
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h> //needed to install
#include <DHT.h> //for the DHT22 sensor (temp and humidity)

//LEDs for temperature
#define LED_blue 3
#define LED_green 4
#define LED_red 5

//setting OLED size in pixels
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

//setting OLED parameters
#define OLED_RESET -1 //so we know we're not using a separate line for a reset
#define SCREEN_ADDRESS 0x3C //I2C address

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

//values from callibrations
const int DryValue = 1023; 
const int WetValue = 720;

//variables for soil moisture
int soilMoistureValue; //value from the ADC output
int soilMoisturePercent; //displays on the OLED

#define SENSOR_IN A0

//buzzer pin
int buzzerPin = 8;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //setting up serial monitor
  analogReference(EXTERNAL);
  dht.begin(); //initialising temp/humid sensor
  //initialising I2C display
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);
  display.clearDisplay();
  pinMode(LED_blue, OUTPUT);
  pinMode(LED_green, OUTPUT);
  pinMode(LED_red, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  delay(200);
  // put your main code here, to run repeatedly:
  soilMoistureValue = analogRead(SENSOR_IN);
  //determining soil moisture percentage value
  soilMoisturePercent = map(soilMoistureValue, DryValue, WetValue, 0, 100); //gets percentage
  
  //keeping values betwee 0 and 100
  soilMoisturePercent = constrain(soilMoisturePercent, 0, 100);
  Serial.println("moisture:" + String(soilMoisturePercent)); //soil moisture percentage
  
  float temperature = dht.readTemperature(); //reading in temp in celsius from sensor
  float humidity = dht.readHumidity(); //reading in humidity in percentage from sensor

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.println("temperature:" + String(temperature)); //temperature value in celsius
    Serial.println("humidity:" + String(humidity)); //humidity value in %
  }

  Serial.println("callibration:" + String(soilMoistureValue)); //soil moisture percentage value for callibration

  if (!isnan(temperature)) {
    if (temperature >= -40 && temperature <= 10) {
      digitalWrite(LED_blue, HIGH);
      digitalWrite(LED_green, LOW);
      digitalWrite(LED_red, LOW);
    } else if (temperature >= 11 && temperature <= 30) {
      digitalWrite(LED_blue, HIGH);
      digitalWrite(LED_green, HIGH);
      digitalWrite(LED_red, LOW);
    } else if (temperature >= 31 && temperature <= 80) {
      digitalWrite(LED_blue, HIGH);
      digitalWrite(LED_green, HIGH);
      digitalWrite(LED_red, HIGH);
    } else {
      // If temperature is out of expected range
      digitalWrite(LED_blue, LOW);
      digitalWrite(LED_green, LOW);
      digitalWrite(LED_red, LOW);
    }
  }

  display.clearDisplay();

 //printing water moisture to oled
  display.setCursor(20,0);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.println("Moisture");
  display.setCursor(80, 0);
  display.setTextSize(1);
  // display.setTextColor(WHITE);
  display.print(soilMoisturePercent);
  display.println("%");

  //printing temperature to oled
  display.setCursor(20, 20);
  display.setTextSize(1);
  display.print("Temp: ");
  display.print(temperature);
  display.println(" C");

  //printing humidity to oled
  display.setCursor(20, 50);
  display.setTextSize(1);
  display.print("Humidity: ");
  display.print(humidity);
  display.println(" %");


  display.display(); //puts everything onto the OLED

  if (Serial.available() > 0)
  {
    int command = Serial.parseInt();
    if (command == 1)
    {
      digitalWrite(buzzerPin, HIGH);
    }
    else if (command == 0)
    {
      digitalWrite(buzzerPin, LOW);
    }
  }

  delay(2000);

}
