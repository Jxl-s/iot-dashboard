#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

// WiFi connection
#define WIFI_SSID "Oooooooooo"
#define WIFI_PASSWORD "BalanceGame"

// MQTT
#define MQTT_HOST "172.20.10.7"
#define MQTT_NAME "intellihouse-iot"

// Pins
#define P_RESISTOR_PIN A0

// RFID Pins
#define SS_PIN D8
#define RST_PIN D0

// Define Topic 

#define MQTT_RFID_TOPIC "room/rfid_reader"
#define MQTT_LIGHT_TOPIC "room/light_intensity"

MFRC522 mfrc522(SS_PIN, RST_PIN);

long now = millis();
long lastTime = 0;

WiFiClient wifi_client;
PubSubClient client(wifi_client);

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("WiFi connected - ESP-8266 IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(String topic, byte *message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("wifi_client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 seconds");
      // Wait 5 seconds before retrying
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(MQTT_HOST, 1883);
  client.setCallback(callback);
  pinMode(P_RESISTOR_PIN, INPUT);
  SPI.begin();      
  mfrc522.PCD_Init();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  if (!client.loop())
    client.connect(MQTT_NAME);

  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    Serial.println("GOT CARD");

    String id = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      id += String(mfrc522.uid.uidByte[i], HEX);
      if (i < mfrc522.uid.size - 1)
        id += "-";
    }
  
    Serial.print("UID: ");
    Serial.println(id);

    client.publish(MQTT_RFID_TOPIC, id.c_str());

    mfrc522.PICC_HaltA();
    delay(5000);
  }

  now = millis();
  if(now - lastTime > 1000) {
    lastTime = now; 
    int value = analogRead(P_RESISTOR_PIN);
    String stringValue = String(value);
    client.publish(MQTT_LIGHT_TOPIC, stringValue.c_str());
  }
}
