#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi connection
#define WIFI_SSID "ssid_here"
#define WIFI_PASSWORD "password_here"

// MQTT
#define MQTT_HOST "192.168.1.2"
#define MQTT_NAME "intellihouse-iot"

#define MQTT_LIGHT_TOPIC "room/light_intensity"

// Pins
#define P_RESISTOR_PIN A0

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
  pinMode(P_RESISTOR_PIN, INPUT);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  if (!client.loop())
    client.connect(MQTT_NAME);

  int value = analogRead(P_RESISTOR_PIN);
  String stringValue = String(value);
  client.publish(MQTT_LIGHT_TOPIC, stringValue.c_str());

  delay(1000);
}
