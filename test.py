import hashlib

fd = open("test.bin", "wb")
fd.write(b"\xff")
fd.close()

fd1 = open("test1.bin", "wb")
fd1.write(b'\xff')
fd1.close

fd = open("test.bin", "rb")
print("test.bin")
readbytes = fd.read(4096)
print(type(readbytes))
print(len(readbytes))
print(readbytes)
stdbyte = readbytes
sha1hash2 = hashlib.sha1(readbytes)
sha1hashed2 = sha1hash2.hexdigest()
fd1 = open("test1.bin", "rb")
print("test1.bin")
readbytes2 = fd1.read()
print(len(readbytes2))
"""
if len(readbytes2) < 4096 : 
	diff = 4096 - len(readbytes2)
	readbytes2 = readbytes2 + (b"\x00" * diff)
"""
print(readbytes2)
sha1hash = hashlib.sha1(readbytes2)
sha1hashed = sha1hash.hexdigest()

print(sha1hashed2)
print(sha1hashed)

if bytearray(readbytes) == bytearray(readbytes2):
	print("bytes comparison ok!")
fd.close()
fd1.close()
