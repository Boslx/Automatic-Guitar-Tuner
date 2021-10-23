import serial
from dotenv import load_dotenv
import os
import time

load_dotenv()

ser = serial.Serial(os.getenv('GAT_SERIAL_PORT'), baudrate=115200)
time.sleep(2)   # wait until Arduino booted

def scale(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# servo id for string number 0-5, tuning speed between -1.0 and 1.0
def set_tuning_servo(servo_id, tuning_speed):
    # check if parameters are in range
    if (tuning_speed < -1.0 or tuning_speed > 1.0 or servo_id < 0 or servo_id > 5):
        return

    # build control string
    buf = ""
    for i in range(0, servo_id):
        buf += ','
    buf += str(scale(tuning_speed, -1.0, 1.0, 1000, 2000))
    for i in range(servo_id, 5):
        buf += ','
    buf += '\n'

    # print(buf)
    ser.write(buf.encode())
    
    pass


if __name__ == "__main__":
    # ser.write("1400,1500,1400,1500,1400,1500\n".encode())
    set_tuning_servo(0, 0)
    set_tuning_servo(5, 0.1)
    try:
        while (True):
            pass   
    except:
        pass