
# this helper was designed to remove "0"*times generation since it's using the "*" symbol (since we don't want to use any)
def cTimesX(c: str, times: int) -> str:
	out = ""
	for i in range(times):
		out += c
	return(out)

def isASupThanB(n1: str, n2: str) -> str:
	# this a helper only used in this scope
	def ASupB(A: str, B: str) -> str:
		lenA = len(A)
		lenB = len(B)

		if lenB > lenA:
			return "B" # in case lenB is greater, B is superior
		elif lenA > lenB:
			return "A" # in case lenA is greater, A is superior
		isEq = False
		for i in range(lenA):
			if B[i] > A[i]:
				return "B" # B is superior
				break
			elif B[i] < A[i]:
				break
			if i == lenA - 1:
				return "0" # both are equal
		return "A" # A is superior

	# if either one has a minus sign but not the other, it's superior
	# NOTE: nowhere in the code a 0 is sent with a sign (or else this would cause a bug)
	if n1[0] == "-" and n2[0] != "-": return "B"
	if n1[0] != "-" and n2[0] == "-": return "A"

	if n1[0] == ".": n1 = "0"+n1
	if n2[0] == ".": n2 = "0"+n2

	N1 = n1.split('.')
	N2 = n2.split('.')

	res = ASupB(N1[0], N2[0])
	if res == "0":
		lenN1 = len(N1)
		lenN2 = len(N2)

		if lenN1 == lenN2 == 2:
			len2N1 = len(N1[1])
			len2N2 = len(N2[1])
			if len2N1 <= len2N2:
				N1[1] = N1[1]+cTimesX("0", len2N2 - len2N1)
			else:
				N2[1] = N2[1]+cTimesX("0", len2N1 - len2N2)
			return ASupB(N1[1], N2[1])

		elif lenN1 == lenN2 == 1:
			return "0"

		else:
			if lenN1 == 2:
				return "A"
			else:
				return "B"
	else:
		return res

# TODO: finish refactoring
# def normalizeNumber(num: str, doTail: bool = False) -> (str, int):

# makes both numbers the same size, filling with zeroes (both to the head and to the tail)
def normalizeInputs(n1: str, n2: str) -> (str, str, int):
	sign1 = False
	sign2 = False

	if n1[0] == "-":
		sign1 = True
		n1 = n1[1:]
	if n2[0] == "-":
		sign2 = True
		n2 = n2[1:]

	# fix .123 to 0.123 before split (to avoid len == 1 for .123)
	if n1[0] == ".": n1 = "0"+n1
	if n2[0] == ".": n2 = "0"+n2

	num1 = n1.split(".")
	num2 = n2.split(".")

	# get original length of number after split (len == 1 is non decimal value, len == 2 is decimal value)
	lnum1 = len(num1)
	lnum2 = len(num2)

	# there cannot be more than 2 floating point in one number
	if lnum1 > 2 or lnum2 > 2:
		raise Exception(ERR_NaN)

	# if both entries are not the same, make it so
	if lnum1 != lnum2:
		if lnum1 == 1:
			num1.insert(1, "")
		if lnum2 == 1:
			num2.insert(1, "")
		lnum1 = lnum2 = 2


	# get length for "part 1" of each number, meaning before fp or if no fp
	lenN1 = len(num1[0])
	lenN2 = len(num2[0])
	# equalize both number string length from the other length based on maximum length
	# fill up the part with zeroes at the beginning
	if lenN1 > lenN2: num2[0] = cTimesX("0", lenN1 - lenN2)+num2[0]
	elif lenN2 > lenN1: num1[0] = cTimesX("0", lenN2 - lenN1)+num1[0]

	number1 = ("-" if sign1 else "")+num1[0]
	number2 = ("-" if sign2 else "")+num2[0]

	# if no entry has decimal values, skip this part
	if lnum1 == 2:
		# get length for "part 2" of each number, meaning after fp
		len2Num1 = len(num1[1])
		len2Num2 = len(num2[1])

		# equalize both number string length from the other length based on maximum length
		# fill up the part with zeroes at the end
		if len2Num1 > len2Num2: num2[1] = num2[1]+cTimesX("0", len2Num1 - len2Num2)
		elif len2Num2 > len2Num1: num1[1] = num1[1]+cTimesX("0", len2Num2 - len2Num1)

		# put both number back together
		number1 += ("."+num1[1] if lnum1 == 2 else "")
		number2 += ("."+num2[1] if lnum2 == 2 else "")

	# return the maimum length since both are now equal (so we don't need to calculate again)
	return (number1, number2, len(number1))

def denormalizeNumber(number: str) -> (str, int):
	if not number:
		return ("0", 1)

	sign = False

	if number[0] == "-":
		number = number[1:]
		sign = True

	numList = number.split(".")

	if len(numList) == 2:
		lenFloat = len(numList[1])
		# denormalize removes trailing zeroes
		for i in range(lenFloat -1, -1, -1):
			if numList[1][i] != "0":
				numList[1] = numList[1][:i + 1]
				break
			if i == 0:
				numList[1] = ""
				break
		# recompose the number with its floating point but without its trailing spaces
		number = numList[0]+("."+numList[1] if len(numList[1]) else "")

	lenNumber = len(number)
	if lenNumber == 0: return ("0", 1)

	# denormalize removes starting zeroes
	for i in range(lenNumber):
		if number[i] == ".":
			number = "0"+number[i:]
			break
		if i == lenNumber - 1:
			number = number[i:]
			break
		if number[i] != "0":
			number = number[i:]
			break

	return ("-"+number if sign else number, len(number))

def denormalizeInputs(n1: str, n2: str) -> (str, int, str, int):
	n1, lenN1 = denormalizeNumber(n1)
	n2, lenN2 = denormalizeNumber(n2)

	return (n1, lenN1, n2, lenN2)

def convertResult(result: str, convention: int):
	decSeparator = None
	if convention == 2:
		decSeparator = " "
	elif convention == 3:
		decSeparator = ","

	if decSeparator:
		lenResult = len(result)
		lenToParse = lenResult
		resultIsFloat = "." in result
		if resultIsFloat:
			lenToParse = result.index(".")
		interval = 0
		newResult = ""
		for i in range(lenToParse - 1, -1, -1):
			if result[i] == "-":
				break
			if interval == 3:
				newResult = result[i]+decSeparator+newResult
				interval = 0
			else:
				newResult = result[i]+newResult
			interval += 1
		if resultIsFloat:
			newResult = newResult+"."+result[result.index(".") + 1:]
		if result[0] == "-":
			newResult = "-"+newResult
		result = newResult

	# this is made afterward to avoid duplicate floating point search (either "." or ",")
	if convention == 2:
		if "." in result:
			fp = result.index(".")
			result = result[:fp]+","+result[fp + 1:]

	return result
