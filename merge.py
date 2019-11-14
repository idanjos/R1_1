import os
import pprint
import json



def deleteBlocks(files):
	for file in files:
		os.remove("result/"+file)
	pass

def merge(filename):
	merged_file = open(filename,"w")
	files = os.listdir("result")
	blocks = []
	for file in files:
		#print(file.split("-"))
		if "index" not in file:
			f = open("result/"+file,"r+")
			blocks += [f]



	bucket = {}
	n_blocks = len(blocks)
	while True:
		for i in range(0,len(blocks)):
			if str(i) not in bucket.keys() and blocks[i] != 0:
				newline = blocks[i].readline()
				if newline == "":
					
					blocks[i].close()
					blocks[i] = 0
					n_blocks -= 1
				else:
					key = newline.split(";")[0]
					line = newline.replace("\n","").split(";")[1::]
					if key in bucket.keys():
						bucket[key]+=[i]
					else:
						bucket[key]=[i]

					bucket[str(i)] = line
			
		if n_blocks == 0:
			
			break
		smallest_term = sorted(bucket.keys())[0+n_blocks]
		output = {}
		
		for index in bucket[smallest_term]:
			for docinfo in bucket[str(index)]:
				key = docinfo.split(":")[0]
				postings = [eval(docinfo.split(":")[1])]
				
				if key in output.keys():
					output[key]+= postings
				else:

					output[key]= postings

		line = smallest_term
		for key in sorted([int(i) for i in output.keys()]):
			
			line+=";"+str(key)+":"+str(sorted(output[str(key)]))
			
			
		merged_file.write(line+"\n")
		#pprint.pprint(bucket)
		
		for index in bucket[smallest_term]:
			bucket.pop(str(index),None)
		del bucket[smallest_term]
		
	merged_file.close()
	deleteBlocks(files)

