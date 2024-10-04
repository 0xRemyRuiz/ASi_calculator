
import random

from constants import *
from advanced import *
from basic import *
from calc import *

# TODO: improve this barebone test sorta "framework"

printAllTestResults = False
# this is now the default since the code is stable
handleFloat = True
testCount = 0
failNumber = 0
def test(name: str, number: int, output: str, expectedOutput: str) -> bool:
    global testCount, failNumber
    output = str(output)
    expectedOutput = str(expectedOutput)
    res = output == expectedOutput
    if not res:
        print("FAIL: {name}:{no} => {out} should be {expected}".format(name=name, no=number, out=output, expected=expectedOutput))
        failNumber += 1
    testCount += 1
    return res

def printTestsAndNo(tests: [(str, str)]):
    results = []
    results.append(tests[0])
    for i in range(1, len(tests)):
        # print(tests[i])
        results.append((i, test(results[0], i, tests[i][0], tests[i][1])))
    if printAllTestResults:
        print(results)

def testNormalization():
    tests = ["testNormalization()"]
    if handleFloat:
        res = normalizeInputs("1.0", "123")
        tests.append((res[0]+" & "+res[1], "001.0 & 123.0"))

        res = normalizeInputs("123.0", ".0")
        tests.append((res[0]+" & "+res[1], "123.0 & 000.0"))

        res = normalizeInputs("123", "12")
        tests.append((res[0]+" & "+res[1], "123 & 012"))

        res = normalizeInputs("123", ".000")
        tests.append((res[0]+" & "+res[1], "123.000 & 000.000"))

        res = normalizeInputs("000123", "000")
        tests.append((res[0]+" & "+res[1], "000123 & 000000"))

        res = normalizeInputs("1.23", "1.2345")
        tests.append((res[0]+" & "+res[1], "1.2300 & 1.2345"))

        res = denormalizeInputs("00000000001.0", "123000")
        tests.append((res[0]+" & "+res[2], "1 & 123000"))

        res = denormalizeInputs("123.0000", "0000.00000")
        tests.append((res[0]+" & "+res[2], "123 & 0"))

        res = denormalizeInputs("0.01", ".1")
        tests.append((res[0]+" & "+res[2], "0.01 & 0.1"))

        res = denormalizeInputs("000012", ".000")
        tests.append((res[0]+" & "+res[2], "12 & 0"))

        res = denormalizeInputs("000123", "000")
        tests.append((res[0]+" & "+res[2], "123 & 0"))

        res = denormalizeInputs("010.0230", "1.2345")
        tests.append((res[0]+" & "+res[2], "10.023 & 1.2345"))
    printTestsAndNo(tests)

def testASuperiorToB():
    tests = ["testASuperiorToB()"]
    if handleFloat:
        tests.append((isASupThanB("1", "1.1"), "B"))
        tests.append((isASupThanB(".12", ".12"), "0"))
        tests.append((isASupThanB("12", "12"), "0"))
        tests.append((isASupThanB("1.0", "123"), "B"))
        tests.append((isASupThanB("1", "123"), "B"))
        tests.append((isASupThanB("123.1", "123"), "A"))
        tests.append((isASupThanB(".1", "123"), "B"))
        tests.append((isASupThanB("123.1", "123.1"), "0"))
    printTestsAndNo(tests)

def baseUnitTests():
    tests = ["baseUnitTests()"]
    tests.append((around("123.55"), "123.55"))
    tests.append((around("123.9"), "123.9"))
    tests.append((around("123.99"), "123.99"))
    tests.append((around("123.999999"), "124"))
    tests.append((around("123.40404"), "123.4"))
    tests.append((aabs("-123"), "123"))
    tests.append((aabs("123"), "123"))
    printTestsAndNo(tests)

def unitTestAdd():
    tests = ["unitTestAdd()"]
    tests.append((add("0", "0"), "0"))
    tests.append((add("0", "1234567890"), "1234567890"))
    tests.append((add("1", "123"), "124"))
    tests.append((add("123", "123"), "246"))
    tests.append((add("999", "999"), "1998"))
    tests.append((add("76535678763", "876543456765434"), "876619992444197"))
    tests.append((add("3456787654345678765", "987654345678876543456789876"), "987654349135664197802468641"))
    tests.append((add("999999999999999999999999999999999999999", "999999999999999999999999999999999999999"), "1999999999999999999999999999999999999998"))
    if handleFloat:
        tests.append((add("1.0", "123"), "124.0"))
        tests.append((add("123.123", "123.123"), "246.246"))
        tests.append((add("999.999", "0.001"), "1000.000"))
        tests.append((add("0.0", "123"), "123.0"))
        tests.append((add(".1", "12"), "12.1"))
        tests.append((add("23456787654.8765432345678765432", "23456765432.876543234567876"), "46913553087.7530864691357525432"))

    printTestsAndNo(tests)

def unitTestSub():
    tests = ["unitTestSub()"]
    tests.append((sub("0", "0"), "0"))
    tests.append((sub("0", "-1"), "1"))
    tests.append((sub("-1", "-1"), "0"))
    tests.append((sub("-2", "8"), "-10"))
    tests.append((sub("10", "4"), "06"))
    tests.append((sub("00000010", "00000000004"), "06"))
    tests.append((sub("0", "1234567890"), "-1234567890"))
    tests.append((sub("345678765434567654", "345678765434567654"), "0"))
    tests.append((sub("01", "8"), "-7"))
    tests.append((sub("123", "123"), "0"))
    tests.append((sub("123", "1"), "122"))
    tests.append((sub("100", "5"), "095"))
    tests.append((sub("999", "998"), "001"))
    tests.append((sub("125", "58"), "067"))
    tests.append((sub("34567876543456787655689873456791", "987654345678876543456789876"), "34566888889111108779146416666915"))
    tests.append((sub("5", "100"), "-095"))
    tests.append((sub("1", "123"), "-122"))
    tests.append((sub("765356", "765357"), "-000001"))
    tests.append((sub("19", "98"), "-79"))
    tests.append((sub("12", "91"), "-79"))
    tests.append((sub("101", "990"), "-889"))
    tests.append((sub("199", "998"), "-799"))
    tests.append((sub("76535678763", "876543456765434"), "-876466921086671"))
    tests.append((sub("0", "0"), "0"))
    tests.append((sub("0", "1234567890"), "-1234567890"))
    if handleFloat:
        tests.append((sub("0.0", "0"), "0"))
        tests.append((sub("0.0", "0."), "0"))
        tests.append((sub(".0", "0."), "0"))
        tests.append((sub("1", "1.1"), "-0.1"))
        tests.append((sub("1.5", "4"), "-2.5"))
        tests.append((sub("123.123", "123.123"), "0"))
        tests.append((sub("345676543456.765434567654", "654212345.876543"), "345022331110.888891567654"))

    printTestsAndNo(tests)

def unitTestMul():
    tests = ["unitTestMul()"]
    tests.append((mul("0", "0", False), "0"))
    tests.append((mul("1", "123", False), "123"))
    tests.append((mul("123", "1", False), "123"))
    tests.append((mul("1", "1", True), "-1"))
    tests.append((mul("-1", "-1", True), "-1"))
    tests.append((mul("-1", "-1", False), "1"))
    tests.append((mul("-1", "1", True), "1"))
    tests.append((mul("1", "-1", True), "1"))
    tests.append((mul("1", "-1", False), "-1"))
    tests.append((mul("-1", "1", False), "-1"))
    tests.append((mul("0", "1234567890", False), "0"))
    tests.append((mul("1", "1234567890", False), "1234567890"))
    tests.append((mul("001", "123", False), "123"))
    tests.append((mul("0000001", "123", False), "123"))
    tests.append((mul("0000001", "000000000000000001", False), "1"))
    tests.append((mul("123", "23", False), "2829"))
    tests.append((mul("13", "238", False), "3094"))
    tests.append((mul("754765", "7678469", False), "5795439654785"))
    tests.append((mul("797997", "9191919", False), "7335123786243"))
    tests.append((mul("234", "323", False), "75582"))
    if handleFloat:
        tests.append((mul("1.3", "3", False), "3.9"))
        tests.append((mul("1.3", "30", False), "39.0"))
        tests.append((mul("34567.765432", "2", False), "69135.530864"))
        tests.append((mul("454.5454545", "2", False), "909.0909090"))
        tests.append((mul("1.3", ".3", False), "0.39"))
        tests.append((mul("1.3", ".03", False), "0.039"))
        tests.append((mul("3", ".33", False), "0.99"))
        tests.append((mul("1.0", "123", False), "123"))
        tests.append((mul("234.0", "323.0", False), "75582"))
        tests.append((mul("123.456", "789.1011", False), "97419.2654016"))
        tests.append((mul("234.543654", "323.76543", False), "75937.12699108122"))
        tests.append((mul("3777777", "2371635716.13213", False), "8959510860782489.67501"))
    printTestsAndNo(tests)

def unitTestDiv():
    tests = ["unitTestDiv()"]
    try:
        tests.append((div("0", "0", False), ERR_Div0))
    except Exception as err:
        tests.append((str(err), ERR_Div0))
    try:
        tests.append((div("123", "0", True), ERR_Div0))
    except Exception as err:
        tests.append((str(err), ERR_Div0))
    tests.append((div("1", "1", True), "-1"))
    tests.append((div("-1", "1", True), "1"))
    tests.append((div("-1", "-1", True), "-1"))
    tests.append((div("1", "-1", True), "1"))
    tests.append((div("1", "-1", False), "-1"))
    tests.append((div("-1", "-1", False), "1"))
    tests.append((div("-1", "1", False), "-1"))
    tests.append((div("12345", "012345", False), "1"))
    tests.append((div("12345", "012345", True), "-1"))
    tests.append((div("12345", "-012345", True), "1"))
    tests.append((div("-12345", "-012345", True), "-1"))
    tests.append((div("0", "1234567890", False), "0"))
    tests.append((div("0000000000", "1234567890", False), "0"))
    tests.append((div("1234567890", "1", False), "1234567890"))

    tests.append((div("124", "2", False), "62"))
    tests.append((div("000000194", "0000000000000002", False), "97"))
    tests.append((div("194", "2", False), "97"))
    tests.append((div("110146", "2", False), "55073"))

    if handleFloat:
        tests.append((div("5", "4", False), "1.25"))
        tests.append((div("5.5", "4", False), "1.375"))
        tests.append((div("1.1", "1.1", False), "1"))
        tests.append((div("3", "1.5", False), "2"))
        tests.append((div("1", "1.1", False, 0), "0"))
        tests.append((div("1", "1.1", False), "0.9090909090909090909090909090909"))
        tests.append((div("1", "1.2", False), "0.83333333333333333333333333333333"))
        tests.append((div("10", "1.5", False), "6.66666666666666666666666666666666"))

        tests.append((div("1.2", "1.1", False), "1.09090909090909090909090909090909"))

        tests.append((div("10", "1.005", False), "9.950248756218905472636815920398"))
        tests.append((div("1000", "1.000005", False), "999.99500002499987500062499687501562"))
        tests.append((div("1", "0.00000000000010000000000000005", False), "9999999999999.99500000000000000249999999999999"))
        tests.append((div("1", "1.00000000000010000000000000005", False), "0.99999999999990000000000000994999"))
        tests.append((div("10", "1.0005", False), "9.99500249875062468765617191404297"))

        tests.append((div("7654345678", "0.05", False), "153086913560"))
        tests.append((div("7654345678", "1.05", False), "7289853026.66666666666666666666666666666666"))

        tests.append((div("001", "123", False), "0.008130081300813008130081300813"))
        tests.append((div("0.0625", "4", False), "0.015625"))
        tests.append((div("1.1", "123", False), "0.0089430894308943089430894308943"))
        tests.append((div("1234567876543234567", "2", False), "617283938271617283.5"))
        tests.append((div("1234567876543234567", "3", False), "411522625514411522.33333333333333333333333333333333"))
        tests.append((div("12300", "122", False), "100.81967213114754098360655737704918"))
        tests.append((div("12300", "122", False, 0), "100"))
        tests.append((div("123", "122", False), "1.00819672131147540983606557377049"))
        tests.append((div("1234567890", "11", False), "112233444.54545454545454545454545454545454"))
        tests.append((div("465718976546578798875125", "345678765456789", False), "1347259430.09882458663526241160768182640359"))
        tests.append((div("23456776543456787654", "23456543234", False), "1000009946.4552155099530041861239748946377"))
        tests.append((div("45678998765456789098765456787654", "7654345678992318271469421", False), "5967720.91059654787126670075480967255433"))
    printTestsAndNo(tests)

def unitTestParsing():
    tests = ['unitTestParsing()']
    convention = 1

    # TODO: fix these test cases
    try:
        tests.append((parseInput(getAST_head().next, "-1+1+2", convention) == None, True))
    except Exception as err:
        tests.append((str(err), True))
    try:
        tests.append((parseInput(getAST_head().next, "-1.1+1+2", convention) == None, True))
    except Exception as err:
        tests.append((str(err), True))
    try:
        tests.append((parseInput(getAST_head().next, "1+1+2", convention) == None, True))
    except Exception as err:
        tests.append((str(err), True))
    try:
        tests.append((parseInput(getAST_head().next, "++------1*----+++-++-+-1", convention) == None, True))
    except Exception as err:
        tests.append((str(err), True))
    try:
        tests.append((parseInput(getAST_head().next, "1 + (2 × 3 + 4 - 8) - ((2 + 3) - 1 × 2 ÷ 2) + 20 - 20 × 3", convention) == None, True))
    except Exception as err:
        tests.append((str(err), True))
    try:
        tests.append((parseInput(getAST_head().next, "1 + (-2 × 3 + 4 - -8) - ((2 + 3) - 1 × 2 ÷ 2) + 20 - 20 × 3", convention) == None, True))
    except Exception as err:
        tests.append((str(err), True))
    try:
        tests.append((parseInput(getAST_head().next, "(1)(-2 -8)1 + (10)2", convention) == None, True))
    except Exception as err:
        tests.append((str(err), True))

    # Errors

    try:
        tests.append((parseInput(getAST_head().next, "1+1A1+2", convention) == None, True))
    except Exception as err:
        tests.append((str(err), ERR_NaN))

    printTestsAndNo(tests)

def debugResolve(entry: str, convention):
    head = getAST_head()
    parseInput(head.next, entry, convention)
    print("Original parsed chain")
    node = head
    while node.next:
        print(node.value, end=" ")
        if node.next:
            node = node.next
    print(node.value)
    resultNode = resolve(head, True)
    print("Modified resolved chain")
    node = head
    while node.next:
        print(node.value, end=" ")
        if node.next:
            node = node.next
    print(node.value, end=" ")
    print("=", resultNode.value)
    return resultNode.value

def testResolve(entry: str, convention):
    head = getAST_head()
    parseInput(head.next, entry, convention)
    resultNode = resolve(head, True)
    return resultNode.value

def unitTestResolve():
    tests = ["unitTestResolve()"]
    convention = 1

    tests = ['unitTestResolve()']
    tests.append((testResolve("+    +  -   -    ----  1 * -1 ", convention), "-1"))
    tests.append((testResolve("+    +  -   -    ----  0000001 * -00000000001 ", convention), "-1"))
    tests.append((testResolve("++------1*-1", convention), "-1"))
    tests.append((testResolve("-1*-1", convention), "1"))
    tests.append((testResolve("++----+-+--1*-1", convention), "1"))
    tests.append((testResolve("-1*-1", convention), "1"))
    tests.append((testResolve("---1*-1+1", convention), "2"))
    tests.append((testResolve("+1/2-----1*-1", convention), "1.5"))
    tests.append((testResolve("+(((((((1/2)))))))-----1*-1", convention), "1.5"))
    tests.append((testResolve("1 + (-2 × 3 + 4 - -8) - ((2 + 3) - 1 × 2 ÷ 2) + 20 - 20 × 3", convention), "-37"))
    tests.append((testResolve("1 + (-2 × 3 + 4 - -8) - (--(2 + 3) - 1 × 2 ÷ 2) + 20 - 20 × 3", convention), "-37"))
    tests.append((testResolve("(1)(-2 -8)1 + (10)2", convention), "10"))

    try:
        tests.append((testResolve("1*-/1", convention), ERR_BadOp))
    except Exception as err:
        tests.append((str(err), ERR_BadOp))
    try:
        tests.append((testResolve("(1-)1", convention), ERR_BadOp))
    except Exception as err:
        tests.append((str(err), ERR_BadOp))
    try:
        tests.append((testResolve("(1-)+1", convention), ERR_BadOp))
    except Exception as err:
        tests.append((str(err), ERR_BadOp))
    try:
        tests.append((testResolve("++----*--1*-1", convention), ERR_BadOp))
    except Exception as err:
        tests.append((str(err), ERR_BadOp))
    try:
        tests.append((testResolve("+1+--/2-----1*-1", convention), ERR_BadOp))
    except Exception as err:
        tests.append((str(err), ERR_BadOp))
    try:
        tests.append((testResolve("12345 * 7654 / 23A56", convention), ERR_NaN))
    except Exception as err:
        tests.append((str(err), ERR_NaN))
    try:
        tests.append((testResolve("1,234/2", convention), ERR_NaN))
    except Exception as err:
        tests.append((str(err), ERR_NaN))

    # # tests.append((resolve(parseInput(AST_head, "1 234/2", 2)).value, "617"))
    # # tests.append((resolve(parseInput(AST_head, "1,234/2", 3)).value, "617"))
    # # tests.append((resolve(parseInput(AST_head, "1,234.123/2", 3)).value, "617"))
    # tests.append((resolve(parseInput(AST_head, "123,456/123", 2)).value, 123,456/123"1 003.70731707317073170731707317"))

    printTestsAndNo(tests)

def baseTests():
    tests = ["baseTests()"]
    tests.append((calc(-1, "123"), "123"))
    tests.append((calc(-1, "1+1"), "2"))
    tests.append((calc(-1, "1+1 +1+ 1 + 1"), "5"))
    tests.append((calc(-1, "1- 0- 1"), "0"))
    tests.append((calc(-1, "1- -- 1"), "0"))
    tests.append((calc(-1, "1---1"), "0"))
    tests.append((calc(-1, "1--1"), "2"))
    printTestsAndNo(tests)

def conventionConversionTests():
    tests = ["conventionConversionTests()"]
    tests.append((calc(-1, "123456789", 2), "123 456 789"))
    tests.append((calc(-1, "123456789", 2), "123 456 789"))
    tests.append((calc(-1, "23456789123456789123456789", 2), "23 456 789 123 456 789 123 456 789"))
    tests.append((calc(-1, "123456789", 3), "123,456,789"))
    tests.append((calc(-1, "1234567", 3), "1,234,567"))
    tests.append((calc(-1, "234567", 3), "234,567"))
    printTestsAndNo(tests)

def testAdd():
    tests = ["testAdd()"]
    tests.append((calc(-1, "1+1"), "2"))
    tests.append((calc(-1, "1+1 +1+ 1 + 1"), "5"))
    tests.append((calc(-1, "123 + 123"), "246"))
    tests.append((calc(-1, "0 + 123"), "123"))
    tests.append((calc(-1, "0 + 0"), "0"))
    tests.append((calc(-1, "123 + 0"), "123"))
    tests.append((calc(-1, "23456543434   +   1092471728468"), "1115928271902"))
    if handleFloat:
        tests.append((calc(-1, "4.123   +   4.125"), "8.248"))
    printTestsAndNo(tests)

def testSubstract():
    tests = ["testSubstract()"]
    tests.append((calc(-1, "1- -- 1"), "0"))
    tests.append((calc(-1, "1---1"), "0"))
    tests.append((calc(-1, "1--1"), "2"))
    tests.append((calc(-1, "-1-1 -1- 1 - 1"), "-5"))
    tests.append((calc(-1, "1-1 -1"), "-1"))
    tests.append((calc(-1, "1-1"), "0"))
    tests.append((calc(-1, "123 - 123"), "0"))
    tests.append((calc(-1, "12 - 123"), "-111"))
    tests.append((calc(-1, "12 - 0"), "12"))
    tests.append((calc(-1, "0 -12- 0"), "-12"))
    tests.append((calc(-1, "0- 12 -0"), "-12"))
    tests.append((calc(-1, "458791296437812469   -   761254768172467"), "458030041669640002"))
    if handleFloat:
        tests.append((calc(-1, "12.345   -   2.9456"), "9.3994"))
    printTestsAndNo(tests)

def testDivide():
    tests = ["testDivide()"]
    tests.append((calc(-1, "12 / 0"), ERR_prefix+ERR_Div0))
    tests.append((calc(-1, "0 / 12"), "0"))
    tests.append((calc(-1, "0 / 0"), ERR_prefix+ERR_Div0))
    tests.append((calc(-1, "12 / -1"), "-12"))
    tests.append((calc(-1, "12 / 2"), "6"))
    tests.append((calc(-1, "12 / -2"), "-6"))
    tests.append((calc(-1, "12 / -2 / -1"), "6"))
    tests.append((calc(-1, "465718976546578798875125   //   345678765456789"), "1347259430"))
    if handleFloat:
        tests.append((calc(-1, "465718976546578798875125   /   345678765456789"), "1347259430.09882458663526241160768182640359"))
        tests.append((calc(-1, "123456/123"), "1003.7073170731707317073170731707317"))
    printTestsAndNo(tests)

def testMultiply():
    tests = ["testMultiply()"]
    tests.append((calc(-1, "12 * 0"), "0"))
    tests.append((calc(-1, "0 * 12"), "0"))
    tests.append((calc(-1, "0 * 0"), "0"))
    tests.append((calc(-1, "12 * -1"), "-12"))
    tests.append((calc(-1, "12 * 2"), "24"))
    tests.append((calc(-1, "12 * -2"), "-24"))
    tests.append((calc(-1, "12 * -2 * -1"), "24"))
    tests.append((calc(-1, "12 * - 2 *-1"), "24"))
    tests.append((calc(-1, "91284817318 * 23784"), "2171118095091312"))
    tests.append((calc(-1, "91284817318 * 78213 * 1273865"), "9094962243100062596910"))
    if handleFloat:
        tests.append((calc(-1, "3456.34   *   3456.345"), "11946303.4773"))
    printTestsAndNo(tests)

def testAdvanced():
    tests = ["testAdvanced()"]
    # test x to the power of y
    tests.append((apow("2", "2"), "4"))
    tests.append((apow("-2", "2"), "4"))
    tests.append((apow("3", "2"), "9"))
    tests.append((apow("3", "3"), "27"))
    tests.append((apow("-3", "3"), "-27"))
    tests.append((apow("9", "2"), "81"))
    tests.append((apow("9", "3"), "729"))
    tests.append((apow("9", "1"), "9"))
    tests.append((apow("9", "0"), "1"))
    # test negative value x to the power of -y
    tests.append((apow("4", "-1"), "0.25"))
    tests.append((apow("4", "-2"), "0.0625"))
    tests.append((apow("3", "-2"), "0.11111111111111111111111111111111"))
    tests.append((apow("3", "-3"), "0.03703703703703703703703703703703"))

    # test square root of 2
    tests.append((asqrt("9"), "3"))
    tests.append((asqrt("152.2756"), "12.34"))
    tests.append((asqrt("1194.3936"), "34.56"))
    tests.append((asqrt(apow("12345.67", "2")), "12345.67"))
    tests.append((asqrt(apow("76543400000000004567", "2")), "76543400000000004567"))
    tests.append((asqrt(apow("76543400000000004567.8701232130213012300000", "2")), "76543400000000004567.87012321302130123"))
    tests.append((asqrt(apow("767892876567876567898767543400000000004567.870123213021301230000098765456787654567", "2")), "767892876567876567898767543400000000004567.870123213021301230000098765456787654567"))
    # test square root of 2 for prime numbers (infinite result)
    tests.append((asqrt("13"), "3.60555127546398929311922126747049"))
    tests.append((asqrt("13.13"), "3.623534186398687752830414178924353"))
    tests.append((asqrt("10005", 64), "100.0249968757810059447921878763577780015950243686963146571355115696"))

    # test factorisation (small because it is costly)
    tests.append((afacto("0"), "1"))
    tests.append((afacto("1"), "1"))
    # tests.append((afacto("-1"), ERR_prefix+ERR_invalid))
    tests.append((afacto("2"), "2"))
    tests.append((afacto("3"), "6"))
    tests.append((afacto("4"), "24"))
    tests.append((afacto("13"), "6227020800"))
    tests.append((afacto("20"), "2432902008176640000"))

    # test combined syntax for previous advanced operations 
    tests.append((calc(-1, "-4!"), "-24"))
    tests.append((calc(-1, "(-4)!"), ERR_prefix+ERR_invalid))
    tests.append((calc(-1, "4!*3"), "72"))
    tests.append((calc(-1, "2*4!"), "48"))
    tests.append((calc(-1, "(2*2)!"), "24"))
    tests.append((calc(-1, "(4)!"), "24"))
    tests.append((calc(-1, "()!"), ERR_prefix+ERR_OpPar))
    tests.append((calc(-1, "1+(2*2)!-1"), "24"))
    tests.append((calc(-1, "1+(2*2)!*1"), "25"))
    tests.append((calc(-1, "5(2*2)!"), "120"))
    tests.append((calc(-1, "5V4"), "10"))
    tests.append((calc(-1, "5V"), ERR_prefix+ERR_invalid))
    tests.append((calc(-1, "5*V4"), "10"))
    tests.append((calc(-1, "5V(2*2)!"), "10"))
    tests.append((calc(-1, "5V((2*2)!)"), "24.4948974278317809819728407470589"))
    tests.append((calc(-1, "2^3!"), "64"))
    tests.append((calc(-1, "2**3!"), "64"))
    tests.append((calc(-1, "V(2**3!)"), "8"))
    # tests.append((calc(-1, "V2**3!"), "8")) # TODO: make this work
    tests.append((calc(-1, "2^!"), ERR_prefix+ERR_invalid))
    tests.append((calc(-1, "2^^3!"), ERR_prefix+ERR_BadOp))
    tests.append((calc(-1, "2***3"), ERR_prefix+ERR_BadOp))
    tests.append((calc(-1, "2**/3"), ERR_prefix+ERR_BadOp))
    tests.append((calc(-1, "3!!"), "720"))
    tests.append((calc(-1, "((3!)!)"), "720"))
    tests.append((calc(-1, "(((3)!)!)"), "720"))
    tests.append((calc(-1, "(3!!)"), "720"))
    tests.append((calc(-1, "((1)!)!!"), "1"))
    tests.append((calc(-1, "((2)!)!!"), "2"))

    # advanced functions
    # testing nth root function in conjunction with apow function with result rounded (for consistency)
    tests.append((around(apow(aroot("1234", "4"), "4")), "1234"))
    tests.append((around(apow(aroot("-9", "3"), "3")), "-9"))
    tests.append((around(apow(aroot("765345", "7"), "7")), "765345"))
    # random int
    rand_num, rand_expo = str(random.randint(1234, 4321)), str(random.randint(3, 7))
    tests.append((around(apow(aroot(rand_num, rand_expo), rand_expo)), rand_num))
    printTestsAndNo(tests)

def testParenthesis():
    tests = ["testParenthesis()"]
    tests.append((calc(-1, "(2+3)+2*3"), "11"))
    tests.append((calc(-1, "-2*(1+1)+1-6"), "-9"))
    tests.append((calc(-1, "-(2*(1+1)+1)-6"), "-11"))
    tests.append((calc(-1, "-((2/2)*(2)/(1+1)+1)-6"), "-8"))
    tests.append((calc(-1, "-(2*1/(1+1)+1)-6"), "-8"))
    tests.append((calc(-1, "-(((2*((1+1))+1)))-6"), "-11"))
    tests.append((calc(-1, "-(-(-(2*((1+1))+1)))-6"), "-11"))
    tests.append((calc(-1, "---+-+-(-(-(2*(--(1+1))+1)))-6"), "-11"))
    tests.append((calc(-1, "-(1+1)*2+(4)+(5-10/2)-((1+1)/2-1)"), "0"))
    tests.append((calc(-1, "-(1+1)*2+(4)+(5-10/2)-((1+1)/2-1) + (1 + 1)"), "2"))
    try:
        tests.append((calc(-1, "1-()"), ERR_prefix+ERR_OpPar))
    except Exception as err:
        tests.append((str(err), ERR_prefix+ERR_OpPar))
    try:
        tests.append((calc(-1, "---+-+-(-(-(2*(--(1+1))+1)-))-6"), ERR_prefix+ERR_BadOp))
        #                                                   ^-- here is the error, ")-)" doesn't mean anything
    except Exception as err:
        tests.append((str(err), ERR_prefix+ERR_BadOp))
    try:
        tests.append((calc(-1, "---+-+-((-(-(2*(--(1+1))+1)))-6"), ERR_prefix+ERR_OpPar))
        #                                ^-- here is the error, this parenthese is too much
    except Exception as err:
        tests.append((str(err), ERR_prefix+ERR_OpPar))

    printTestsAndNo(tests)

def do_heavyTestingCalc():
    tests = ["heavyTestingCalc()"]

    # little priority test
    tests.append((calc(-1, " 1 + 1 / 1287469297356 * 10000000000000"), "8.7671755128735202121"))

    tests.append((calc(-1, "654323456789876543212345764323456789098765432123456789098765432123456789876543212345678998765432345678987654321234567898765432345678987654323456789876543345678876543234567898765432345678987654321234567898765432345678987654/8432234567898765432123456789098765432345678987654323456789876543245678987654345678909876543234567890987654345678987654324567898765434567898765433456782876543456789876543276543234567898765434567898765434567898765434567876542"), "0.07759787177658268984599095433463"))
    tests.append((calc(-1, "234567987654323456789876543456789876543*98765456789876543456787654.12214124214214-234567987654323456789876543456789876543*98765456789876543456787654.12214124214214"), "0"))
    tests.append((calc(-1, "6543456789.8765432345678/1276545687.7654321234567876543-6543456789.8765432345678/1276545687.7654321234567876543"), "0"))
    tests.append((calc(-1, "(234567987654323456789876543456789876543*98765456789876543456787654.12214124214214 + 6543456789.8765432345678/1276545687.7654321234567876543) - (234567987654323456789876543456789876543*98765456789876543456787654.12214124214214 + 6543456789.8765432345678/1276545687.7654321234567876543)"), "0"))
    # TODO: check this test as it seems wrong
    tests.append((calc(-1, "987654567-87654345678*87456789/8543212345678.876543234567+76543234567.987654323456787654323456789876543234567-654234567/876542345678765432*76543234567898765432+876543456789-43223456789987.8765434567/654321+(6543234567.6543212345-7654345678.876543234)"), "895765861781.343842729539448887925182778484243234567"))

    # NOTE: Python3 is not good with numbers (or at least it rounds up A LOT to increase performance)
    # I want to add that in python3, `round(1.5) == round(2.5)` while I know that it's not "python specific" and it's algorithmic related but man, that's wrong...
    # 654323456789876543212345764323456789098765432123456789098765432123456789876543212345678998765432345678987654321234567898765432345678987654323456789876543345678876543234567898765432345678987654321234567898765432345678987654/8432234567898765432123456789098765432345678987654323456789876543245678987654345678909876543234567890987654345678987654324567898765434567898765433456782876543456789876543276543234567898765434567898765434567898765434567876542*0.07759787177658269
    # = 654323456789876543212345764323456789098765432123456789098765432123456789876543212345678998765432345678987654321234567898765432345678987654323456789876543345678876543234567898765432345678987654321234567898765432345678987654/8432234567898765432123456789098765432345678987654323456789876543245678987654345678909876543234567890987654345678987654324567898765434567898765433456782876543456789876543276543234567898765434567898765434567898765434567876542*0.07759787177658268984599095433463

    # NOTE: examples (division) below have an infinite number of decimal so it's been crafted around the limit constant of value "32"
    tests.append((calc(-1, "654323456789876543212345764323456789098765432123456789098765432123456789876543212345678998765432345678987654321234567898765432345678987654323456789876543345678876543234567898765432345678987654321234567898765432345678987654/8432234567898765432123456789098765432345678987654323456789876543245678987654345678909876543234567890987654345678987654324567898765434567898765433456782876543456789876543276543234567898765434567898765434567898765434567876542/0.07759787177658268984599095433463"), "1"))
    tests.append((calc(-1, "654323456789876543212345764323456789098765432123456789098765432123456789876543212345678998765432345678987654321234567898765432345678987654323456789876543345678876543234567898765432345678987654321234567898765432345678987654/8432234567898765432123456789098765432345678987654323456789876543245678987654345678909876543234567890987654345678987654324567898765434567898765433456782876543456789876543276543234567898765434567898765434567898765434567876542/0.0775978717765826898459909543346397877692736310656283698419534063"), "0.99999999999999999999999999999987"))

    tests.append((calc(-1, "12356789987654345678765432345678765432345678+876543234567887654321234567-87654321234567887654323456789876543*5432345+765432345676543234567/7654-765432345678987654323456789", 2), "11 880 621 473 967 347 098 216 795 575 707 789 524 487 812,9998693493598118630781290828325"))
    tests.append((calc(-1, "5678765432345678+567887654321234567-567887654323456789876543*5432345+32345676543234567/7654-003767654345678543345678902345678987654323456789", 2), "-3 767 654 345 678 546 430 640 561 870 864 292 210 475 512 187,0001306506401881369218709171675"))
    tests.append((calc(-1, "12356789987654345678765432345678765432345678+876543234567887654321234567-87654321234567887654323456789876543*5432345+765432345676543234567/7654-765432345678987654323456789", 3), "11,880,621,473,967,347,098,216,795,575,707,789,524,487,812.9998693493598118630781290828325"))

    printTestsAndNo(tests)

def do_fullUnitTests():
    baseUnitTests()
    testNormalization()
    testASuperiorToB()
    unitTestAdd()
    unitTestSub()
    unitTestMul()
    unitTestDiv()

def do_fullTestsCalc():
    unitTestParsing()
    unitTestResolve()
    baseTests()
    conventionConversionTests()
    testParenthesis()
    testAdd()
    testSubstract()
    testDivide()
    testMultiply()
    testAdvanced()

# NOTE: good verification source is: https://www.dcode.fr/big-numbers-division
# TODO: maybe integrate new tests like in https://github.com/Jrmy-rbr/inf/blob/master/Test.js
# TODO: maybe integrate new tests like in https://github.com/gavinhoward/bc/tree/master/tests/bc

# do_fullUnitTests()
# do_fullTestsCalc()
# do_heavyTestingCalc()

baseUnitTests()
testAdvanced()

print()
print("Total number tests run:", testCount)
print("Total number of test failed:", failNumber)
print()
