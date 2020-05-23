/*
 * HydroUnit_Standard.ino - Sketch that runs on HydroSoil standard HydroUnit for reporting soil data to HydroCore
 * Copyright (c) 2020 Blake Tourneur - On behalf of the HydroSoil team 
 * Only for use on official HydroUnit Standard
 */

// Import libraries
#include <ESP8266WiFi.h>          // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h>         // Library for connection and data transmission to MQTT Server

// Pins and settings
const int ledPin = D4;            // Built-in LED in the Arduino for troubleshooting
const int soilSensor = A0;        // External soil sensor for taking measurements
int soilValue;                    // Variable to store readings from the soil sensor
const int powerLED = D5;          // Red power indicator LED
const int statusLED = D6;         // Green transmission status LED
const int waterLED = D7;          // Blue irrigation indicator LED
bool mqttConnected = false;       // Connection status to HydroCore
int ledState = LOW;               // Whether the connection LED is on or off
unsigned long previousMillis = 0; // Store the last time the LED was on

// WiFi credidentials
const char* ssid = "Blake_GS8";
const char* wifi_password = "Blue67@@";

// MQTT server details to connect to HydroCore
const char* mqtt_server = "hydrosoilmainunit.local";
const char* mqtt_topic = "HydroSoil Data";
const char* mqtt_username = "SoilMeasurer";
const char* mqtt_password = "HydroSoil123";
const char* clientID = "SB57432";

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(powerLED, OUTPUT);
  pinMode(statusLED, OUTPUT);
  pinMode(waterLED, OUTPUT);
  pinMode(soilSensor, INPUT);

  // Switch the on-board LED off to start with, and the power indicator LED
  digitalWrite(ledPin, HIGH);
  digitalWrite(powerLED, HIGH);
  
  // Begin Serial at 9600 baud and print debugging info
  Serial.begin(9600);
  Serial.println("Welcome to HydroUnit v1.0 - Debugging Session");
  Serial.println("---------------------------------------------");
  Serial.print("Connecting to Wifi Network: ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection has been confirmed
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  // Debugging - Output the IP Address of the HydroUnit
  Serial.println("WiFi connected successfully");
  Serial.print("HydroUnit IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("---------------------------------------------");
}

void loop() {
  // Establish connection to MQTT Broker
  Serial.println("Connecting to HydroCore MQTT Server");
  while (mqttConnected == false){
    if (client.connect(clientID, mqtt_username, mqtt_password)) {
      Serial.print("Connected to HydroCore as HydroUnit ID ");
      Serial.println(String(clientID));
      mqttConnected == true;
      break;
    }
    else {
      Serial.println("Connection to HydroCore failed, trying again...");
    }

    if (millis() - previousMillis >= 1000){ // For blinking the status LED
      if (ledState == LOW){
        digitalWrite(statusLED, HIGH);
        ledState = HIGH;
      } else {
        digitalWrite(statusLED, LOW);
        ledState = LOW;
      }
      previousMillis = millis();
    }
  }
  digitalWrite(statusLED, HIGH); // Turn status LED solid on
  Serial.println("---------------------------------------------");

  while (true) {
    soilValue = analogRead(soilSensor);
    soilValue = soilValue / 8.42;
    digitalWrite(ledPin, LOW);
    String payload = "00000" + String(clientID) + ": " + String(soilValue);
  
    // Publish soil value to the MQTT Broker
    if (client.publish(mqtt_topic, (char*) payload.c_str())) {
      Serial.println("Soil moisture data sent to HydroCore");
    }
    else {
      Serial.println("Soil moisture data failed to send. Connection to HydroCore may have been terminated. Restarting code...");
      ESP.restart();
    }
    digitalWrite(ledPin, HIGH);
    delay(1000);
  }
}
