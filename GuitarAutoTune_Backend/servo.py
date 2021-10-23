import serial
import os
import time
from dotenv import load_dotenv

ser = serial.Serial()

def init(port):
    global ser
    ser = serial.Serial(port, baudrate=115200)
    time.sleep(2)   # wait until Arduino booted

def scale(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# servo id for string number 0-5, tuning speed between -1.0 and 1.0
def set_tuning_servo(servo_id, tuning_speed):
    # check if parameters are in range
    if (tuning_speed < -1.0 or tuning_speed > 1.0 or servo_id < 0 or servo_id > 5):
        return

    # build control string
    buf = "s"
    for i in range(0, servo_id):
        buf += ','
    buf += str(scale(tuning_speed, -1.0, 1.0, 1000, 2000))
    for i in range(servo_id, 5):
        buf += ','
    buf += '\n'

    # print(buf)
    ser.write(buf.encode())
    ser.flush()
    time.sleep(0.01)
    

def stop_tuning_servos():
    ser.write("1500,1500,1500,1500,1500,1500\n".encode())
    ser.flush()
    time.sleep(0.01)

if __name__ == "__main__":
    # ser.write("1400,1500,1400,1500,1400,1500\n".encode())
    load_dotenv()
    init(os.getenv('GAT_SERIAL_PORT'))
    set_tuning_servo(0, 0)
    set_tuning_servo(5, 0.1)
    try:
        while (True):
            pass   
    except:
        pass