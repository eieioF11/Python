import speech_recognition as sr
import MeCab

#Natural language processing
r = sr.Recognizer()
mic = sr.Microphone()
 t = MeCab.Tagger()

while True:
    print("Say something ...")

    with mic as source:
        r.adjust_for_ambient_noise(source) #雑音対策
        audio = r.listen(source)

    print ("Now to recognize it...")

    try:
        print(r.recognize_google(audio, language='ja-JP'))
       
        sentence = "太郎はこの本を女性に渡した。"
        print(t.parse(sentence))
        # "ストップ" と言ったら音声認識を止める
        if r.recognize_google(audio, language='ja-JP') == "ストップ" :
            print("end")
            break

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))