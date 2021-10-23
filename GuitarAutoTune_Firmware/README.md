# Firmware

## Serial protocol
Baudrate: `115200`

Servo values are in range between 1000-2000.  
LED Values are between 000000 - FFFFFF.

### Protocol:  
Servo: `s<Servo1>,<Servo2>,...\n`

LED: `l<LED1>,<LED2>,...\n`

### Example:  
Servo: `s1500,1200,1000,2000,1500,1500\n`

LED: `lFFFFFF,FF0000,00FF00,0000FF\n`