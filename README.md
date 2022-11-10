# Crypty

Crypty is a module that I've developed during learning cryptography - especially solving tasks from:

- Cryptopals
- Cryptohack
- TryHackMe

The module itself is full of methods that I had to repetitevely use while doing challenges, they allow to automate most of tasks that I came across.

## Expected datatypes

Before I move on to explanation of ****certain methods, at first I would like to show the syntax that I chose to determine datatypes that the methods are expecting as an input.

- **bytes** - list of integers containing byte values only (0-255), especially *bytearray*
- **hex** - string of bytes in hexadecimal representation, with leading zeros (ex. int:10 is exptected to be represented as '0x0a', not just '0xa')
- **string** - just a string, usually expected to be human-readable text
- **number** - integer with no maximum size defined (method would work on either typically sized integers and 'big number' types)
- **prime** - integer that is expected to be a prime number

## Methods

### Convertion methods

- hexToString(<hex>)        -> <string>
- hexToBytes(<hex>)         -> <bytes>
- stringToBytes(<string>)   -> <bytes>
- stringToHex(<string>)     -> <hex>
- bytesToString(<bytes>)    -> <string>
- bytesToHex(<bytes>)       -> <hex>

### Encoding/Decoding methods

Methods below *encode* data given in proper data type into Base64 standard code: 

- stringToBase64(<string>)  -> <string>
- hexToBase64(<hex>)        -> <string>
- bytesToBase64(<bytes>)    -> <string>

Methods below could be used to *decode* data given in Base64 format into chosen data type:

- base64ToString(<string>)  -> <string>
- base64ToHex(<string>)     -> <hex>
- base64ToBytes(<string>)   -> <bytes>

### TODO
