import re
import os
import math

regex = re.compile(r'(\s|\[|\])')
def calculateIDF(N,data):
	#print(data)
	df = len(data.split(";"))-1
	return str(math.log(N/df,10))
	pass

def calculateWT(data):
	array = data.split(";")[1::]
	#print(data.split(";")[0])
	output = ""
	for obj in array:
		tf = len(eval(obj.split(":")[1]))
		output+= ";"+obj.split(":")[0]+":"+str(math.log(tf,10)+1)+":"+re.sub(regex,'',obj.split(":")[1])
	return output	
	pass

def calculateIndexes(N,filename):
	vocabulary_size = 0
	final = open("result/indices.txt","w")
	with open(filename, "r") as fp:
		for line in fp:
			vocabulary_size+=1
			line = line.replace("\n","")
			#print(line)
			term = line.split(";")[0]
			idf = calculateIDF(N,line)
			wt = calculateWT(line) #return string plz
			output = term+":"+idf+wt
			final.write(output+"\n")
			
	final.close()
	os.remove(filename)
	print("Vocabulary size:"+str(vocabulary_size))
	pass

#calculateIndexes(2295504,"merge/merged.txt")