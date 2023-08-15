import random
import argparse
from time import time


def get_parser():
    parser = argparse.ArgumentParser(usage='python3 Proxifier_Keygen.py [-v setup]',
        description='Proxifier_Keygen: 基于python3的Proxifier注册机, 默认key为setup版本',
                                     )
    p = parser.add_argument_group('Proxifier_Keygen的参数')
    p.add_argument("-v", "--version", type=str, help="Proxifier的版本:setup/portable/mac")
    # p.add_argument("-c", "--custom", type=str, help="自定义Key的第四组字符")
    # p.add_argument("-t", "--table", type=str, help="自定义Key的生成字符表")
    args = parser.parse_args()
    return args


def handle(s):
    res = 0
    for i in range(len(s) - 1, -1, -1):
        res <<= 5
        t = ord(s[i])
        if s[i] == 'W':
            continue
        elif s[i] == 'X':
            res += 24
        elif s[i] == 'Y':
            res += 1
        elif s[i] == 'Z':
            res += 18
        elif s[i] in "0123456789":
            res += t - 48
        else:
            res += t - 55
    return res


def handle_re(s, len):
    res = ''
    for i in range(len):
        t = s % (2 ** 5)
        s //= 32
        if t == 0:
            res += 'W'
        elif t == 24:
            res += 'X'
        elif t == 1:
            res += 'Y'
        elif t == 18:
            res += 'Z'
        elif t <= 9:
            res += chr(t + 48)
        else:
            res += chr(t + 55)
    return res


def CRC32_like(n):
    res = 0
    for i in range(12):
        v2 = ((n >> (8 * i)) & 0xff) << 24
        if i:
            res ^= v2
        else:
            res = (~v2) & 0xffffffff
        for j in range(8):
            res *= 2
            if res >= 0xffffffff:
                res &= 0xffffffff
                res ^= 0x4C11DB7
    return res


def keygen(args):
    if not args.version or args.version == 'setup':  # --version
        product = 0
    elif args.version == 'portable':
        product = 1
    elif args.version == 'mac':
        product = 2
    else:
        print("版本参数错误!")
        exit(-1)
    # if args.custom:               # --custom
    #     key_4th = args.custom
    # if args.table:                # --custom
    #     character_table = args.table

    character_table = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXZY'
    random.seed(time())
    key_4th = ''
    for i in range(5):
        key_4th += character_table[random.randint(0, len(character_table) - 1)]

    # 小于0x2580是过期的key, 高两字节是产品版本, 为0则是安装版, 1是便携版, 2是Mac版
    low_4B = random.randint(0x2580, 0xFFFF) + (product << 21)
    # 高两字节是证书有效期, 为零直接无限期
    mid_4B = random.randint(0, 0xFFFF)
    high_4B = handle(key_4th)
    res = CRC32_like((high_4B << 64) + (mid_4B << 32) + low_4B)
    v17 = res & 0x1FFFFFF
    v18 = v17 ^ (v17 << 7)
    key_5th = handle_re(v17, 5)
    key_0_7_ch = handle_re(low_4B ^ 0x12345678 ^ v18, 7)
    key_7_14_ch = handle_re(mid_4B ^ 0x87654321 ^ v18, 7)

    key = ''
    # 第三位不影响 key, 但是不能为'Y', 否则版本对不上
    key += key_0_7_ch[:2] + character_table[random.randint(0, 34)] + key_0_7_ch[3:5]
    key += '-'
    key += key_0_7_ch[5:7] + key_7_14_ch[:3]
    key += '-'
    key += key_7_14_ch[3:7] + key_0_7_ch[2]
    key += '-'
    key += key_4th
    key += '-'
    key += key_5th
    return key


if __name__ == '__main__':
    args = get_parser()
    print(keygen(args))
