import serial
# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM17'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200


def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=0.1)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = ser.readline().decode('utf-8')
        # reading is a string...do whatever you want from here
        print(reading, end='')


if __name__ == "__main__":
    main()
    