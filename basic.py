
from constants import *
from formatting import *

# TODO: try to optimize by removing the nomalization/denormalization functions (is it vain?)

"""
# fast addition idea
add chunks
  123456789101112
+ 123456789101112
is like
  12345678
+ 12345678
output = res+"0"*7
then
  9101112
+ 9101112
output = add(res, output)
with a lot of zeros
"""

def add(n1: str, n2: str) -> str:
    sign = False
    if n2[0] == "-":
        if n1[0] == "-":
            n1, n2 = n1[1:], n2[1:]
            sign = True
        else:
            return sub(n1, n2[1:])
    elif n1[0] == "-":
        return sub(n2, n1[1:])
    # optimize null operations
    if n1 == "0" : return n2
    elif n2 == "0": return n1

    n1, n2, lenMax = normalizeInputs(n1, n2)

    output = ""
    carry = False
    # reverse logic for range to begin at the end of both normalized arrays
    for i in range(lenMax - 1, -1, -1):
        num = 0
        # if we find a floating point, add it then skip and keep eventual carry
        if n1[i] == ".":
            output = "."+output
            continue
        if carry:
            num += 1
            carry = False

        num += (ord(n1[i]) - ORD_0) + (ord(n2[i]) - ORD_0)
        # mark a carry if needed
        if num > 9:
            carry = True

        c = str(num)
        if len(c) > 1:
            c = c[1]
        # add the digit to the output
        output = c+output
        # output = str(num % 10)+output

    # if in the end there is still a carry left, add it in front
    if carry:
        output = "1"+output
    return "-"+output if sign else output

"""
# fast sub idea is the same as fast add but in reverse
"""
def sub(n1: str, n2: str) -> str:
    n1, lenN1, n2, lenN2 = denormalizeInputs(n1, n2)

    if n2[0] == "-":
        if n1[0] == "-":
            # invert logic as -x - -y == y - x
            n1, n2 = n2[1:], n1[1:]
        else:
            # else x - -y == x + y
            return add(n1, n2[1:])
    elif n1[0] == "-":
        # if n2 is not neg but n1 is it means -x - y == -(x + y)
        return "-"+add(n1[1:], n2)

    # optimize null operations
    if n2 == "0": return n1
    elif n1 == "0": return "-"+n2

    # making sure we only do A - B if A > B (adding the sign if it's not the case)
    isN1Sup = isASupThanB(n1, n2)
    # if it returns "0" it means that both are equal
    if isN1Sup == "0":
        return "0"
    sign = False
    # reverse and set the sign to do B - A if B > A
    if isN1Sup == "B":
        n2, n1 = n1, n2
        sign = True # set the negative sign to True

    n1, n2, lenMax = normalizeInputs(n1, n2)

    output = ""
    carry = False
    # reverse logic for range to begin at the end of both arrays
    for i in range(lenMax - 1, -1, -1):
        # if we find a floating point, add it then skip and keep eventual carry
        if n1[i] == ".":
            output = "."+output
            continue

        num = (ord(n1[i]) - ORD_0) - (ord(n2[i]) - ORD_0) - carry
        carry = False
        if num < 0:
            num += 10
            carry = True
        else:
            carry = False

        c = str(num)
        if len(c) > 1:
            c = c[1]
        output = c+output


    # print(output)
    # output, _ = denormalizeNumber(output)
    # print(output)

    return "-"+output if sign else output

def resolveFactorSign(n1: str, n2: str, sign: bool) -> (str, str, bool):
    if n1[0] == "-":
        if n2[0] != "-":
            if sign:
                sign = False
            else:
                sign = True
        else:
            n2 = n2[1:]
        n1 = n1[1:]
    elif n2[0] == "-":
        if sign:
            sign = False
        else:
            sign = True
        n2 = n2[1:]
    return n1, n2, sign

"""
# Fast multiplication idea (cheating rule "no mul, no div, no mod")
    ln1 = len(num1)
    ln2 = len(num2)
    lnTotal = (ln1 + ln2) -1
    res = [0] * (ln1 + ln2 + 1)
    
    for i in range(ln1 -1, -1, -1):
        a = int(num1[i])
        for j in range(ln2 -1, -1, -1):
            b = int(num2[j])
            idx = lnTotal - (i + j)
            res[idx] += a * b
            res[idx + 1] += res[idx] // 10
            res[idx] %= 10
    
    remZero = True
    result = ""
    for i in range(ln1 + ln2, 0, -1):
        if remZero and res[i] == 0:
            continue
        remZero = False
        result += str(res[i])
"""

def mul(n1: str, n2: str, sign: bool) -> str:
    # optimize null operations
    if n1 == "0" or n2 == "0": return "0"

    n1, lenN1, n2, lenN2 = denormalizeInputs(n1, n2)
    # -- == + ; -+ == +- == - ; --- == -
    n1, n2, sign = resolveFactorSign(n1, n2, sign)

    n1IsFloat = "." in n1
    n2IsFloat = "." in n2

    decal = (lenN1 - 1 - n1.index(".") if n1IsFloat else 0) + (lenN2 - 1 - n2.index(".") if n2IsFloat else 0)
    origDecal = decal

    # removing the floating point for n1 is much easier
    if n1IsFloat:
        n1 = n1[:n1.index(".")]+n1[n1.index(".") + 1:]
        lenN1 -= 1

    output = "0"
    # reverse logic for range to begin at the end of both normalized arrays
    for i in range(lenN1 - 1, -1, -1):
        carry = 0

        # floating point pointer
        fp = decal

        # here we "move" for each decimal already calculated after fp
        # dec = lenN1 - 1 - i - n1IsFloat - n2IsFloat - (decal if decal >= 0 else 0)
        dec = lenN1 - 1 - i - origDecal
        buffer = "0"*dec
        for j in range(lenN2 - 1, -1, -1):
            if n2[j] == ".":
                # skip the fp
                continue

            # TODO: remove last multiplication
            # num = (ord(n1[i]) - ORD_0) * (ord(n2[j]) - ORD_0) + carry

            n = (ord(n1[i]) - ORD_0)
            m = (ord(n2[j]) - ORD_0)
            num = 0
            for x in range(m):
                num += n
            num += carry

            carry = 0
            c = str(num)
            if len(c) > 1:
                carry = ord(c[0]) - ORD_0
                c = c[1]

            buffer = c+buffer

            if fp > 1:
                fp -= 1
            elif fp == 1:
                buffer = "."+buffer
                fp = 0

        # eventually consume remaining fp counter and add zeroes
        if carry:
            buffer = str(carry)+buffer
        if fp >= 1:
            if carry:
                fp -= 1
            buffer = "0."+cTimesX("0", fp)+buffer

        output = add(buffer, output)

        decal -= 1

    # NOTE: old simple algorithm not handling float (remember that at the time we needed to return 0 if B > A)
    # NOTE2: this version needed inputs to be normalized, that's why we're going through both array using `lenMax` value
    # output = "0"
    # # reverse logic for range to begin at the end of both normalized arrays
    # for i in range(lenMax - 1, -1, -1):

    #   # here we "move" for each decimal already calculated
    #   buffer = "0"*(lenMax - i - 1)
    #   carry = 0
    #   for j in range(lenMax - 1, -1, -1):
    #       num = (ord(n1[i]) - ORD_0) * (ord(n2[j]) - ORD_0) + carry
    #       # carry has been consumed
    #       carry = 0
    #       if num >= 10:
    #           carry = num // 10
    #           # carry = floor(num / 10)
    #           num %= 10
    #       buffer = str(num)+buffer
    #   if carry > 0:
    #       buffer = str(carry)+buffer

    #   output = add(buffer, output)

    # put back the sign
    return "-"+output if sign else output

# This function sole goal is to remove the floating point for n2 and multiply n1 by the necessary amount
# Example : removeFloatingPointForN2("123.456", "0.00001") gives ("12345600", 8, "1", 1) where (n1, lenN1, n2, lenN2)
# This is because it is very very much faster and easier to div that way using the reduce by substraction technique (same as by hand)
def removeFloatingPointForN2(n1: str, n2: str) -> (str, int, str, int):
    # n2 isn't a float? nothing to do then
    if not "." in n2:
        return (n1, len(n1), n2, len(n2))

    fp = n2.index(".")
    # remove the floating point entirely for n2 (as it's the entire point)
    n2 = n2[:fp]+n2[fp + 1:]
    dec = len(n2) - fp
    for i in range(len(n2)):
        if n2[i] != "0":
            n2 = n2[i:]
            break

    if n2[-1] == ".":
        n2 = n2[:-1]

    if "." in n1:
        fp = n1.index(".")
        # move the floating point away
        n1 = n1[:fp]+n1[fp + 1:]
        # decrease de decimal counter by the amount consumed moving the floating point
        dec -= len(n1) - fp

    n1 = n1+cTimesX("0", dec)

    return (n1, len(n1), n2, len(n2))

def div(n1: str, n2: str, sign: bool, limit: int = 32) -> str:
    # we need to "denormalize" inputs, to make sure there is no leading zero (this is due to the divsion method)
    n1, lenN1, n2, lenN2 = denormalizeInputs(n1, n2)
    # -- == + ; -+ == +- == - ; --- == -
    n1, n2, sign = resolveFactorSign(n1, n2, sign)

    if n2 == "0": raise Exception(ERR_Div0)
    if n1 == "0": return "0"

    # optimize identity operations
    if n1 == n2: return "-1" if sign else "1"
    if n2 == "1": return "-"+n1 if sign else n1

    # TODO: maybe clean that or at least rename!!!
    # NOTE: this is needed preparation operation since we do "sub reduce" strategy, else we get 0 and exit
    n1, lenN1, n2, lenN2 = removeFloatingPointForN2(n1, n2)
    n2, lenN2, n1, lenN1 = removeFloatingPointForN2(n2, n1)

    # slider size is the smallest junction for n1 and n2
    pt = min(lenN1, lenN2)

    # then if n2 > n1 we move the cursor preemptively by one
    if isASupThanB(n1[:pt], n2) == "B":
        pt += 1

    n1Ended = False
    floatingPast = False
    # # this is the calculation limit after n1 has been totally reduced (to avoid infinite loops)
    # limit = 32
    # start buffer up to the pointer value minus one since we add one right away
    buffer = n1[:pt - 1]
    i = pt - 1
    output = "0"
    truncate = True if limit <= 0 else False
    if truncate: limit = 1
    while (not n1Ended or (buffer != "0" and buffer != "00")) and limit > 0:

        if i >= lenN1:
            n1Ended = True
        if not n1Ended and n1[i] == ".":
            i += 1
            n1Ended = True

        # if we're past the floating point, move buffer floating point up by one decimal
        if floatingPast or n1Ended:
            if "." in buffer:
                fp = buffer.index(".")
                buffer = buffer[:fp]+buffer[fp + 1:fp + 2]+"."+buffer[fp + 2:]

        buffer = buffer+(n1[i] if i < lenN1 else "0")

        count = -1
        while buffer[0] != "-":
            count += 1
            prevBuffer = buffer
            buffer = sub(buffer, n2)

        # NOTE: this code below is the legacy code using division and modulo
        # if output != "" and count > 9:
        #   carry = count // 10
        #   output = output[:-1]+str(ord(output[-1]) - ORD_0 + carry)
        #   count %= 10
        # output += str(count)

        c = str(count)
        if output != "" and len(c) > 1:
            carry = ord(c[0]) - ORD_0
            output = output[:-1]+str(ord(output[-1]) - ORD_0 + carry)
            c = c[0]
        output += c

        # if we went to far, back up one operation
        if buffer[0] == "-":
            buffer = prevBuffer

            # if we already "consumed" all of n1, that means we are past the floating point and it needs to be added to the result
            if n1Ended and not floatingPast:
                # if limit is less than 1, it means we want no decimal (equal to // 2)
                if truncate:
                    output = output[:-1]
                    break
                output = output[:-1]+"."+c
                floatingPast = True

        if n1Ended:
            limit -= 1

        i += 1

    # NOTE: old simple code not handling floats
    # for i in range(pt - 1, lenN1):
    #   buffer = buffer+n1[i]
    #   prevBuffer = buffer
    #   buffer = sub(buffer, n2)

    #   count = 0
    #   while buffer[0] != "-":
    #       count += 1
    #       prevBuffer = buffer
    #       buffer = sub(buffer, n2)

    #   output += str(count)

    #   # if we went to far, back up one operation
    #   if buffer[0] == "-":
    #       buffer = prevBuffer

    # since we blindly add "0" even if unecessary, denomalize saves time here (and is more readable on the testing side)
    output, _ = denormalizeNumber(output)

    # put back the sign
    return "-"+output if sign else output

