import speech_recognition as sr
import MeCab

#Natural language processing
r = sr.Recognizer()
mic = sr.Microphone()
mecab = MeCab.Tagger()

while True:
    print("Say something ...")

    with mic as source:
        r.adjust_for_ambient_noise(source) #雑音対策
        audio = r.listen(source)

    print ("Now to recognize it...")

    try:
        sentence = r.recognize_google(audio, language='ja-JP')
        print(sentence)#音声認識の結果表示
        print(mecab.parse(sentence))#形態素解析の結果表示
        str_output = mecab.parse(sentence)#str型で、単語が空白で別れる
        wordlist = str_output.split(' ')
        print(list)

        # "ストップ" と言ったら音声認識を止める
        if sentence.find('ストップ') != -1 :
            print("end")
            break

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))