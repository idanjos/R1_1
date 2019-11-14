import re
import os
import math
import psutil
regex = re.compile(r'(\s|\[|\])')
def calculateIDF(N,data):
	#print(data)
	df = len(data.split(";"))-1
	return math.log(N/df,10)
	pass

def memory_usage_psutil():
    # return the memory usage in percentage like top
    process = psutil.Process(os.getpid())
    mem = process.memory_percent()
    return mem

def calculateWTnorm():
	pass

def calculateWT(data):
	array = data.split(";")[1::]
	#print(data.split(";")[0])
	c = 0
	output = ""
	temp = {}
	for obj in array:
		tf = len(eval(obj.split(":")[1]))
		c += tf**2
		temp[obj.split(":")[0]] = math.log(tf ,10)+1
		#output+= ";"+obj.split(":")[0]+":"+str(math.log(tf ,10)+1)+":"+re.sub(regex,'',obj.split(":")[1])
	c = math.sqrt(c)
	for obj in array:
		output+= ";"+obj.split(":")[0]+":"+str(round(temp[obj.split(":")[0]]/c,2))+":"+re.sub(regex,'',obj.split(":")[1])
	
	return output	
	pass

def calculateIndexes(N,filename,limite):
	indexBlock = 0
	vocabulary_size = 0
	final = open("result/index"+str(indexBlock)+".txt","w")
	with open(filename, "r") as fp:
		for line in fp:
			vocabulary_size+=1
			line = line.replace("\n","")
			#print(line)
			term = line.split(";")[0]
			idf = calculateIDF(N,line)
			wt = calculateWT(line) #return string plz
			output = term+":"+str(round(idf,2))+wt
			final.write(output+"\n")
			if memory_usage_psutil() > limite:
				indexBlock+=1
				final.close()
				final = open("result/index"+str(indexBlock)+".txt","w")
			
	final.close()
	os.remove(filename)
	print("Vocabulary size:"+str(vocabulary_size))
	pass

#calculateIndexes(2295504,"merge/merged.txt")