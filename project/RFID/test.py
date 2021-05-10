
import matplotlib.pyplot as plt
from SerialConnection import select_port
import numpy as np
import datetime
import re

global end

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

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
        f.write("ID,\n")#ログの書き込み
    ID=0
    readID=0
    while True:
        try:
            readdata=str(ser.readline().decode())
            print(readdata)
        except KeyboardInterrupt:#Press a key to begin scanning for tags.と表示されたらctrl + C
            ser.write(b".\n")
            break
    print("Start!!\n\r")
    datas = []
    while True:
        if end==True:     # グラフ上で右クリックしたとき終了
            break
        try:
            ser.reset_input_buffer()#受信バッファをクリア
            readdata=str(ser.readline().decode()).strip()#受信データをデコードして文字列に変換
            if hasNumbers(readdata) and any(map(str.isdigit, readdata)):
                readID=readdata
            if readID in datas:
                # IDが入ってないやつを追加
                datas.append(readID)
            else:
                pass
            cnr = 0
            for i in datas:
                print("IDs:", i)
                print("IDs", data[cnt])
                cnt += 1
            if readID!=ID:
                ID=readID
                print(ID)
                #データの保存
                with open(path, 'a') as f:
                    f.write(str(ID)+",\n")#ログの書き込み
        except KeyboardInterrupt:
            break
    #終了処理
    print("End")
    ser.close()#シリアルポート停止

if __name__ == "__main__":
    main()