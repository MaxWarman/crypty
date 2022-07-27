"""

Author: MaxWarman
Turbo crypto module

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

		index = (octet1 & ((1 << 1) | (1 << 0)) ) << 4 | (octet2 >> 4)
		base64String += baseChars[index]
		
		if state == 0:
			base64String += padding
			continue

		index = (octet2 & ((1 << 3)|(1 << 2)|(1 << 1)|(1 << 0)) ) << 2 | (octet3 >> 6)
		base64String += baseChars[index]
		
		if state == 1:
			base64String += padding
			continue
		
		index = (octet3 & ((1 << 5)|(1 << 4)|(1 << 3)|(1 << 2)|(1 << 1)|(1 << 0)))
		base64String += baseChars[index]

	return base64String

def hexToString(txt):
	string = ""
	for i in range(0, len(txt), 2):
		string += chr( int(f"{txt[i]}{txt[i+1]}", 16) )

	return string

def stringToHex(txt):
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

def hexToBytes(hex1):
	tmp = []
	for i in range(0, len(hex1), 2):
		left = hex1[i]
		right = "0" if i == len(hex1)-1 else hex1[i+1]
		tmp.append(int(left, 16)<<4 | int(right, 16))

	return bytearray(tmp)

def bytesToHex(bytes1):	
	h = ""
	for value in bytes1:
		tmp = hex(value)[2:]
		if len(tmp)%2 == 1:
			tmp = "0" + tmp
		h += tmp

	return h	

def stringToBytes(txt, encoding="utf-8"):
	return bytearray(txt, encoding)

def bytesToString(bytes1):
	txt = ""
	for val in bytes1:
		txt += chr(val)

	return txt

def intToBytes(number1):
	return hexToBytes(hex(number1)[2:])

def bytesToInt(bytes1):
	return int(bytesToHex(bytes1), 16)

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
	assert(stringToBase64(testPhrase) == bytesToBase64(bytearray(testPhrase, "utf-8")) == hexToBase64(stringToHex(testPhrase)) == "VGhpcyBpcyBhIHRlc3QgcGhyYXNlIGZvciBteSBiYXNlNjQgZW5jb2Rlci4=")	

def testHammingDistance():
	testPhrase1 = stringToBytes("this is a test")
	testPhrase2 = stringToBytes("wokka wokka!!!")
	assert(getHammingDistance(testPhrase1, testPhrase2) == 37)

def main():
	print("MaxWarman's Cryptopals functions module")

	testTypeConvertion()
	testXorOperation()
	testBase64encoding()
	testHammingDistance()

	print("Tests successful")


if __name__ == "__main__":
	main()