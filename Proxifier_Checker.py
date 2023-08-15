"""
本脚本为Proxifier中key的check算法，不是项目主要内容，仅供逆向学习参考
"""


def handle(s):
    res = 0
    for i in range(len(s) - 1, -1, -1):
        res *= 32
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


def CRC32_like(n):
    res = 0
    for i in range(12):
        v2 = ((n >> (8 * i)) & 0xff) << 24
        if i:
            res ^= v2
        else:
            res = (~v2) & 0xFFFFFFFF
        for j in range(8):
            res *= 2
            if res >= 0xFFFFFFFF:
                res &= 0xFFFFFFFF
                res ^= 0x4C11DB7
    return res


# 替换这里的key为想要验证的key
key = 'QSC6X-CWAAK-4D62C-OAXDD-S9GE1'
key = key.replace('-', '')
key = key[:2] + key[14] + key[3:]
# 末尾5位
v17 = handle(key[20:25])
v18 = v17 ^ (v17 << 7)
# 开头7位
v23 = handle(key[:7])
# 开头8~14位
v27 = handle(key[7:7 + 7])
low_4B = v18 ^ v23 ^ 0x12345678
mid_4B = v18 ^ v27 ^ 0x87654321
high_4B = handle(key[15:20])

print("v17       :" + hex(v17))
print("v18       :" + hex(v18))
print("low_4B    :" + hex(low_4B))
print("mid_4B    :" + hex(mid_4B))
print("high_4B   :" + hex(high_4B))
print(hex((high_4B << 64) + (mid_4B << 32) + low_4B))

res = CRC32_like((high_4B << 64) + (mid_4B << 32) + low_4B)
print(hex(res))
print(hex(res & 0x1FFFFFF))
assert v17 == (res & 0x1FFFFFF)
print("验证成功")
