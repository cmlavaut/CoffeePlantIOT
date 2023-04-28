#include <UIPEthernet.h>
#include <PubSubClient.h>
#include "DHT.h"

#define CLIENT_ID       "ArduinoMQTT"
#define PUBLISH_DELAY   5000
#define DHTPIN          7
#define DHTTYPE         DHT22

uint8_t mac[6] = {0x00,0x01,0x02,0x03,0x04,0x05};
//IPAddress mqttServer(192,168,50,155);
char mqttuser = "kmi";
char mqttpassword = "$PH4Jb^pCdKqHL8KD5S!";
char mqttTopic = "sensores/3";

EthernetClient ethClient;
PubSubClient mqttClient("darkn.duckdns.org", 1883, ethClient);
DHT dht(DHTPIN, DHTTYPE);

struct Valores{
  int value;
  int existencia;
};
 int sensornivel = 10; 



void setup() {

  // setup serial communication
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(10, INPUT_PULLUP);
  while(!Serial) {};
  Serial.println(F("MQTT Arduino Demo"));
  Serial.println();
  
  // setup ethernet communication using DHCP
  if(Ethernet.begin(mac) == 0) {
    Serial.println(F("Unable to configure Ethernet using DHCP"));
    for(;;);
  }
  Serial.println(F("Ethernet configured via DHCP"));
  Serial.print("IP address: ");
  Serial.println(Ethernet.localIP());
  Serial.println();
      // setup DHT sensor
  dht.begin();

}

void loop() {

  // it's time to send new data?
  if(!mqttClient.connected()){
    reconnect();
  }
  mqttClient.loop();
  static unsigned long lastPublishTime = 0;
  if (millis() - lastPublishTime > 5000) {
    sendData();
    lastPublishTime = millis();
}
}

void reconnect() {
  while (!mqttClient.connected()) {
    Serial.print("Conectando al servidor MQTT...");
    if (mqttClient.connect("arduinoClient", mqttuser, mqttpassword)) {
      Serial.println("Conectado!");
      mqttClient.subscribe(mqttTopic);
    } else {
      Serial.print("Error de conexión. Código de error: ");
      Serial.print(mqttClient.state());
      Serial.println(" Intentando de nuevo en 5 segundos...");
      delay(5000);
    }
  }
}


void sendData() {

  Valores humedad_suelo = suelo();
  float humedad_amb = dht.readHumidity();
  float temperatura_amb = dht. readTemperature();
  String message = "arduino_sala " + String(humedad_suelo.value) + " " + String(humedad_amb) + " " + String(temperatura_amb) + " "+ String(humedad_suelo.existencia);
  Serial.println(message);

  if(mqttClient.connect(CLIENT_ID, mqttuser, mqttpassword)) {
    mqttClient.publish(mqttTopic, message.c_str());
    delay(3000);
  } else{
    Serial.println("error: no se puedo publicar mensaje");

  }
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