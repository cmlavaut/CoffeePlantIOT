
#include "DHT.h"
#define DHTTYPE DHT22
int DHTPin = 7;
DHT dht(DHTPin, DHTTYPE); 
struct Valores{
  int value;
  int existencia;
};
 int sensornivel = 10; 
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
pinMode(3, OUTPUT);
pinMode(10, INPUT_PULLUP);
dht.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
Valores humedad_suelo = suelo();
float humedad_amb = dht.readHumidity();
float temperatura_amb = dht. readTemperature();
Serial.println("arduino_sala " + String(humedad_suelo.value) + " " + String(humedad_amb) + " " + String(temperatura_amb) + " "+ String(humedad_suelo.existencia));
delay(2000);
}

Valores suelo(){
Valores valores;
int min_dry = 248;
int max_dry = 568;
int sensor = analogRead(A0);
valores.value = (max_dry - sensor)*100/(max_dry - min_dry);
int sensornivel = digitalRead(10);
if (sensornivel !=0){
  digitalWrite(3, LOW); // motor off
  valores.existencia = 0; // no hay agua en la maceta
}
else if (valores.value <50){
    digitalWrite(5,HIGH);
    delay(300);
    digitalWrite(5,LOW);
    delay(300);
    digitalWrite(3, HIGH); //motor en valor 1 es q esta encendido
    valores.existencia = 1; // hay agua en la maceta
}else{
    digitalWrite(4, HIGH);
    delay(300);
    digitalWrite(4,LOW);
    delay(300);
    digitalWrite(3,LOW);// motor apagado
    valores.existencia = 1;
}
return valores;
}
