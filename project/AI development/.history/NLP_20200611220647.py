import speech_recognition as sr
import MeCab

#Natural language processing
r = sr.Recognizer()
mic = sr.Microphone()
mecab = MeCab.Tagger()
#mecab = MeCab.Tagger("-Owakati")
#mecab = MeCab.Tagger("-Ochasen")

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
        print(output)#形態素解析の結果表示
        wordlist = []
        #単語リスト作成
        for i in :
            if i=='EOF':continue
            tmp= i.split()[0]
            wordlist.append(tmp)

        print("Word list")
        print(wordlist)

        # "ストップ" と言ったら音声認識を止める
        if sentence.find('ストップ') != -1 :
            print("end")
            break

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))