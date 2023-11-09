#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

// RFID Pins
#define SS_PIN D8
#define RST_PIN D0

// WiFi connection
#define WIFI_SSID "ssid_here"
#define WIFI_PASSWORD "password_here"

// MQTT
#define MQTT_HOST "192.168.1.2"
#define MQTT_NAME "intellihouse-iot"

#define MQTT_RFID_TOPIC "room/rfid_reader"

MFRC522 mfrc522(SS_PIN, RST_PIN);

WiFiClient wifi_client;
PubSubClient client(wifi_client);

void setup_wifi() {
  delay(10);
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

void callback(String topic, byte* message, unsigned int length) {
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
    if (client.connect(MQTT_NAME)) {
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
  SPI.begin();      
  mfrc522.PCD_Init();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  if(!client.loop())
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
}