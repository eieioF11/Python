import MeCab
t = MeCab.Tagger()
sentence = "太郎はこの本を女性に渡した。"
print(t.parse(sentence))