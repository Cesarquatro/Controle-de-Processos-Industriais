import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM17'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200

dataList = {"Tempo(s)"    :[], 
            "Setpoint"    :[], 
            "Valor Atual" :[],
            "Erro"        :[],
            "Saída PWM"   :[]}
Keys = list(dataList.keys())

def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=0.1)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = ser.readline().decode('utf-8')
        # reading is a string...do whatever you want from here
        #print(reading, end='')
        
        try:
            reading = [float(value) for value in reading.strip().split(',')]
            print(len(reading))
            for i in range(len(reading)):
                dataList[Keys[i]].append(reading[i])
        except:
            #print("Error")
            pass
        for key in Keys:
            #limit the list to 50 elements
            dataList[key] = dataList[key][-50:]
            #print(f"{key}: {dataList[key]}")
        #dataList = dataList[-50:]
        #print("dataList")
        #print(dataList)


if __name__ == "__main__":
    main()
    