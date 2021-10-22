#include <Arduino.h>
#include <Servo.h>

#define NUM_TUNING_SERVOS   6
Servo tuningServos[NUM_TUNING_SERVOS];
const uint8_t tuningServoPins[] = {7, 8, 9, 10, 11, 12};

void setup() {
    pinMode(13, OUTPUT);
    Serial.begin(115200);

    for (int i = 0; i < NUM_TUNING_SERVOS; i++) {
        tuningServos[i].attach(tuningServoPins[i]);
    }
}

void loop() {
    for (int val = 1000; val < 2000; val += 10) {
        for (int i = 0; i < NUM_TUNING_SERVOS; i++) {
            tuningServos[i].writeMicroseconds(val);
        }
        delay(10);
        Serial.println(val);
    }
    delay(500);
    for (int val = 2000; val > 1000; val -= 10) {
        for (int i = 0; i < NUM_TUNING_SERVOS; i++) {
            tuningServos[i].writeMicroseconds(val);
        }
        delay(10);
        Serial.println(val);
    }
    delay(500);
}