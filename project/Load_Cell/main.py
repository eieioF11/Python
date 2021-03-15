import matplotlib.pyplot as plt
from SerialConnection import select_port
import numpy as np
import datetime

def main():
    print("Start!")
    ser = select_port()
    if ser is None:
        return

    dt_now = datetime.datetime.now()
    path='data/'+dt_now.strftime('%Y%m%d%H%M%S_Log.csv')
    f = open(path, 'w')

    plt.figure()
    #x軸の幅を100にする
    xlim = [0, 10]
    X, Y = [], []
    xlim2 = [0, 10]
    X2, Y2 = [], []
    while True:
        try:
            ser.reset_input_buffer()
            ser.write(b'F')
            readdata=str(ser.readline().decode())
            data=readdata.replace('\r\n','')
            sensordata=data.split(',')
            try:
                m=float(sensordata[0])
            except:
                m=0

            try:
                temp=float(sensordata[1])
            except:
                temp=0

            if isinstance(m, float) and isinstance(temp, float):
                print(readdata)
                with open(path, 'a') as f:
                    dt_now = datetime.datetime.now()
                    f.write(dt_now.strftime('%Y/%m/%d(%H:%M:%S),')+str(m)+","+str(1)+",\n")

                #画面をクリア
                plt.cla()
                Y.append(m)
                X.append(len(Y))
                #xに100個以上格納されたら
                if len(X) > 10:
                    xlim[0] += 1
                    xlim[1] += 1

                Y2.append(temp)
                X2.append(len(Y2))
                #xに100個以上格納されたら
                if len(X2) > 10:
                    xlim2[0] += 1
                    xlim2[1] += 1

                plt.plot(X, Y,color = 'blue')
                plt.plot(X2, Y2,color = 'red')
                #x軸、y軸方向の表示範囲を設定
                plt.ylim(-1, 2)
                plt.xlim(xlim[0], xlim[1])
                #描写
                plt.pause(0.01)

        except KeyboardInterrupt:
            ser.close()
            break


if __name__ == "__main__":
    main()