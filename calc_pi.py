
from constants import *
from basic import *
from advanced import *
from formatting import *
import sys
from calc import calc

# calculate Pi using the Gregory-Leibniz series
# (4/1)-(4/3)+(4/5)-(4/7)+(4/9)-(4/11)+(4/13)-(4/15)
# Stabilze the 3.141592 (6 first digits after fp) around 2 900 000 iterations
def calculatePiStepByStep(digitByDigit: bool = True, limit: int = 32):
    d = 1
    buffer = div("4", str(d), False, limit)
    sign = True
    LDSC = 40
    lastDigitStableCycle = LDSC
    pt = 0
    while True:
        lastDigit = buffer[pt]
        d += 2
        if sign:
            buffer = sub(buffer, div("4", str(d), False, limit))
            sign = False
        else:
            buffer = add(buffer, div("4", str(d), False, limit))
            sign = True

        if digitByDigit:
            if lastDigitStableCycle < 0:
                print(lastDigit, end="")
                sys.stdout.flush()
                pt += 1
                lastDigitStableCycle = LDSC
            elif lastDigit == buffer[pt]:
                lastDigitStableCycle -= 1
        else:
            print(buffer, ((d + 1) / 2), end='\r')

# calculatePiStepByStep(False)

# version using native python3 number types
def calculatePiStepByStep_orig(digitByDigit: bool = True):
    d = 1
    buffer = 4 / d
    sign = True
    LDSC = 40
    lastDigitStableCycle = LDSC
    pt = 0
    while True:
        lastDigit = str(buffer)[pt]

        d += 2
        if sign:
            buffer -= 4 / d
            sign = False
        else:
            buffer += 4 / d
            sign = True

        if digitByDigit:
            if lastDigitStableCycle < 0:
                print(lastDigit, end="")
                sys.stdout.flush()
                pt += 1
                lastDigitStableCycle = LDSC
            elif lastDigit == buffer[pt]:
                lastDigitStableCycle -= 1
        else:
            print(buffer, ((d + 1) / 2), end='\r')

# Nilakantha series
def calculatePiNilakantha(digitByDigit: bool = True, limit: int = 32):
    # 3+4/(2·3·4)-4/(4·5·6)+4/(6·7·8)-4/(8·9·10)+4/(10·11·12)-4/(12·13·14)
    buffer = add("3", div("4", mul(mul("2", "3", False), "4", False), False, limit))
    sign = True
    lastDigit = ""
    LDSC = 40
    lastDigitStableCycle = LDSC
    d = 4
    pt = 0
    while True:

        lastDigit = buffer[pt]
        if sign:
            # buffer = sub(buffer, div("4", str(d * (d + 1) * (d + 2)), False, limit))
            buffer = sub(buffer, div("4", mul(mul(str(d), str(d + 1), False), str(d + 2), False), False, limit))
            sign = False
        else:
            # buffer = add(buffer, div("4", str(d * (d + 1) * (d + 2)), False, limit))
            buffer = add(buffer, div("4", mul(mul(str(d), str(d + 1), False), str(d + 2), False), False, limit))
            sign = True
        d += 2

        if digitByDigit:
            if lastDigitStableCycle < 0:
                print(lastDigit, end="")
                sys.stdout.flush()
                pt += 1
                lastDigitStableCycle = LDSC
            elif lastDigit == buffer[pt]:
                lastDigitStableCycle -= 1
        else:
            print(buffer, ((d + 1) / 2), end='\r')

# calculatePiNilakantha(False)

# version using native python3 number types
def calculatePiNilakantha_orig(digitByDigit: bool = True):
    # 3+4/(2·3·4)-4/(4·5·6)+4/(6·7·8)-4/(8·9·10)+4/(10·11·12)-4/(12·13·14)
    limit = 99
    buffer = 3 + 4 / (2 * 3 * 4)
    sign = True
    lastDigit = ""
    LDSC = 40
    lastDigitStableCycle = LDSC
    d = 4
    pt = 0
    tlen = len(str(buffer))
    while pt < tlen - 1:

        lastDigit = str(buffer)[pt]
        if sign:
            buffer -= 4 / (d * (d + 1) * (d + 2))
            sign = False
        else:
            buffer += 4 / (d * (d + 1) * (d + 2))
            sign = True
        d += 2

        if digitByDigit:
            if lastDigitStableCycle < 0:
                print(lastDigit, end="")
                sys.stdout.flush()
                pt += 1
                lastDigitStableCycle = LDSC
            elif lastDigit == str(buffer)[pt]:
                lastDigitStableCycle -= 1
        else:
            print(buffer, ((d + 1) / 2), end='\r')

# Version pure python3
def chudnovsky_orig(n):
    import decimal
    """Chudnovsky algorithm."""
    def binary_split(a, b):
        if b == a + 1:
            Pab = -(6*a - 5)*(2*a - 1)*(6*a - 1)
            Qab = 10939058860032000 * a**3
            Rab = Pab * (545140134*a + 13591409)
            # print("If: {a} and {b}".format(a=a,b=b), "Pab", Pab, "Qab", Qab, "Rab", Rab)
        else:
            m = (a + b) // 2
            Pam, Qam, Ram = binary_split(a, m)
            Pmb, Qmb, Rmb = binary_split(m, b)
            
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Rab = Qmb * Ram + Pam * Rmb
            # print("Else: {a} and {b}".format(a=a,b=b), "m", m, "Pab", Pab, "Qab", Qab, "Rab", Rab)
        return Pab, Qab, Rab

    P1n, Q1n, R1n = binary_split(1, n)
    return (426880 * decimal.Decimal(10005).sqrt() * Q1n) / (13591409*Q1n + R1n)

# chudnovsky algorithm to try when asqrt() is done
# cf. https://en.wikipedia.org/wiki/Chudnovsky_algorithm#Python_code
def achudnovsky(n: str, limit: int = 64) -> str:
    """Chudnovsky algorithm."""
    def binary_split(a, b):
        if b == add(a, "1"):
            Pab = calc("-(6*{a} - 5)*(2*{a} - 1)*(6*{a} - 1)".format(a=a))
            Qab = mul("10939058860032000", apow(a, "3"), False)
            Rab = mul(Pab, add(mul("545140134", a, False), "13591409"), False)
            # print("If: {a} and {b}".format(a=a,b=b), "Pab", Pab, "Qab", Qab, "Rab", Rab)
        else:
            # (a + b) // 2
            m = div(add(a, b), "2", False, 0)
            Pam, Qam, Ram = binary_split(a, m)
            Pmb, Qmb, Rmb = binary_split(m, b)
            
            Pab = mul(Pam, Pmb, False)
            Qab = mul(Qam, Qmb, False)
            Rab = add(mul(Qmb, Ram, False), mul(Pam, Rmb, False))
            # print("Else: {a} and {b}".format(a=a,b=b), "m", m, "Pab", Pab, "Qab", Qab, "Rab", Rab)
        return Pab, Qab, Rab

    if isASupThanB(n, "2") == "B":
        print("Error: Chudnovsky algorithm needs 2 as minimum value to compute pi")
        return "-1"

    P1n, Q1n, R1n = binary_split("1", n)
    # reference value for decimal.Decimal(10005).sqrt() => "100.0249968757810059447921879"
    return div(mul(mul("426880", asqrt("10005", limit), False), Q1n, False), add(mul("13591409", Q1n, False), R1n), False, limit)

# for i in range(2, 32):
#   print(i, ":", achudnovsky(str(i), 200))
# print(achudnovsky("15", 212))

# decimal.getcontext().prec = 100 # number of digits of decimal precision
# print(chudnovsky_orig(8))



