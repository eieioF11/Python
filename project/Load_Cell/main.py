import matplotlib.pyplot as plt
import numpy as np
import serial

def main():
    print("Start")
    ser = serial.Serial('com3',9600,timeout=None)

    plt.figure()
    #x軸の幅を100にする
    xlim = [0, 10]
    X, Y = [], []
    xlim2 = [0, 10]
    X2, Y2 = [], []
    while True:
        try:
            ser.reset_input_buffer()
            data=ser.readline()
            try:
                m=int(data)/1000
            except:
                m=0
            print(m)
            #画面をクリア
            plt.cla()
            Y.append(m)
            X.append(len(Y))
            #xに100個以上格納されたら
            if len(X) > 10:
                xlim[0] += 1
                xlim[1] += 1

            Y2.append(0)
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