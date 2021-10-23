#include <Arduino.h>
#include <Servo.h>

#define NUM_TUNING_SERVOS   6
Servo tuningServos[NUM_TUNING_SERVOS];
const uint8_t tuningServoPins[] = {7, 8, 9, 10, 11, 12};
#define TIMEOUT 100


uint8_t curServoIdx = 0;
String curString;
uint32_t lastCommand = 0;

void parseReceivedMessage() {
    if (curServoIdx < NUM_TUNING_SERVOS) {
        int32_t val = curString.toInt();
        if (val >= 700 && val <= 2300) {
            tuningServos[curServoIdx].writeMicroseconds(val);
            lastCommand = millis();
            // Serial.println("Setting servo " + String(curServoIdx) + " to " + String(val));
        }
        else {
            // Serial.println("Received wrong value " + String(curString));
        }
    }
}

void handleSerialByte(char c) {
    switch (c) {
        case ';':
        case '\n':
            parseReceivedMessage();
            curString = "";
            curServoIdx = 0;
            break;
        case ',':
            parseReceivedMessage();
            curString = "";
            curServoIdx++;
            break;
        default:
            curString += c;
            break;
    }
    // Serial.print(c); // echo char
}

void stopServos() {
    for (int i = 0; i < NUM_TUNING_SERVOS; i++) {
        tuningServos[i].writeMicroseconds(1500);
    }
}

void setup() {
    pinMode(13, OUTPUT);
    Serial.begin(115200);
    Serial.println("AutoTuner init.");

    for (int i = 0; i < NUM_TUNING_SERVOS; i++) {
        tuningServos[i].writeMicroseconds(1500);
        tuningServos[i].attach(tuningServoPins[i]);
    }
}

void loop() {
    while (Serial.available()) {
        handleSerialByte(Serial.read());
    }
    if (millis() - lastCommand > TIMEOUT) {
        lastCommand = millis();
        stopServos();
    }
}
