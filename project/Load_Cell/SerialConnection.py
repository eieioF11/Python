import serial
from serial.tools import list_ports

def select_port():
    ser = serial.Serial()
    ser.baudrate = 9600    # ArduinoのSerial.beginで指定した値
    ser.timeout = 0.1       # タイムアウトの時間

    ports = list_ports.comports()    # ポートデータを取得

    devices = [info.device for info in ports]

    if len(devices) == 0:
        # シリアル通信できるデバイスが見つからなかった場合
        print("error: device not found")
        return None
    elif len(devices) == 1:
        print("only found %s" % devices[0])
        ser.port = devices[0]
    else:
        # ポートが複数見つかった場合それらを表示し選択させる
        for i in range(len(devices)):
            print("input %3d: open %s" % (i,devices[i]))
        print("input number of target port >> ",end="")
        num = int(input())
        ser.port = devices[num]

    # 開いてみる
    try:
        ser.open()
        return ser
    except:
        print("error when opening serial")
        return None
