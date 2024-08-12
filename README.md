# twDaitaiMerge
PythonでTailwind CSSをCDN等で使用する際にクラス名をだいたいマージするためのライブラリ

## インストール
```
git clone https://github.com/nOjms-Blue/twDaitaiMerge.git
cd twDaitaiMerge
pip install .
```

## 使い方
```
from twDaitaiMerge import twMerge

original = "h-10 w-12 m-2 bg-white hover:bg-gray-100"
merge = "h-12 w-16 mx-0 bg-blue-500 hover:bg-blue-400"
print(twMerge(original, merge))
```
出力
```
bg-blue-500 mx-0 w-16 h-12 my-2 hover:bg-blue-400
```