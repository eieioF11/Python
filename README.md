# Python
Pythonを使用して作成したソースコードのリポジトリ
# Installation
##pythonのインストール(Windows10)
otherフォルダにあるpython-3.7.3-amd64.exeもしくはpython-3.7.3.exeを実行してインストールする
64bit版の場合はpython-3.7.3-amd64.exe
注意　インストール時にAdd Python 3.7 to PATHという項目に必ずチェックをすること
インストール後にターミナルでpythonと入力してpythonが起動すれば成功。
起動しない場合は一度PCを再起動してみる
再起動しても起動しない場合はPythonのPATHが通っていない場合があるので手動でPATHを通す

##ライブラリーのインストール

ターミナルでotherフォルダに移動して以下のコマンドを入力することでライブラリーをインストールする
以下に記述されてないものは
```bash
pip install ライブラリー名
```
でインストールする

例　MeCabライブラリーをインストールする場合
```bash
pip install MeCab
```
##OpenCVライブラリーのインストール
```bash
pip install opencv-python
```
##PyAudioのインストール

32bitのpython3.7を使用する場合
```bash
pip install PyAudio-0.2.11-cp37-cp37m-win32.whl
```
64bitのpython3.7を使用する場合
```bash
pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
```
##OpenGLのインストール

32bitのpython3.7を使用する場合

otherフォルダのOpenGL_32bitフォルダに移動して以下のコマンドを入力
```bash
pip install PyOpenGL-3.1.5-cp37-cp37m-win32.whl
pip install PyOpenGL_accelerate-3.1.5-cp37-cp37m-win32.whl
```
64bitのpython3.7を使用する場合

otherフォルダのOpenGL_64bitフォルダに移動して以下のコマンドを入力
```bash
pip install PyOpenGL-3.1.5-cp37-cp37m-win_amd64.whl
pip install PyOpenGL_accelerate-3.1.5-cp37-cp37m-win_amd64.whl
```
# Note
開発に使用したPythonのバージョンは3.7.3
# Reference site
LINE Notify
https://qiita.com/moriita/items/5b199ac6b14ceaa4f7c9
OpenGL
https://qiita.com/emuai/items/1dd61ffa1b69643a9ca3
https://shizenkarasuzon.hatenablog.com/entry/2018/12/29/095702

