
from basic import *
from formatting import *

# TODO: maybe check apple source code for sqrt (or maybe not)
# https://opensource.apple.com/source/Libm/Libm-47.1/ppc.subproj/sqrt.c.auto.html

# https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Decimal_(base_10)
def asqrt(entry: str, limit: int = 32) -> str:
	parts = entry.split(".")
	parts0len = len(parts[0])
	# if parts0len % 2 != 0:
	if "." in div(str(parts0len), "2", False):
		parts[0] = "0"+parts[0]
	# get the first group splitted each 2 digits before the fp
	group1 = [parts[0][i:i + 2] for i in range(0, parts0len, 2)]

	def compute(group: str, c: str, p: str) -> (str, str, str):
		P = mul("20", p, False)
		# print("in", group, c, P)
		for i in range(1, 10):
			x = str(i)
			r = sub(c, mul(x, add(P, x), False))
			rVs0 = isASupThanB(r, "0")
			# if r < 0
			if rVs0 == "B":
				x = sub(x, "1")
				break
			elif rVs0 == "0":
				break
		return (x, sub(c, mul(x, add(P, x), False)), add(mul(p, "10", False), x))

	# p = 0
	# c = c * 100 + res
	# find y = x ( 20 p + x ) for y ≤ c
	# x is the result for the group
	# p = p * 10 + x
	# c -= y

	x, curr_divid, curr_quot = compute(group1[0], group1[0], "0")
	buffer = x
	# remove the first group as it's already been done
	for g in group1[1:]:
		x, curr_divid, curr_quot = compute(g, add(mul(curr_divid, "100", False), g), curr_quot)
		buffer += x

	if len(parts) >= 2:
		buffer += "."
		p1len = len(parts[1])
		group2 = [parts[1][i:i + 2] for i in range(0, p1len, 2)]
		for g in group2:
			x, curr_divid, curr_quot = compute(g, add(mul(curr_divid, "100", False), g), curr_quot)
			buffer += x

	# continue if needed up to the limit (since primes have infinite decimal)
	if curr_divid != "0":
		# if there is not fp already, we place the fp, else we just continue
		if "." not in buffer:
			buffer += "."
		for i in range(limit):
			x, curr_divid, curr_quot = compute("0", add(mul(curr_divid, "100", False), "0"), curr_quot)
			buffer += x
			if curr_divid == "0":
				break

	return buffer

def apow(x: str, times: str) -> str:
	buffer = ""
	sign = False
	# TODO: maybe remove the "int" function call, or maybe not, there is no other way to convert int to char or char to int in python
	if times[0] == "-":
		buffer = div(x, x, False)
		for i in range(int(times[1:])):
			buffer = div(buffer, x, False)
	else:
		buffer = "1"
		for i in range(int(times)):
			buffer = mul(buffer, x, False)
	return buffer

# TODO: maybe improve naive implementation with https://cs.stackexchange.com/questions/14456/factorial-algorithm-more-efficient-than-naive-multiplication
def afacto(entry: str) -> str:
	if entry[0] == "-":
		raise Exception(ERR_invalid)
	buffer = "1"
	while isASupThanB(entry, "0") == "A":
		buffer = mul(buffer, entry, False)
		entry = sub(entry, "1")
	return buffer
