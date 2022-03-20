from decimal import Decimal
cipher1 = "119 508 49 661 1263 407 1262 407 511 49 17 52 17"
cipher2 = "1432 394 1061 1006 1379 1273 158 1273 1143 1061 1377 1536 1377"

listC1 = cipher1.split(" ")
listC2 = cipher2.split(" ")
block1 = 119
block2 = 1432


def inverseMod(a, m):
    for i in range(1, m):
        if (m * i + 1) % a == 0:
            return (m * i + 1) // a
    return None

def xgcd(e1, e2):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while e2 != 0:
        q, e1, e2 = e1 // e2, e2, e1 % e2
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return e1, x0, y0


n = 1643
g, a, b = xgcd(11, 13)
b = b


# pow(block1,a,n)*pow(block2,b,n))%n
def decipher(b1, b2):
    inv = inverseMod(b2, n)
    print(chr(pow(b1, a) * (pow(inv, -b)) % n), end='')


for item1, item2 in zip(listC1, listC2):
    decipher(int(item1), int(item2))
