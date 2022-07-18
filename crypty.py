"""

Author: MaxWarman
Turbo crypto module

"""

def stringToBase64(string):
	return hexToBase64(stringToHex(string))

def bytesToBase64(barr):
	return hexToBase64(bytesToHex(barr))

def hexToBase64(h):
	baseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

	# 0 - take first four bits; 1 - take two bits; 2 - take last four bits;
	state = 0

	base64 = ""

	base = 0
	buffer = 0

	for char in h:
		byte = int(char, 16)
		if state == 0:
			base = byte

		elif state == 1:
			buffer = byte

			base = (base << 2) | (buffer >> 2)

			base64 += baseChars[base]
			
			base = 0

		else:
			# Get rid of two left most bits
			buffer &= ~((1 << 3) | (1 << 2))
			buffer = (buffer << 4)


			base = buffer | byte

			base64 += baseChars[base]

			base = 0
			buffer = 0

		state += 1
		if state > 2:
			state = 0

	return base64

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
		tmp.append(int(h[i], 16)<<4 | int(h[i+1], 16))

	return bytearray(tmp)

def bytesToHex(barr):	
	h = ""
	for value in barr:
		tmp = hex(value)[2:]
		if len(tmp)%2 == 1:
			tmp = "0" + tmp
		h += tmp

	return h	

def stringToBytes(txt, encoding="utf-8"):
	return bytearray(txt, encoding)

def bytesToString(barr):
	txt = ""
	for val in barr:
		txt += chr(val)

	return txt

def xorStrings(string1, string2, encoding="utf-8"):
	bytes1 = bytearray(string1, encoding)
	bytes2 = bytearray(string2, encoding)

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

def testTypeTranslation():
	testPhrase = "This is a typ3 tr4ns14t10n t35t"
	testHex = "654bdb3a84663e6ffcabd68100000148"

	assert(testPhrase == hexToString(stringToHex(testPhrase)))
	assert(testHex == bytesToHex(hexToBytes(testHex)))
	assert(testPhrase == bytesToString(stringToBytes(testPhrase)))

def testXorOperation():
	testPhrase1 = "This is a tęst phrase."
	testPhrase2 = "None se b nars fgreag!"
	assert(xorBytes(bytearray(testPhrase1, "utf-8"), bytearray(testPhrase2, "utf-8")) == xorStrings(testPhrase1, testPhrase2))

def testBase64encoding():
	testPhrase = "This is a test phrase for my base64 encoder."
	assert(hexToBase64(stringToHex(testPhrase)) == stringToBase64(testPhrase) == bytesToBase64(bytearray(testPhrase, "utf-8")))	

def main():
	print("MaxWarman's Cryptopals functions module")

	testTypeTranslation()
	testXorOperation()
	testBase64encoding()

	print("Tests successful")


if __name__ == "__main__":
	main()