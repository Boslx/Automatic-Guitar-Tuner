#include <Arduino.h>
#include <Servo.h>
#include <FastLED.h>

#define NUM_TUNING_SERVOS   6
Servo tuningServos[NUM_TUNING_SERVOS];
const uint8_t tuningServoPins[] = {7, 8, 9, 10, 11, 12};
#define TIMEOUT 100

#define NUM_LEDS 6
#define DATA_PIN 5
CRGB leds[NUM_LEDS];


uint8_t curParameterIdx = 0;
String curString;
uint32_t lastCommand = 0;

enum {
    PARSE_NONE,
    PARSE_SERVO,
    PARSE_LED
} parseMode_e;

uint8_t curParseMode = PARSE_NONE;

void parseReceivedMessage() {
    switch (curParseMode) {
        case PARSE_SERVO:
            if (curParameterIdx < NUM_TUNING_SERVOS) {
                int32_t val = curString.toInt();
                if (val >= 700 && val <= 2300) {
                    tuningServos[curParameterIdx].writeMicroseconds(val);
                    lastCommand = millis();
                    // Serial.println("Setting servo " + String(curParameterIdx) + " to " + String(val));
                }
                else {
                    // Serial.println("Received wrong value " + String(curString));
                }
            }
            break;
        case PARSE_LED:
            if (curParameterIdx < NUM_LEDS) {
                uint32_t val = strtol(curString.c_str(), 0, 16);
                leds[curParameterIdx] = CRGB(val);
            }
            break;
    }
}


void handleSerialByte(char c) {
    switch (curParseMode) {
        case PARSE_NONE:
            switch (c) {
                case 's':
                    curParseMode = PARSE_SERVO;
                    curString = "";
                    curParameterIdx = 0;
                    break;
                case 'l':
                    curParseMode = PARSE_LED;
                    curString = "";
                    curParameterIdx = 0;
                    break;
            }
            break;
        case PARSE_SERVO:
        case PARSE_LED:
            switch (c) {
                case ';':
                case '\n':
                    parseReceivedMessage();
                    if (curParseMode == PARSE_LED) {
                        FastLED.show();
                    }
                    curString = "";
                    curParameterIdx = 0;
                    curParseMode = PARSE_NONE;
                    break;
                case ',':
                    parseReceivedMessage();
                    curString = "";
                    curParameterIdx++;
                    break;
                default:
                    curString += c;
                    break;
            }
            break;
    }
    // Serial.print(c); // echo char
}

void stopServos() {
    for (int i = 0; i < NUM_TUNING_SERVOS; i++) {
        tuningServos[i].writeMicroseconds(1500);
    }
}

void fillLeds(CRGB color) {
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = color;
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

    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    fillLeds(CRGB::Black);
    FastLED.show();
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
