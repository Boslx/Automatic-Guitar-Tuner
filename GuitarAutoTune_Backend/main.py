# From https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36
# This is a simple demonstration on how to stream
# audio from microphone and then extract the pitch
# and volume directly with help of PyAudio and Aubio
# Python libraries. The PyAudio is used to interface
# the computer microphone. While the Aubio is used as
# a pitch detection object. There is also NumPy
# as well to convert format between PyAudio into
# the Aubio.
import argparse
import os
import time
from enum import Enum

import aubio
import numpy as num
import pyaudio
import serial.tools.list_ports
from dotenv import load_dotenv
from pynput import keyboard

import chords
import servo

load_dotenv()

cheat_mode = True   # stops tuning once target frequency has ben reached once and stops perfecting it (looks better on video)

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE = 4096
CHANNELS = 1
FORMAT = pyaudio.paFloat32
METHOD = "default"
SAMPLE_RATE = 44100
HOP_SIZE = BUFFER_SIZE // 2
PERIOD_SIZE_IN_FRAME = HOP_SIZE
CHORD = chords.STANDARD_TONES

colorTuningDone =       0x004000
colorTuningInProgress = 0x401000
colorTuningNeeded =     0x400000

class Tuning(Enum):
    NOT_DONE = colorTuningNeeded
    IN_PROGRESS = colorTuningInProgress
    DONE = colorTuningDone

lastNotes = []
currentlyTuning = False
currentlyStopped = False
tuningProgress =  [Tuning.NOT_DONE for i in range(6)] # contains colors directly
prevTuningProgress = []

lastEmergencyStop = 0
manualModeWatchedString = None


def update_leds():
    global prevTuningProgress
    if (tuningProgress != prevTuningProgress):
        servo.set_leds(tuningProgress)
    prevTuningProgress = tuningProgress.copy()

def on_press(key):
    if hasattr(key, 'char'):
        for i in range(1, 7):
            if key.char == str(i):
                global manualModeWatchedString
                manualModeWatchedString = (i - 1)

def main(args):
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()

    # Initiating PyAudio object.
    pA = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pA.open(format=FORMAT, channels=CHANNELS,
                  rate=SAMPLE_RATE, input=True,
                  frames_per_buffer=PERIOD_SIZE_IN_FRAME)

    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
                             HOP_SIZE, SAMPLE_RATE)

    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-40)

    # Set LED colors
    update_leds()

    # Infinite loop!
    while True:
        # Always listening to the microphone.
        data = mic.read(PERIOD_SIZE_IN_FRAME, exception_on_overflow=False)
        # Convert into number that Aubio understand.
        samples = num.frombuffer(data, dtype=aubio.float_type)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]
        # Compute the energy (volume)
        # of the current frame.
        volume = num.sum(samples ** 2) / len(samples) * 10000
        # cutoff if volume is too silent
        # if volume < 5:
        #     currentlyTuning = False

        # disable servos every second to prevent issues with logic
        global lastEmergencyStop
        if (time.time() - lastEmergencyStop > 1.0):
            lastEmergencyStop = time.time()
            servo.stop_tuning_servos()

        global currentlyStopped, currentlyTuning
        currentlyTuning = (volume > 5)
        if (not currentlyStopped and not currentlyTuning):
            servo.stop_tuning_servos()
            servo.stop_tuning_servos()
            currentlyStopped = True
        if (not currentlyTuning):
            continue

        # Format the volume output so it only
        # displays at most six numbers behind 0.
        # volume = "{:6f}".format(volume)

        # Finally print the pitch and the volume.
        # print(str(pitch) + " " + str(volume))

        # Find the nearest note in Tones
        if manualModeWatchedString is not None:
            noteName = list(CHORD)[manualModeWatchedString]
            supposedPitch = CHORD[noteName]
        else:
            noteName, supposedPitch = min(CHORD.items(), key=lambda x: abs(pitch - x[1]))

        differenceHz = supposedPitch - pitch

        print(f"[{noteName}] {differenceHz:7.3f}  {volume}")

        lastNotes.insert(0, noteName)
        if (len(lastNotes) > 4):
            lastNotes.pop()
            if (len(set(lastNotes)) == 1):  # check if last 4 notes are the same
                doTuning(noteName, differenceHz)


def doTuning(noteName, differencePitch):
    global currentlyStopped, currentlyTuning
    servo_idx = list(CHORD.keys()).index(noteName)

    if (cheat_mode and tuningProgress[servo_idx] == Tuning.DONE):
        return
    
    if abs(differencePitch) > 40:
        tuningProgress[servo_idx] = Tuning.NOT_DONE
        update_leds()
        stopTuning()
        print("Difference between supposed and actual pitch above 40hz")
        return

    if abs(differencePitch) < 0.2:
        tuningProgress[servo_idx] = Tuning.DONE
        update_leds()
        stopTuning()
        return

    # set tuning color
    tuningProgress[servo_idx] = Tuning.IN_PROGRESS
    update_leds()

    currentlyTuning = True
    currentlyStopped = False

    if (abs(differencePitch) < 0.5):
        speed = 0.05
    elif (abs(differencePitch) < 1):
        speed = 0.1
    else:
        speed = 0.15

    if (differencePitch > 0):
        servo.set_tuning_servo(servo_idx, speed)
    else:
        servo.set_tuning_servo(servo_idx, -speed)


def stopTuning():
    global currentlyTuning, manualModeWatchedString
    currentlyTuning = False
    manualModeWatchedString = None


parser = argparse.ArgumentParser(description='Utility for automatically tuning musical instruments')

if __name__ == "__main__":
    serial_ports = serial.tools.list_ports.comports()
    ports = [p[0] for p in serial_ports]
    parser.add_argument('-d', '--device', choices=ports, required=False, help='Serial port of the Arduino',
                        default=os.getenv('GAT_SERIAL_PORT'))
    args = parser.parse_args()

    servo.init(args.device)

    print("Init done, ready for tuning!")
    main(args)
