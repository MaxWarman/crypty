"""

Author: MaxWarman
Turbo crypto module

"""

import math

def stringToBase64(string):
	return hexToBase64(stringToHex(string))

def bytesToBase64(barr):
	return hexToBase64(bytesToHex(barr))

def hexToBase64(h):
	baseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

	# 0 - take first four bits; 1 - take two bits; 2 - take last four bits;
	state = 0

	base64String = ""

	base = 0
	buffer = 0

	for char in h:
		byte = int(char, 16)
		if state == 0:
			base = byte

		elif state == 1:
			buffer = byte

			base = (base << 2) | (buffer >> 2)

			base64String += baseChars[base]
			
			base = 0

		else:
			# Get rid of two left most bits
			buffer &= ~((1 << 3) | (1 << 2))
			buffer = (buffer << 4)


			base = buffer | byte

			base64String += baseChars[base]

			base = 0
			buffer = 0

		state += 1
		if state > 2:
			state = 0

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

def hexToBytes(h):
	tmp = []
	for i in range(0, len(h), 2):
		left = h[i]
		right = "0" if i == len(h)-1 else h[i+1]
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
	assert(hexToBase64(stringToHex(testPhrase)) == stringToBase64(testPhrase) == bytesToBase64(bytearray(testPhrase, "utf-8")))	

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