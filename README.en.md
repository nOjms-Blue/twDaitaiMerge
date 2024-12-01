# twDaitaiMerge
A Python library for roughly merging Tailwind CSS class names.
<br />
[ [English](README.en.md) | [日本語](README.md) ]


## Install
```
git clone https://github.com/nOjms-Blue/twDaitaiMerge.git
cd twDaitaiMerge
pip install .
```


## How to use
```
from twDaitaiMerge import twMerge

original = "h-10 w-12 m-2 bg-white hover:bg-gray-100"
merge = "h-12 w-16 mx-0 bg-blue-500 hover:bg-blue-400"
print(twMerge(original, merge))
```
Output
```
bg-blue-500 mx-0 w-16 h-12 my-2 hover:bg-blue-400
```