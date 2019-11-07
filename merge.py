import os

print(os.listdir("results"))
for file in os.listdir("results"):
	print(file.split("-"))
	with open("results/"+file,"r") as f:
		for line in f:
			temp = line.replace("\n","").split(";")
			print(temp[0])
			print(temp[1::])
			break