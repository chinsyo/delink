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

def transcode(s):
    t = guesscode(s)
    raw_url = decode(s, t)
    thd_url = encode(raw_url, EncodeType.THUNDER)
    flg_url = encode(raw_url, EncodeType.FLASHGET)
    qqd_url = encode(raw_url, EncodeType.QQDOWNLOAD)
    return (raw_url, thd_url, flg_url, qqd_url)

def encode(s, t):
    if t is EncodeType.RAW:
        return s
    encoded = _padding(s, t)
    encoded = _utf8function(b64encode, encoded)
    if t is EncodeType.THUNDER:
        encoded = "thunder://" + encoded
    if t is EncodeType.FLASHGET:
        encoded = "flashget://" + encoded
    if t is EncodeType.QQDOWNLOAD:
        encoded = "qqdl://" + encoded
    return encoded

def decode(s, t):
    if t is EncodeType.RAW:
        return s
    decoded = _subscript(s)
    decoded = _utf8function(b64decode, decoded)
    decoded = _trimming(decoded, t)
    return decoded

def guesscode(s):
    if s.startswith('thunder://'):
        return EncodeType.THUNDER
    if s.startswith('flashget://'):
        return EncodeType.FLASHGET
    if s.startswith('qqdl://'):
        return EncodeType.QQDOWNLOAD
    return EncodeType.RAW

def _subscript(s):
    return re.split(r"//", s)[1]

def _utf8function(fn, s):
    assert type(s) is str
    b = s.encode('utf-8')
    b = fn(b)
    return b.decode('utf-8')

def _padding(s, t):
    dest = s
    if t is EncodeType.THUNDER:
        dest = "AA" + dest + "ZZ"
    if t is EncodeType.FLASHGET:
        dest = "[FLASHGET]" + dest + "[FLASHGET]"
    return dest

def _trimming(s, t):
    dest = s
    if (dest[:2] == "AA") and (dest[-2:] == "ZZ"):
        dest = dest[2:-2]
    if (dest[:10] == "[FLASHGET]") and (dest[-10:] == "[FLASHGET]"):
        dest = dest[10:-10]
    return dest

if __name__ == '__main__':
    args = sys.argv[1:]
    for arg in args:
        raw, thd, flg, qqd = transcode(arg)

        print("原始: {}".format(raw))
        print("迅雷: {}".format(thd))
        print("快车: {}".format(flg))
        print("旋风: {}".format(qqd))
        print("")
