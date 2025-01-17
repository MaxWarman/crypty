"""

Author: MaxWarman
Description: My crypto tools module

"""

import math

def stringToBase64(string1):
	return bytesToBase64(stringToBytes(string1))

def hexToBase64(hex1):
	return bytesToBase64(hexToBytes(hex1))

def bytesToBase64(bytes1):

	"""
		1)	[********][*********][*********]
			{******} {**|****} {****|**} {*******}	<- no padding added

		2)  [********][*********][00000000]
			{******} {**|****} {****|00} {000000}	<- padding '=' added to the output

		3)	[********][000000000][000000000]	
			{******} {**|0000} {0000|00} {000000}	<- padding '==' added to the output

	"""
	baseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

	base64String = ""

	for i in range(0, len(bytes1), 3):

		state = (len(bytes1) - 1 - i) 	# 2+ - normal, 1 - padding '=', 0 - padding '==' 
		padding = ""

		octet1 = bytes1[i]

		if state != 0:
			octet2 = bytes1[i+1]
		else:
			octet2 = 0
			padding += "="

		if state >= 2:
			octet3 = bytes1[i+2]
		else:
			octet3 = 0
			padding += "="

		index = (octet1 >> 2)
		base64String += baseChars[index]

		index = (octet1 & (1<<1 | 1<<0) ) << 4 | (octet2 >> 4)
		base64String += baseChars[index]
		
		if state == 0:
			base64String += padding
			break

		index = (octet2 & (1<<3 | 1<<2 | 1<<1 | 1<<0) ) << 2 | (octet3 >> 6)
		base64String += baseChars[index]
		
		if state == 1:
			base64String += padding
			break
		
		index = (octet3 & (1<<5 | 1<<4 | 1<<3 | 1<<2 | 1<<1 | 1<<0))
		base64String += baseChars[index]

	return base64String

def base64ToBytes(string1):
	baseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	resultBytes = []

	for i in range(0, len(string1), 4):
		sextet1 = sextet2 = sextet3 = sextet4 = None
		for ind, char in enumerate(baseChars):
			if string1[i] == char:
				sextet1 = ind
			if string1[i+1] == char:
				sextet2 = ind
			if string1[i+2] == char:
				sextet3 = ind
			if string1[i+3] == char:
				sextet4 = ind

		octet1 = (sextet1 << 2) | (sextet2 >> 4)
		resultBytes.append(octet1)
		
		if sextet3 == None:
			break
		else:
			octet2 = ((sextet2 & (1<<3 | 1<<2 | 1<<1 | 1<<0)) << 4) | (sextet3 >> 2)

		resultBytes.append(octet2)

		if sextet4 == None:
			break
		else:
			octet3 = ((sextet3 & (1<<1 | 1<<0)) << 6) | sextet4

		resultBytes.append(octet3)

	return bytearray(resultBytes)

def base64ToHex(string1):
	return bytesToHex(base64ToBytes(string1))

def base64ToString(string1):
	return bytesToString(base64ToBytes(string1))

def hexToString(hex1):
	string = ""
	for i in range(0, len(hex1), 2):
		string += chr( int(f"{hex1[i]}{hex1[i+1]}", 16) )

	return string

def hexToBytes(hex1):
	if len(hex1) % 2 != 0:
		hex1 = "0" + hex1

	tmp = []
	for i in range(0, len(hex1), 2):
		left = hex1[i]
		right = hex1[i+1]
		tmp.append(int(left, 16)<<4 | int(right, 16))

	return bytearray(tmp)

def stringToHex(string1):
	txt = string1
	h = ""
	for char in txt:
		barr = bytearray(char, "utf-8")
		tmp = ""
		for value in barr:
			tmp += hex(value)[2:]
		if len(tmp)%2 == 1:
			h += "0" + tmp
		else:
			h += tmp
	return h

def stringToBytes(string1, encoding="utf-8"):
	return bytearray(string1, encoding)

def bytesToHex(bytes1):	
	h = ""
	for value in bytes1:
		tmp = hex(value)[2:]
		if len(tmp)%2 == 1:
			tmp = "0" + tmp
		h += tmp

	return h	

def bytesToString(bytes1):
	txt = ""
	for val in bytes1:
		txt += chr(val)

	return txt

def bytesToInt(bytes1):
	return int(bytesToHex(bytes1), 16)

def intToBytes(number1):
	return hexToBytes(hex(number1)[2:])

def intToHex(number1):
	h = hex(number1)[2:]
	if len(h)%2 != 0:
		h = "0" + h
	return h

def xorStrings(string1, string2, encoding="utf-8"):
	bytes1 = stringToBytes(string1, encoding)
	bytes2 = stringToBytes(string2, encoding)

	return xorBytes(bytes1, bytes2)

def xorBytes(bytes1, bytes2):
	xorValues = []
	isFirstLonger = len(bytes1) > len(bytes2)

	for i in range( max( len(bytes1), len(bytes2) )):
		if isFirstLonger:
			xorValues.append( bytes1[i] ^ bytes2[i % len(bytes2)] )
		else:
			xorValues.append( bytes1[i % len(bytes1)] ^ bytes2[i] )

	return bytearray(xorValues)

def getEnglishScore(bytes1):

	d = {
		'a':0.082, 'b':0.015, 'c':0.028, 'd':0.043, 'e':0.13, 'f':0.022, 'g':0.02,
		'h':0.061, 'i':0.07, 'j':0.0015, 'k':0.0077, 'l':0.04, 'm':0.024, 'n':0.067,
		'o':0.075, 'p':0.019, 'q':0.00095, 'r':0.06, 's':0.063, 't':0.091,
		'u':0.028, 'v':0.0098, 'w':0.024, 'x':0.0015, 'y':0.02, 'z':0.00074,
		' ':0.05
		}

	score = 0
	for value in bytes1:
		char = chr(value).lower()
		if char in d.keys():
			p = 1/d[char]
		else:
			p = 1/(0.0001)

		score += p * math.log(p, 2)

	score /= math.log(len(bytes1), 2)

	return score

def rot13(string1, key=13):
	resultRot13 = ""
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	key %= len(alphabet)
	for char in string1:
		if char in alphabet.lower():
			resultRot13 += chr( (ord(char) - ord("a") + key) % len(alphabet) + ord("a") )
		elif char in alphabet.upper():
			resultRot13 += chr( (ord(char) - ord("A") + key) % len(alphabet) + ord("A") )
		else:
			resultRot13 += char
	return resultRot13

def getGCD(number1, number2):
	while number2 != 0:
		tmp = number2
		number2 = number1 % number2
		number1 = tmp

	return number1

# Find a,b where a*x + b*y = gcd(x,y) and x,y are given
def getGcdCoefficients(number1, number2):

	if number2 == 0:
		a = 1
		b = 0
		return a, b

	a, b = getGcdCoefficients(number2, number1%number2)
	buffer = b
	b = a - number1//number2 * b
	a = buffer

	return a, b

def getMultiplicativeInverse(number1, prime):
	if number1 % prime != 0:
		return pow(number1, prime-2, prime)
	else:
		return None

def getLegendreSymbol(number1, prime):
	legendreSymbol = pow(number1, (prime-1)//2, prime)
	return legendreSymbol

def getModularSquareRoot(number1, prime):
	# source: # https://en.wikipedia.org/wiki/Tonelli–Shanks_algorithm

	# Quick solve using property of case when p == 3 (mod 4)
	if prime % 4 == 3:
		return pow(number1, (prime+1)//4, prime)
	
	# Universal solve for every odd prime (p == 1 (mod 4) & p == 3 (mod 4))
	else:
		# Step 1 - find Q and S such that: prime - 1 = Q * 2^S, Q - odd
		S = 0
		tmp = prime-1
		while tmp % 2 == 0:
			S += 1
			tmp //= 2
		Q = (prime-1) // pow(2, S)

		# Step 2 - find quadratic non-residue z in Z_p
		for i in range(2, prime):
			if getLegendreSymbol(i, prime) == prime-1:
				z = i
				break
		
		# Step 3 - loop until algorithm's criteria are met
		M = S
		c = pow(z, Q, prime)
		t = pow(number1, Q, prime)
		root = pow(number1, (Q+1)//2, prime)

		while True:
			if t == 0:
				return 0
			elif t == 1:
				return root
			else:
				for i in range(1, M):
					if pow(t, pow(2, i), prime) == 1:
						tmp = i
						break
				
				b = pow(c, pow(2, M-tmp-1, prime), prime)
				M = tmp
				c = pow(b, 2, prime)
				t = (t * c) % prime
				root = (root * b) % prime

def getShannonEntropy(bytes1):

	d = {}

	for value in bytes1:
		if value not in d.keys():
			d[value] = 1/len(bytes1)
		else:
			d[value] += 1/len(bytes1)
	
	entropy = 0
	for value in bytes1:
		p = 1/d[value]
		entropy += p * math.log(p, 2)
	
	entropy /= math.log(len(bytes1), 2)

	return entropy

def countBitsInInt(number1):
    count = 0
    while number1 > 0:
        number1 &= number1 - 1
        count += 1

    return count

def getHammingDistance(bytes1, bytes2):

    if len(bytes1) != len(bytes2):
        raise ValueError("Byte sequences have unequal lenght!")

    xorNumber = int(bytesToHex(bytes1), 16) ^ int(bytesToHex(bytes2), 16)
    hammingDistance = countBitsInInt(xorNumber)
    
    return hammingDistance

def testTypeConvertion():
	testPhrase = "This is a typ3 tr4ns14t10n t35t"
	testHex = "654bdb3a84663e6ffcabd68100000148"
	testNumber = 1234565

	assert(testPhrase == hexToString(stringToHex(testPhrase)))
	assert(testHex == bytesToHex(hexToBytes(testHex)))
	assert(testPhrase == bytesToString(stringToBytes(testPhrase)))
	assert(testNumber == bytesToInt(intToBytes(testNumber)))

def testXorOperation():
	testPhrase1 = "This is a tęst phrase."
	testPhrase2 = "None se b nars fgreag!"
	assert(xorBytes(bytearray(testPhrase1, "utf-8"), bytearray(testPhrase2, "utf-8")) == xorStrings(testPhrase1, testPhrase2))

def testBase64encoding():
	testPhrase = "This is a test phrase for my base64 encoder."
	correctEncoding = "VGhpcyBpcyBhIHRlc3QgcGhyYXNlIGZvciBteSBiYXNlNjQgZW5jb2Rlci4="
	assert(stringToBase64(testPhrase) == bytesToBase64(bytearray(testPhrase, "utf-8")) == hexToBase64(stringToHex(testPhrase)) == correctEncoding)	

def testBase64decoding():
	testPhrase = "This is a test phrase for my base64 decoder."
	correctEncoding = "VGhpcyBpcyBhIHRlc3QgcGhyYXNlIGZvciBteSBiYXNlNjQgZGVjb2Rlci4="
	assert(base64ToString(correctEncoding) == testPhrase)		

def testRot13():
	testPhrase = "This is a test phrase for my rot13 encrypter."
	assert(rot13(testPhrase) == "Guvf vf n grfg cuenfr sbe zl ebg13 rapelcgre.")

def testGCD():
	testNumber1 = 1234567891011121314151617181920212223242526272829
	testNumber2 = 89798763754892653453379597352537489494736
	assert(getGCD(testNumber1, testNumber2) == 3)

def testGcdCoefficients():
	testNumber1 = 1234567891011121314151617181920212223242526272829
	testNumber2 = 89798763754892653453379597352537489494736
	coefficient1, coefficient2 = getGcdCoefficients(testNumber1, testNumber2)
	assert(getGCD(testNumber1, testNumber2) == coefficient1 * testNumber1 + coefficient2 * testNumber2)

def testHammingDistance():
	testPhrase1 = stringToBytes("this is a test")
	testPhrase2 = stringToBytes("wokka wokka!!!")
	assert(getHammingDistance(testPhrase1, testPhrase2) == 37)

def main():
	print("MaxWarman's crypto tools module")
	print("Running tests...")

	testTypeConvertion()
	testXorOperation()
	testBase64encoding()
	testBase64decoding()
	testRot13()
	testGCD()
	testGcdCoefficients()
	testHammingDistance()

	print("Tests successful!")


if __name__ == "__main__":
	main()