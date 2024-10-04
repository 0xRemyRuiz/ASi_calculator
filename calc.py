
from constants import *
from formatting import *
from basic import *
from advanced import *

import os

# import pdb; pdb.set_trace()

class AST_node():
    def __init__(self, value: str, isNum: bool = False):
        self.value = value
        self.isNum = isNum
        self.next = None

class ParsingError(Exception):
    def __init__(self, message, offset):
        super().__init__(message)
        self.offset = offset

# little helper to have a unified way of starting a new chain
def getAST_head():
    head = AST_node("0", True)
    head.next = AST_node("+")
    return head

# TODO: add an array of variables with associated values
def parseInput(node: AST_node, entry: str, convention: int):
    cntOpenedParentheses = 0
    # convetion here is to have "0 +" expression inserted as head
    # so prevC == "+"
    prevC, num, i = node.value, "", -1
    for c in iter(entry):
        i += 1
        # skip all the spaces in any case
        if c == " ": continue
        # if convention is US, skip "," as it is a space character
        if convention == 3 and c == ",": continue
        # if convention is EU, convert "," into dots
        if convention == 2 and c == ",": c = "."

        if (c >= "0" and c <= "9") or c == ".":
            num += c
            prevC = ""
            continue # continue parsing the number
        # if we were registering a number, add it to the node
        elif num != "":
            if node and node.value == ")":
                node.next = AST_node("*")
                node = node.next
            node.next = AST_node(num, True)
            node = node.next
            num = ""

        # simple symbol conversions
        if c == "÷":
            c = "/"
        elif c == "×":
            c = "*"
        elif c == "√" or c == "✓":
            c = "V"

        if c == "(":
            # convention here is that x(y) or (x)(y) equals x * y
            if prevC == "" or prevC == ")":
                node.next = AST_node("*")
                node = node.next
            cntOpenedParentheses += 1
        elif c == ")":
            cntOpenedParentheses -= 1
        elif c == "/" or c == "*":
            if c == "*":
                if prevC == "*":
                    # pow is either ^ or **
                    node.value = "^"
                    prevC = "^"
                    continue
            if c == "/" and prevC == "/":
                node.value = "//"
                continue
            if prevC == "+" or prevC == "-" or prevC == "(" or prevC == "^":
                raise ParsingError(ERR_BadOp, i)
        elif c == "+":
            if prevC == "*" or prevC == "/":
                continue # simplify notation
            elif prevC == "+":
                continue # skip adding pluses
            elif prevC == "-":
                # invert logic then continue
                node.value = "-"
                continue
        elif c == "-":
            if prevC == "+":
                node.value = "-"
                # simplify notation
                prevC = "-"
                continue
            elif prevC == "-":
                node.value = "+"
                # invert last entry
                prevC = "+"
                continue
        elif c == "V":
            # xVy is equal to x * Vy
            if node.isNum:
                node.next = AST_node("*")
                node = node.next
        else:
            if not (c == "^" or c == "!"):
                # if not a number, not a space and not a handled operation char
                raise ParsingError(ERR_NaN, i)

        node.next = AST_node(c)
        node = node.next
        prevC = c

        if cntOpenedParentheses < 0:
            raise ParsingError(ERR_OpPar, i)

    if num != "":
        if node and node.value == ")":
            node.next = AST_node("*")
            node = node.next
        node.next = AST_node(num, True)

    if cntOpenedParentheses > 0:
        raise ParsingError(ERR_OpPar, i)

# TODO: implement a "preResolve" function that would execute in threads all inner parenthesis before resolving the whole
DEBUG = False
depth = -1
def resolve(node: AST_node, deepMode: bool = True, limit: int = 32) -> AST_node:
    global depth
    depth += 1

    # TODO: maybe rework the whole sign handling logic
    sign, operation, resultBuffer = False, None, None
    while node != None:

        nextOp = node.next.value if node.next else None
        if DEBUG: print("{t}-D:{d} ResultBuffer={r}, Operation={o}, Node={n}".format(t=("#"*depth), d=depth, r=resultBuffer, o=operation, n=node.value))

        if node.isNum:
            # factorisation is only a "lookback" operator `n!`, so we need to "exhaust" all the "!" operator before continuing
            while nextOp == "!":
                if DEBUG: print("{t}-D:{d} doing {x}!".format(t=("#"*depth), d=depth, x=node.value))
                node.value = afacto(node.value)
                node.next = node.next.next
                nextOp = None
                if node.next != None:
                    nextOp = node.next.value

            if operation != None:
                # flush current operation unless next is a priority
                nextOp = None
                if node.next != None:
                    nextOp = node.next.value

                if (nextOp == "*" or nextOp == "/" or nextOp == "//") and deepMode:
                    # resolve priority operation (deepMode = False) before continuing
                    if DEBUG: print("{t}~Going non-deep -D:{d} ResultBuffer={r}, Operation={o}, Node={n}, NextOp={no}".format(t=("#"*depth), d=depth, r=resultBuffer, o=operation, n=node.value, no=nextOp))
                    node = resolve(node, False, limit)
                    if resultBuffer == None:
                        resultBuffer = node.value
                    # skip next hop to resolve from priority operation result
                    continue
                else:
                    if operation == "+":
                        if DEBUG: print("{t}-D:{d} doing {x} + {y}".format(t=("#"*depth), d=depth, x=resultBuffer, y=node.value))
                        if sign:
                            resultBuffer = "-"+resultBuffer
                        resultBuffer = add(resultBuffer, node.value)
                    elif operation == "-":
                        if DEBUG: print("{t}-D:{d} doing {x} - {y}".format(t=("#"*depth), d=depth, x=resultBuffer, y=node.value))
                        if sign:
                            resultBuffer = "-"+resultBuffer
                        resultBuffer = sub(resultBuffer, node.value)
                    elif operation == "*":
                        if DEBUG: print("{t}-D:{d} doing {x} * {y}".format(t=("#"*depth), d=depth, x=resultBuffer, y=node.value))
                        resultBuffer = mul(resultBuffer, node.value, sign)
                    elif operation == "/":
                        if DEBUG: print("{t}-D:{d} doing {x} / {y}".format(t=("#"*depth), d=depth, x=resultBuffer, y=node.value))
                        resultBuffer = div(resultBuffer, node.value, sign, limit)
                    elif operation == "//":
                        if DEBUG: print("{t}-D:{d} doing {x} // {y}".format(t=("#"*depth), d=depth, x=resultBuffer, y=node.value))
                        resultBuffer = div(resultBuffer, node.value, sign, 0)
                    elif operation == "^":
                        if DEBUG: print("{t}-D:{d} doing {x} ^ {y}".format(t=("#"*depth), d=depth, x=resultBuffer, y=node.value))
                        resultBuffer = apow(resultBuffer, node.value)
                    else:
                        raise Exception(ERR_UNKN)
                    sign = False

                    # if we were resolving a priority operation return the result right away
                    if not deepMode:
                        node.value = resultBuffer
                        depth -= 1
                        return node

                    # flush current operation
                    operation = None

            # there can't be a number without an operation pending (unless we're at the start of a new parenthese call)
            elif resultBuffer == None:
                resultBuffer = node.value
            else:
                raise Exception(ERR_UNKN)

        # node doesn't contain a number
        else:
            # c is a copy of node.value
            c = node.value
            if c == ")":
                # at this point, all operation need to be resolved
                if operation == None:
                    # empty parenthese return an error
                    if resultBuffer == None:
                        raise Exception(ERR_OpPar)
                    # if char is a closing parenthesis, return the current crafted node as the result
                    node.value = ("-" if sign else "")+resultBuffer
                    node.isNum = True
                    depth -= 1
                    return node
                else:
                    raise Exception(ERR_BadOp)

            if c == "+" or c == "-":
                if operation == None:
                    if resultBuffer != None:
                        operation = c
                    elif c == "-":
                        sign = True
                elif operation == "*" or operation == "/" or operation == "//" or operation == "^":
                    if c == "-":
                        sign = True
                else:
                    raise Exception(ERR_BadOp)
            elif c == "*" or c == "/" or c == "//" or c == "^":
                if operation == None:
                    operation = c
                else:
                    raise Exception(ERR_BadOp)
            elif c == "(":
                # if we encounter a parenthesis, recurse into a resolve function
                if DEBUG: print("{t}~Going deep -D:{d} ResultBuffer={r}, Operation={o}, Node={n}, NextOp={no}".format(t=("#"*depth), d=depth, r=resultBuffer, o=operation, n=node.value, no=nextOp))
                node = resolve(node.next, True, limit)
                # continue to skip `node = node.next` since we have the new node returned by the recursion instead
                continue
            # TODO: maybe improve on this so priotiy operations get treated properly
            elif c == "V":
                # square root operation is a "lookahead" operator `Vx`, so we need to "exhaust" it before continuing
                if node.next and (node.next.isNum or nextOp == "("):
                    # here we need a duplicate code for the parenthese call for now (this is due to the simple chained list nature of the AST)
                    if nextOp == "(":
                        if DEBUG: print("{t}~Going deep -D:{d} ResultBuffer={r}, Operation={o}, Node={n}, NextOp={no}".format(t=("#"*depth), d=depth, r=resultBuffer, o=operation, n=node.value, no=nextOp))
                        node.next = resolve(node.next.next, True, limit)
                    if DEBUG: print("{t}-D:{d} doing V{x}".format(t=("#"*depth), d=depth, x=node.next.value))
                    node.value = asqrt(node.next.value, limit)
                    node.isNum = True
                    # skip over current node in resolution
                    node.next = node.next.next
                    continue
                else:
                    raise Exception(ERR_invalid)
            else:
                raise Exception(ERR_invalid)

        node = node.next

    if DEBUG: print("{t}-D:{d} Result output={r}".format(t=("#"*depth), d=depth, r=resultBuffer))
    depth -= 1 
    return AST_node(resultBuffer, True)

def calc(prePromptSize: int, entry: str, convention: int = 1, limit: int = 32) -> str:
    head = getAST_head()

    resultNode = None
    try:
        parseInput(head.next, entry, convention) # 2 should be gotten from client
    except ParsingError as err:
        if prePromptSize >= 0:
            n = os.get_terminal_size().columns
            line_num = (len(entry) + prePromptSize) // n
            entry = (" "*prePromptSize)+entry
            i = err.offset+prePromptSize
            for j in range(line_num + 1):
                jn = j * n
                print(entry[jn:jn + n])
                if i >= jn and i <= jn + n:
                    print(" "*(i % n - 1)+"~^~")
        return ERR_prefix+str(err)

    try:
        resultNode = resolve(head, True, limit)
    except Exception as err:
        return ERR_prefix+str(err)

    result = ""
    if not resultNode.isNum:
        return ERR_prefix+"result node is not a number"
    else:
        result = resultNode.value

    result = convertResult(result, convention)

    result, _ = denormalizeNumber(result)

    return result
