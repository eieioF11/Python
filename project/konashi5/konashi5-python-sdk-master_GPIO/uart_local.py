#!/usr/bin/python3

import serial
import time


with serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE) as ser:
    cnt = 0
    string = b''
    while True:
        # time.sleep(5)
        # cnt += 1
        # data_str = "Count: {}\n".format(cnt)
        # print("Write", data_str)
        # ser.write(bytes(data_str, "utf8"))
        ret = ser.read()
        if ret == b'\n':
            print(string.decode("utf8"))
            string = b''
        else:
            string += ret
