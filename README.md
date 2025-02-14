# uPicross
A small in-console implementation of picross

[![PyPI - Downloads](https://img.shields.io/pypi/dm/upicross?style=flat-square)](https://pypi.org/project/upicross/)
[![PyPI](https://img.shields.io/pypi/v/upicross?style=flat-square)](https://pypi.org/project/upicross/)
[![PyPI - License](https://img.shields.io/pypi/l/upicross?style=flat-square)](https://burnsomni.net/project/upicross/?branch=master&path=LICENSE)

### Install
```bash
    pip install upicross
```

### Run
```bash
    upicross [-w <width>] [-h <height>] [-d density]
```    

|Arguments|                                       |
|---------|---------------------------------------|
|--help   |Show Help                              |
|-w \<N>  |Set width to N spaces. Default = 20    |
|-h \<N>  |Set height to N spaces. Default = 12   |
|-d \<N>  |Set density to N  (0-1). Default = 0.6 |


|Controls|           |
|--------|-----------|
|h,j,k,l |Move Cursor|
|x       |Set Cell   |
|z       |Block Cell |
|u       |Undo       |
|q       |Quit       |
