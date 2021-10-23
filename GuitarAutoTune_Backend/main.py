# From https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36
# This is a simple demonstration on how to stream
# audio from microphone and then extract the pitch
# and volume directly with help of PyAudio and Aubio
# Python libraries. The PyAudio is used to interface
# the computer microphone. While the Aubio is used as
# a pitch detection object. There is also NumPy
# as well to convert format between PyAudio into
# the Aubio.
import aubio
import numpy as num
import pyaudio
import sys
import os
import argparse
import serial.tools.list_ports
from dotenv import load_dotenv

import servo

load_dotenv()

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE = 2048
CHANNELS = 1
FORMAT = pyaudio.paFloat32
METHOD = "default"
SAMPLE_RATE = 44100
HOP_SIZE = BUFFER_SIZE // 2
PERIOD_SIZE_IN_FRAME = HOP_SIZE

referencePitch = 440


def frequency(referenceFrequency, semitonesDifference):
    return referenceFrequency * pow(2, (semitonesDifference / 12))


TONES = {
    'E4': frequency(referencePitch, -5.000),
    'B3': frequency(referencePitch, -10.000),
    'G3': frequency(referencePitch, -14.000),
    'D3': frequency(referencePitch, -19.000),
    'A2': frequency(referencePitch, -24.000),
    'E2': frequency(referencePitch, -29.000),
}


def main(args):
    # Initiating PyAudio object.
    pA = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pA.open(format=FORMAT, channels=CHANNELS,
                  rate=SAMPLE_RATE, input=True,
                  frames_per_buffer=PERIOD_SIZE_IN_FRAME
                  )

    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
                             HOP_SIZE, SAMPLE_RATE)

    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-40)

    # Infinite loop!
    while True:
        # Always listening to the microphone.
        data = mic.read(PERIOD_SIZE_IN_FRAME)
        # Convert into number that Aubio understand.
        samples = num.fromstring(data,
                                 dtype=aubio.float_type)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]
        # Compute the energy (volume)
        # of the current frame.
        # volume = num.sum(samples ** 2) / len(samples)
        # Format the volume output so it only
        # displays at most six numbers behind 0.
        # volume = "{:6f}".format(volume)

        # Finally print the pitch and the volume.
        # print(str(pitch) + " " + str(volume))

        # Find the nearest note in Tones
        noteName, supposedPitch = min(TONES.items(), key=lambda x: abs(pitch - x[1]))
        differenceHz = supposedPitch - pitch

        print(f"[{noteName}] {differenceHz}")

parser = argparse.ArgumentParser(description='Utility for automatically tuning musical instruments')

if __name__ == "__main__":
    serial_ports = serial.tools.list_ports.comports()
    ports = [p[0] for p in serial_ports]
    parser.add_argument('-d', '--device', choices=ports, required=False, help='Serial port of the Arduino', default=os.getenv('GAT_SERIAL_PORT'))
    args = parser.parse_args()

    servo.init(args.device)

    main(args)
