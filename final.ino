#include <WiFi.h>
#include <HTTPClient.h>
#include <MFRC522.h>
#include <TinyGPSPlus.h>



const char* ssid = "momo";
const char* password = "Omer1234";

#define RST_PIN 0
#define SS_PIN 5

MFRC522 mfrc522(SS_PIN, RST_PIN);
TinyGPSPlus gps;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  mfrc522.PCD_Init();
  Serial.println("RFID Reader initialized");

  Serial2.begin(9600, SERIAL_8N1, 16, 17);
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println("Card UID: " + uid);
    if (gps.encode(Serial2.read()))
    {
    if (gps.location.isValid()) {
      String lat = String(gps.location.lat(), 6);
      String lng = String(gps.location.lng(), 6);
      Serial.println("Latitude: " + lat + ", Longitude: " + lng);
      

      HTTPClient http;
      http.begin("http://192.168.43.206:5000/data/");
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      String data = "uid=" + uid + "&lat=" + lat + "&lng=" + lng;
      Serial.println(data);
      int httpCode = http.POST(data);



      if (httpCode > 0) {
        Serial.println("Data sent to server");
      } else {
        Serial.println("Error sending data to server");
      }
      http.end();
    }
    } else {
      Serial.println("Invalid GPS");
    }
  }
  }
