
#include "DHT.h"
#define DHTTYPE DHT22
int DHTPin = 7;
DHT dht(DHTPin, DHTTYPE); 

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
dht.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
int humedad_suelo = suelo();
float humedad_amb = dht.readHumidity();
float temperatura_amb = dht. readTemperature();
Serial.println("arduino_sala " + String(humedad_suelo) + " " + String(humedad_amb) + " " + String(temperatura_amb));
delay(2000);
}

int suelo(){
int min_dry = 248;
int max_dry = 568;
int sensor = analogRead(A0);
int value = (max_dry - sensor)*100/(max_dry - min_dry);
if (value <50){
    digitalWrite(5,HIGH);
    delay(300);
    digitalWrite(5,LOW);
    delay(300);
}else{
    digitalWrite(4, HIGH);
    delay(300);
    digitalWrite(4,LOW);
    delay(300);
}
return value;
}
