#include <Arduino.h>
#include <Servo.h>

#define NUM_TUNING_SERVOS   6
Servo tuningServos[NUM_TUNING_SERVOS];
const uint8_t tuningServoPins[] = {7, 8, 9, 10, 11, 12};


uint8_t curServoIdx = 0;
String curString;

void parseReceivedMessage() {
    if (curServoIdx < NUM_TUNING_SERVOS) {
        int32_t val = curString.toInt();
        if (val >= 700 && val <= 2300) {
            tuningServos[curServoIdx].writeMicroseconds(val);
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
    Serial.print(c);
}

void setup() {
    pinMode(13, OUTPUT);
    Serial.begin(115200);

    for (int i = 0; i < NUM_TUNING_SERVOS; i++) {
        tuningServos[i].attach(tuningServoPins[i]);
        tuningServos[i].writeMicroseconds(1500);
    }
}

void loop() {
    while (Serial.available()) {
        handleSerialByte(Serial.read());
    }
}