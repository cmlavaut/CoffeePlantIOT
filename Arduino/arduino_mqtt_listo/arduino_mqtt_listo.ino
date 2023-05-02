#include <UIPEthernet.h>
#include <PubSubClient.h>
#include "DHT.h"

#define CLIENT_ID       "ArduinoMQTT"
#define TOPIC           "sensores/3"
#define PUBLISH_DELAY   5000
#define DHTPIN          7
#define DHTTYPE         DHT22
#define mqttuser        "kmi"
#define mqttpassword    "$PH4Jb^pCdKqHL8KD5S!"

uint8_t mac[6] = {0xDE,0xED,0xBA,0xFE,0xFE,0xED};
//IPAddress mqttServer("darkn.duckdns.org");


EthernetClient ethClient;
PubSubClient mqttClient;
DHT dht(DHTPIN, DHTTYPE);

struct Valores{
  float value;
  int existencia;
};
 int sensornivel = 10;


long previousMillis;

void setup() {

  // setup serial communication
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(10, INPUT_PULLUP);
  
  // setup ethernet communication using DHCP
  if(Ethernet.begin(mac) == 0) {
    Serial.println(F("Unable to configure Ethernet using DHCP"));
    for(;;);
  }
  Serial.println(F("Ethernet configured via DHCP"));
  Serial.print("IP address: ");
  Serial.println(Ethernet.localIP());
  Serial.println();

  // setup mqtt client
  mqttClient.setClient(ethClient);
  mqttClient.setServer("darkn.duckdns.org", 1883);
  Serial.println(F("MQTT client configured"));

  // setup DHT sensor
  dht.begin();
  Serial.println(F("DHT sensor initialized"));

  Serial.println();
  Serial.println(F("Ready to send data"));
  previousMillis = millis();
}

void loop() {

  // it's time to send new data?
  if(millis() - previousMillis > PUBLISH_DELAY) {
    sendData();
    previousMillis = millis();
  }

  mqttClient.loop();
}

void sendData() {
  char bufferH[20];
  char bufferT[20];
  char bufferS[20];
  char message[50];
  Valores humedad_suelo = suelo();
  float humedad_amb = dht.readHumidity();
  float temperatura_amb = dht. readTemperature();
 // char message = "arduino_sala " + String(humedad_suelo.value) + " " + String(humedad_amb) + " " + String(temperatura_amb) + " "+ String(humedad_suelo.existencia);
  dtostrf(humedad_amb,3,2,bufferH);
  dtostrf(temperatura_amb,3,2,bufferT);
  dtostrf(humedad_suelo.value,3,2,bufferS);
  sprintf(message, "arduino_sala %s 80 5 %s %s %d",bufferS,bufferH,bufferT,humedad_suelo.existencia);
  Serial.println(message);
  
    
  if(mqttClient.connect(CLIENT_ID, mqttuser, mqttpassword)) {

    //mqttClient.publish(TOPIC, dtostrf(message, 6, 2, msgBuffer));
    mqttClient.publish(TOPIC, message);
  }
  else{
    Serial.println("ERROR");
  }
}

Valores suelo(){
Valores variable;
int min_dry = 248;
int max_dry = 568;
int sensor = analogRead(A0);
float abc = (max_dry - sensor)*100/(max_dry - min_dry);
variable.value = (max_dry - sensor)*100/(max_dry - min_dry);
//int sensornivel = digitalRead(10);
if (sensornivel < 10){
  digitalWrite(3, HIGH); // no hay agua
  digitalWrite(2,LOW); // motor off
  variable.existencia = 0; // no hay agua en la maceta
}
else if (variable.value <50){
    digitalWrite(5,HIGH);
    delay(300);
    digitalWrite(5,LOW);
    delay(300);
    digitalWrite(3,LOW); //si hay agua
    digitalWrite(2, HIGH); //motor en valor 1 es q esta encendido
    variable.existencia = 1; // hay agua en la maceta
}else{
    digitalWrite(4, HIGH);
    delay(300);
    digitalWrite(4,LOW);
    delay(300);
    digitalWrite(3,LOW); //si hay agua
    digitalWrite(2,LOW);// motor apagado
    variable.existencia = 1;
}
return variable;
}
