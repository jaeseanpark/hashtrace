count = 0
with open("walkfile.txt", "r") as f:
	for line in f:
		if line != "\n":
			count += 1

print(count)
	
