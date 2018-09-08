# Logger
## Overview
ログ取り用プログラム

年ごとのディレクトリに月日ごとのファイルが作成され、書き込んだ時間ごとにログが残っていきます。

## Usage
プログラム自体は、
```
$ python Logger.py
```
で動作します。
PyInstallerなどを使って、バイナリ化しておくと便利です。

初回起動時に、どこに保存するかを決定するダイアログが出てくるので、保存したいディレクトリを選択して下さい。

Logger起動後は、テキストフィールドに内容を書き込み、<ctrl-s>で保存して下さい。

保存するディレクトリを変えたい場合は、<ctrl-r>で初回起動時と同じダイアログが出てきます。

## Requirement
Python 3.6.4

tkinter

## License
Copyright © 2018 T_Sumida Distributed under the MIT License.
