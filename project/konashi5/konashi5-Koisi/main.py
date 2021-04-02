from Konashi import *
from line_notify_bot import LINENotifyBot
import random


if __name__ == "__main__":
    async def main():
        global button
        global Temp
        global Hum
        global Press
        global Accel
        global Gyro
        global Presence
        global mode
        global LED
        global packageID
        global stickerID
        global comment
        Presence={}
        Presence[0]=Presence[1]=False

        def pressuretom(P):
            #P0=1022.72
            P0=1013.15
            return ((pow((P0/P),(1/5.257))-1)*(Temp+273.15))/0.0065

        def WBGT(T,H):
            return 0.725*T+0.0368*H+0.00364*T*H-3.246

        def map(x,in_min,in_max,out_min,out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        def Room_condition(Temp,Hum,Press):
            global comment
            global h
            global wbgt
            global mode
            global LED
            global packageID
            global stickerID

            comment=""
            h=pressuretom(Press)
            wbgt=WBGT(Temp,Hum)
            if wbgt>31:#危険
                mode=8
                LED=15
                comment="危険 熱中症に注意！外出はなるべく避けよう"
                packageID=1
                stickerID=21
            elif wbgt>28:#厳重警戒
                mode=7
                LED=14
                comment="厳重警戒 熱中症に注意！炎天下はなるべく避けよう"
                packageID=1
                stickerID=422
            elif wbgt>25:#警戒
                mode=6
                LED=12
                comment="警戒　運動や激しい作業をする際はこまめに休憩しよう"
                packageID=2
                stickerID=27
            elif wbgt>21:#注意
                mode=5
                LED=8
                comment="注意　激しい運動や重労働時は熱中症に気をつけよう"
                packageID=2
                stickerID=31
            elif Temp<14:#寒い
                mode=4
                LED=0
                comment="寒イ.."
                packageID=2
                stickerID=29
            elif Hum>60:#湿度高め
                mode=3
                LED=0
                comment="湿度が高め\n雨降ってる？\n最適湿度は40~60％だよ"
                sticker=[9,507]
                rnum=random.randint(0,1)
                if rnum>0:
                    packageID=2
                else:
                    packageID=1
                stickerID=sticker[rnum]
            elif Hum<30:#乾燥してる
                mode=2
                LED=0
                comment="乾燥してるよ\n加湿器つけよう！\n最適湿度は40~60％だよ"
                packageID=2
                stickerID=24
            elif Hum<40:#少し乾燥してる
                mode=1
                LED=0
                comment="少し乾燥してるよ\n加湿器つけたほうがいいかも\n最適湿度は40~60％だよ"
                packageID=1
                stickerID=15
            else:#ほぼ安全
                mode=0
                LED=0
                comment="快適～♪"
                sticker=[2,5,13,103,26,140,141,142,501,513]
                rnum=random.randint(0,9)
                if rnum>3:
                    packageID=2
                else:
                    packageID=1
                stickerID=sticker[rnum]

        bot = LINENotifyBot(access_token='UilHhgEr7klUFPxhWyHdxYrJDbomRgXxLWeeNJsFyqY')

        k = Konashi(name="ksAB1A08")
        k2 = Konashi(name="ksAB0FF0")

        await k.connect(5)
        await k2.connect(5)

        print("Connected")

        bot.send(
            message="Start up!",
            sticker_package_id=1,
            sticker_id=12,
            )

        await asyncio.sleep(0.5)
        def pin_change_cb(pin, val):
            global button
            if pin==0 and val==1:
                button=1
            elif pin==0 and val==0:
                button=0
            print("Pin {}: {}".format(pin, val))

        def temperature_cb(temp):
            global Temp
            Temp=temp

        def humidity_cb(hum):
            global Hum
            Hum=hum

        def pressure_cb(press):
            global Press
            Press=press

        def presence_cb(pres):#人感センサー1
            global Presence
            Presence[0]=pres
            print("Presence1:", pres)

        def presence_cb2(pres):#人感センサー2
            global Presence
            Presence[1]=pres
            print("Presence2:", pres)

        def accelgyro_cb(accel, gyro):
            global Accel
            global Gyro
            Accel=accel
            Gyro=gyro

        k.gpioSetInputCallback(pin_change_cb)
        await k.gpioConfigSet([(0x01,True,KonashiGpioPinConfig(KONASHI_GPIO_DIRECTION_IN,send_on_change=True)), (0x1E,True,KonashiGpioPinConfig(KONASHI_GPIO_DIRECTION_OUT,send_on_change=False))])
        await k.builtinSetTemperatureCallback(temperature_cb)
        await k.builtinSetHumidityCallback(humidity_cb)
        await k.builtinSetPressureCallback(pressure_cb)
        await k.builtinSetPresenceCallback(presence_cb)
        await k.builtinSetAccelGyroCallback(accelgyro_cb)
        await asyncio.sleep(1)

        k2.gpioSetInputCallback(pin_change_cb)
        await k2.gpioConfigSet([(0x01,True,KonashiGpioPinConfig(KONASHI_GPIO_DIRECTION_IN,send_on_change=True)), (0x1E,True,KonashiGpioPinConfig(KONASHI_GPIO_DIRECTION_OUT,send_on_change=False))])
        await k2.builtinSetPresenceCallback(presence_cb2)
        await asyncio.sleep(1)

        i=0
        LED=0
        button=0
        stickerID=5
        packageID=1
        SendFlag=False
        Buttoncount=0
        ButtonFlag=False
        Home=True
        Alert=False
        prei=i
        R=255
        G=255
        B=255
        mode=0
        oldmode=-1
        while(True):

            if (Presence[0] or Presence[1]) and button==False:
                if Home:
                    R=int(map(Temp,0,45,0,255))
                    B=int(map(Hum,0,100,0,255))
                    G=int(map(Press,870,1400,0,255))#観測記録　min 870 max 1093.0[hPa]
                    if R>255:
                        R=255
                    if B>255:
                        B=255
                    if G>255:
                        G=255
                    print(R,G,B,Temp,Hum,Press)
                    t={}
                    if Presence[0]:
                        t[0]=500
                        t[1]=1500
                    elif Presence[1]:
                        t[0]=1500
                        t[1]=500
                    else:
                        t[0]=1000
                        t[1]=1000
                    await k.builtinSetRgb(R,G,B, 255, t[0])
                    await k2.builtinSetRgb(R,G,B, 255, t[1])
                else:
                    if Presence[0]:
                        comment="デバイス1に反応あり!!\n"
                    elif Presence[1]:
                        comment="デバイス2に反応あり!!\n"
                    else:
                        comment="両方のデバイスに反応あり!!!"
                    if SendFlag ==False:
                        bot.send(
                            message="\n[Warning!]\n家に誰かいる!!\n"+comment,
                            sticker_package_id=1,
                            sticker_id=3,
                            )
                        SendFlag=True
                        prei=i
                    Alert=True
            else:
                if Alert==False:
                    await k.builtinSetRgb(0,0,0, 255, 1000)
                    await k2.builtinSetRgb(0,0,0, 255, 500)
                SendFlag=False

            if i%3==1 or oldmode==-1:
                Room_condition(Temp,Hum,Press)
                await k.gpioControl([(~(LED<<1),KONASHI_GPIO_LEVEL_LOW), (LED<<1,KONASHI_GPIO_LEVEL_HIGH)])
                await k2.gpioControl([(~(LED<<1),KONASHI_GPIO_LEVEL_LOW), (LED<<1,KONASHI_GPIO_LEVEL_HIGH)])
                if Alert:
                    await k.builtinSetRgb(255,0,0, 255, 1)
                    await k2.builtinSetRgb(255,0,0, 255, 1)
            else:
                if Alert:
                    await k.builtinSetRgb(0,0,0, 255, 1)
                    await k2.builtinSetRgb(0,0,0, 255, 1)
                    if (i-prei)>8:
                        Alert=False

            if  oldmode != mode:
                oldmode=mode
                bot.send(
                    message="\n"+comment+"\n気温 "+str(Temp)+"[℃]\n湿度 "+str(Hum)+"[%]\n気圧 "+str(round(Press,1))+"[hPa]\nWBGT "+str(round(wbgt,2))+"[℃]\n標高 約"+str(round(h,1))+"[m]",
                    sticker_package_id=packageID,
                    sticker_id=stickerID,
                    )

            i+=1
            if button:
                ButtonFlag=True
                Buttoncount+=1
                if Buttoncount > 3:
                    break
            else:
                if ButtonFlag:
                    Home=not Home
                    print("Home:",Home)
                    if Home == False:
                        bot.send(
                            message="セキュリティーモード起動!\nいってらっしゃ～い",
                            sticker_package_id=1,
                            sticker_id=408,
                            )
                    else:
                        bot.send(
                            message="セキュリティーモード終了!\nおかえりなさい",
                            sticker_package_id=2,
                            sticker_id=143,
                            )
                        oldmode=-1
                    Alert=False
                    ButtonFlag=False
                    Buttoncount=0
            await asyncio.sleep(1)

        await k.gpioControl([(0x1E,KONASHI_GPIO_LEVEL_LOW)])
        await k2.gpioControl([(0x1E,KONASHI_GPIO_LEVEL_LOW)])

        await k.gpioControl([(0x1E,KONASHI_GPIO_LEVEL_HIGH)])
        await k2.gpioControl([(0x1E,KONASHI_GPIO_LEVEL_HIGH)])

        await asyncio.sleep(2)
        await k.gpioControl([(0x1E,KONASHI_GPIO_LEVEL_LOW)])
        await k2.gpioControl([(0x1E,KONASHI_GPIO_LEVEL_LOW)])

        await k.builtinSetRgb(0,0,0, 255, 1000)
        await k2.builtinSetRgb(0,0,0, 255, 1000)

        await k.disconnect()
        await k2.disconnect()

        print("Disconnected")
        bot.send(
            message="Shutdown!",
            sticker_package_id=1,
            sticker_id=1,
            )

        await asyncio.sleep(2)

    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
