# coding: utf-8

from base64 import b64encode, b64decode
from enum import Enum 
import re
import sys

class EncodeType(Enum):
    RAW = 0
    THUNDER = 1
    FLASHGET = 2
    QQDOWNLOAD = 3

def encode(s, t):
    if t is EncodeType.RAW:
        return s
    encoded = padding(s, t)
    encoded = utf8encoded(encoded)
    encoded = b64encode(encoded)
    if t is EncodeType.THUNDER:
        encoded = utf8encoded("thunder://") + encoded
    if t is EncodeType.FLASHGET:
        encoded = utf8encoded("flashget://") + encoded + utf8encoded("&forece")
    if t is EncodeType.QQDOWNLOAD:
        encoded = utf8encoded("qqdl://") + encoded
    return utf8decoded(encoded)

def decode(s, t):
    if t is EncodeType.RAW:
        return s
    decoded = subscript(s)
    decoded = utf8encoded(decoded)
    decoded = b64decode(decoded)
    decoded = utf8decoded(decoded)
    decoded = trimming(decoded, t)
    return decoded

def transcode(s, t):
    raw_url = decode(s, t)
    thd_url = encode(raw_url, EncodeType.THUNDER)
    flg_url = encode(raw_url, EncodeType.FLASHGET)
    qqd_url = encode(raw_url, EncodeType.QQDOWNLOAD)

    print("原始: {}".format(raw_url))
    print("迅雷: {}".format(thd_url))
    print("快车: {}".format(flg_url))
    print("旋风: {}".format(qqd_url))
    print(" " * 60)

def guesscode(s):
    if s.startswith('thunder://'):
        return EncodeType.THUNDER
    if s.startswith('flashget://'):
        return EncodeType.FLASHGET
    if s.startswith('qqdl://'):
        return EncodeType.QQDOWNLOAD
    return EncodeType.RAW

def utf8encoded(s):
    return s.encode('utf-8')

def utf8decoded(b):
    return b.decode('utf-8')

def padding(s, t):
    dest = s
    if t is EncodeType.THUNDER:
        dest = "AA" + dest + "ZZ"
    if t is EncodeType.FLASHGET:
        dest = "[FLASHGET]" + dest + "[FLASHGET]"
    return dest

def trimming(s, t):
    dest = s
    if (dest[:2] == "AA") and (dest[-2:] == "ZZ"):
        dest = dest[2:-2]
    if (dest[:10] == "[FLASHGET]") and (dest[-10:] == "[FLASHGET]"):
        dest = dest[10:-10]
    return dest

def subscript(s):
    return re.split(r"//|&", s)[1]

if __name__ == '__main__':
    args = sys.argv[1:]
    for arg in args:
        code = guesscode(arg)
        transcode(arg, code)
