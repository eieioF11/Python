import matplotlib.pyplot as plt
from SerialConnection import select_port
import numpy as np
import datetime

def main():
    print("Start!")

    #Serial portの選択
    ser = select_port()
    if ser is None:
        return

    #ログファイルの作成(yyyymmddHHMMSS_Log.csv yyyy:年 mm:月 dd:日 HH:時 MM:分 SS:秒)
    dt_now = datetime.datetime.now()#現在時刻の取得
    path='data/'+dt_now.strftime('%Y%m%d%H%M%S_Log.csv')#ファイルのPath
    f = open(path, 'w')#ファイル作成

    plt.figure()
    #x軸の幅を100にする
    xlim = [0, 10]
    X, Y = [], []
    X2, Y2 = [], []
    while True:
        try:
            ser.reset_input_buffer()#受信バッファをクリア
            ser.write(b'F')#シリアル送信
            readdata=str(ser.readline().decode())#受信データをデコードして文字列に変換
            data=readdata.replace('\r\n','')#'\r\n'を''に置き換え
            sensordata=data.split(',')#カンマで分割

            #受信データ変換
            try:
                m=float(sensordata[0])
            except:
                m=0

            try:
                temp=float(sensordata[1])
            except:
                temp=0

            if isinstance(m, float) and isinstance(temp, float):#変数m temp両方ともfloat型のとき(うまく受信できたとき)
                print(readdata)

                #データの保存
                with open(path, 'a') as f:
                    dt_now = datetime.datetime.now()#現在時刻の取得
                    f.write(dt_now.strftime('%Y/%m/%d(%H:%M:%S),')+str(m)+","+str(temp)+",\n")#ログの書き込み

                #画面をクリア
                plt.cla()
                plt.grid()

                Y.append(m)
                X.append(len(Y))
                #xに100個以上格納されたら
                if len(X) > 10:
                    xlim[0] += 1
                    xlim[1] += 1

                Y2.append(temp)
                X2.append(len(Y2))

                plt.plot(X, Y,color = 'blue')
                plt.plot(X2, Y2,color = 'red')
                plt.axvspan(xlim[0],xlim[1], color="gray", alpha=0.3)
                #x軸、y軸方向の表示範囲を設定
                plt.ylim(-1, 2)
                plt.xlim(xlim[0], xlim[1])
                #描写
                plt.pause(0.01)

        except KeyboardInterrupt:
            print("End")
            ser.close()
            break


if __name__ == "__main__":
    main()