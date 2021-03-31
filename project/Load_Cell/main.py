#グラフ上で右クリックすると終了
#Serialのボーレートは9600　PCから何らかの値を送信するとArduinoからデータが送られてくる
#Arduinoから送られてくるデータ形式は　重量の値,温度の値,湿度の値,気圧の値\n\r の少数値(小数点以下3桁)の文字列　Ex. 1.601,25.023,30.124,1020.001\n\r
#ログファイルはmain.pyと同じディレクトリにあるdataに保存される　ファイル名の形式は　yyyymmddHHMMSS_Log.csv yyyy:年 mm:月 dd:日 HH:時 MM:分 SS:秒
import matplotlib.pyplot as plt
from SerialConnection import select_port
import numpy as np
import datetime

global end

def onclick(event):
    global end
    end=False
    if event.button==3:#グラフを右クリックしたとき
        end=True

def main():#メイン関数
    global end
    end=False
    print("Start!")
    #Serial portの選択
    ser = select_port()
    if ser is None:
        return#シリアルポートがないときプログラム終了
    #ログファイルの作成(yyyymmddHHMMSS_Log.csv yyyy:年 mm:月 dd:日 HH:時 MM:分 SS:秒)
    dt_now = datetime.datetime.now()#現在時刻の取得
    path='data/'+dt_now.strftime('%Y%m%d%H%M%S_Log.csv')#ファイルのPath
    with open(path, 'a') as f:
        f.write("時刻,"+"重量[kg],"+"気温[℃],"+"湿度[%],"+"気圧[hPa],\n")#ログの書き込み
    #グラフの設定
    fig = plt.figure(figsize=(8.0, 7.5))#figsize = ウィンドウサイズ
    #x軸の幅を100にする
    xlim = [0, 10]
    prexlim=0
    #データを格納する配列
    X, Y = [], []
    X2, Y2 = [], []
    X3, Y3 = [], []
    X4, Y4 = [], []
    #グラフをクリックしたときの位置とボタンの種類を取得する設定
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    while True:
        if end==True:     # グラフ上で右クリックしたとき終了
            break
        try:
            ser.reset_input_buffer()#受信バッファをクリア
            ser.write(b'F')#シリアル送信
            readdata=str(ser.readline().decode())#受信データをデコードして文字列に変換
            data=readdata.replace('\r\n','')#'\r\n'を''に置き換え
            sensordata=data.split(',')#カンマで分割

            #受信データ変換
            try:#重量[kg]
                m=float(sensordata[0])
            except:
                m=0

            try:#気温[℃]
                temp=float(sensordata[1])
            except:
                temp=0

            try:#湿度[%]
                hum=float(sensordata[2])
            except:
                hum=0

            try:#気圧[hPa]
                press=float(sensordata[3])
            except:
                press=0

            if isinstance(m, float) and isinstance(temp, float):#変数m temp両方ともfloat型のとき(うまく受信できたとき)
                print(readdata)

                #データの保存
                with open(path, 'a') as f:
                    dt_now = datetime.datetime.now()#現在時刻の取得
                    f.write(dt_now.strftime('%Y/%m/%d(%H:%M:%S),')+str(m)+","+str(temp)+","+str(hum)+","+str(press)+",\n")#ログの書き込み

                #画面をクリア
                plt.cla()
                plt.clf()
                #グラフの作成（4つ）
                ax1 = fig.add_subplot(2, 2, 1)
                ax2 = fig.add_subplot(2, 2, 2)
                ax3 = fig.add_subplot(2, 2, 3)
                ax4 = fig.add_subplot(2, 2, 4)
                #グリッドを表示する
                ax1.grid(True)
                ax2.grid(True)
                ax3.grid(True)
                ax4.grid(True)
                #データの書き込み
                Y.append(m)#kg
                #Y.append(m*1000)#g
                X.append(len(Y))
                #xに100個以上格納されたら
                if len(X) > 10:
                    xlim[0] += 1
                    xlim[1] += 1

                Y2.append(temp)
                X2.append(len(Y2))

                Y3.append(hum,)
                X3.append(len(Y3))

                Y4.append(press)
                X4.append(len(Y4))
                #グラフのにデータをプロット　線の色指定
                ax1.plot(X, Y,color = 'magenta')#重量
                ax2.plot(X2, Y2,color = 'red')#気温
                ax3.plot(X3, Y3,color = 'blue')#湿度
                ax4.plot(X4, Y4,color = 'green')#気圧
                #x軸、y軸方向の表示範囲を設定
                ax2.set_ylim(0,50)#気温の表示範囲0℃から50℃
                ax3.set_ylim(0,100)#湿度の表示範囲0%から100%
                ax4.set_ylim(800,1100)#気圧の表示範囲800hPaから1100hPa
                ax1.set_xlim(xlim[0], xlim[1])
                ax2.set_xlim(xlim[0], xlim[1])
                ax3.set_xlim(xlim[0], xlim[1])
                ax4.set_xlim(xlim[0], xlim[1])
                #plt.xlim(xlim[0], xlim[1])
                #テキスト表示
                ax1_pos = ax1.get_position()#重量のグラフの位置取得
                ax2_pos = ax2.get_position()#気温のグラフの位置取得
                ax3_pos = ax3.get_position()#湿度のグラフの位置取得
                ax4_pos = ax4.get_position()#気圧のグラフの位置取得
                fig.text(ax1_pos.x1 - 0.1, ax1_pos.y1 - 0.05,str(round(m,1))+"[kg]")#最新の重量の値を表示
                fig.text(ax2_pos.x1 - 0.1, ax2_pos.y1 - 0.05,str(round(temp,1))+"[deg]")#最新の気温の値を表示
                fig.text(ax3_pos.x1 - 0.1, ax3_pos.y1 - 0.05,str(round(hum,1))+"[%]")#最新の湿度の値を表示
                fig.text(ax4_pos.x1 - 0.12, ax4_pos.y1 - 0.05,str(round(press,1))+"[hPa]")#最新の気圧の値を表示
                fig.text(0.4,0.95,"Right click to finish",color="red",fontsize=15)
                #タイトル表示
                ax1.set_title('Weight[kg]')
                ax2.set_title('Temperature[deg]')
                ax3.set_title('Humidity[%]')
                ax4.set_title('Pressure[hPa]')
                #描写
                plt.pause(0.01)

        except KeyboardInterrupt:
            break
    #終了処理
    print("End")
    ser.close()#シリアルポート停止

if __name__ == "__main__":
    main()