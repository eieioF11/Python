import speech_recognition as sr
import MeCab
import requests
import json

#weather

def getweather(city_name):
    app_id = "31abb09e5d4b51e798fa7dc2ea43a6aa"
    #&units=metricで摂氏温度を求める
    URL = "https://api.openweathermap.org/data/2.5/weather?q={0},jp&units=metric&lang=ja&appid={1}".format(city_name, app_id)

    response = requests.get(URL)
    data =  response.json()

    #天気情報
    weather = data["weather"][0]["description"]
    #最高気温
    temp_max = data["main"]["temp_max"]
    #最低気温
    temp_min = data["main"]["temp_min"]
    #寒暖差
    diff_temp = temp_max - temp_min
    #湿度
    humidity = data["main"]["humidity"]
    #都市名
    city = data["name"]

    context = {"最高気温":str(temp_max) + "度", "最低気温": str(temp_min) + "度", "寒暖差": str(diff_temp) + "度", "湿度": str(humidity) + "%"}
    print("今日の{0}の天気は{1}".format(city,weather))
    for k, v in context.items():
        print("{0}は{1}".format(k, v))
    print("です。")

#Natural language processing
r = sr.Recognizer()
mic = sr.Microphone()
mecab = MeCab.Tagger()
#mecab = MeCab.Tagger("-Owakati")
#mecab = MeCab.Tagger("-Ochasen")

# MeCab による単語への分割関数 (名詞のみ残す)
def split_text_only_noun(text):
    tagger = MeCab.Tagger()

    words = []
    for c in tagger.parse(text).splitlines()[:-1]:
        surface, feature = c.split('\t')
        pos = feature.split(',')[0]
        if pos == '名詞':
            words.append(surface)
    return ' '.join(words)

while True:
    print("Say something ...")

    with mic as source:
        r.adjust_for_ambient_noise(source) #雑音対策
        audio = r.listen(source)

    print ("Now to recognize it...")

    try:
        sentence = r.recognize_google(audio, language='ja-JP')
        print(sentence)#音声認識の結果表示

        output = mecab.parse(sentence)#形態素解析

        words = output.splitlines()#文字列を改行で分割する
        #print(output)#形態素解析の結果表示

        split_text = split_text_only_noun(sentence)
        #print("split_text")
        #print(split_text)

        splitlist = split_text.split()
        if split_text.count("天気")>=1:
            City="Tokyo"
            for w in splitlist:
                #print(w)
                if w=="東京":
                    City="Tokyo"
                elif w=="大阪":
                    City="osaka"
                elif w=="名古屋":
                    City="nagoya"
                elif w=="北海道":
                    City="hokkaido"
                elif w=="京都":
                    City="京都"
                elif w=="広島":
                    City="hirosima"
                elif w=="埼玉":
                    City="saitama"
            getweather(City)

        # "ストップ" と言ったら音声認識を止める
        if sentence.find('ストップ') != -1 :
            print("End")
            break

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))