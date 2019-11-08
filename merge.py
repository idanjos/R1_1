import os
import pprint
import json
def closeAll(array):
	for io in array:
		io.close()

def deleteBlocks(files):
	for file in files:
		os.remove("results/"+file)
	pass

def merge():
	merged_file = open("merge/merged.txt","w")
	files = os.listdir("results")
	blocks = []
	for file in files:
		#print(file.split("-"))
		f = open("results/"+file,"r+")
		blocks += [f]



	bucket = {}
	n_blocks = len(blocks)
	while True:
		for i in range(0,len(blocks)):
			if str(i) not in bucket.keys() and blocks[i] != 0:
				newline = blocks[i].readline()
				if newline == "":
					#print("Bruh")
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
			print("finished Merging")
			break
		smallest_term = sorted(bucket.keys())[0+n_blocks]
		output = {}
		#pprint.pprint(bucket)
		for index in bucket[smallest_term]:
			for docinfo in bucket[str(index)]:
				key = docinfo.split(":")[0]
				postings = eval(docinfo.split(":")[1])
				#print(docinfo.split(":")[1])
				if key in output.keys():
					output[key]+= postings
				else:
					output[key]= postings
		#print(smallest_term)
		#print("Line of each file")
		#pprint.pprint(bucket)

		#pprint.pprint(output)
		line = smallest_term

		for key in sorted([int(i) for i in output.keys()]):
			line+=";"+str(key)+":"+str(sorted(output[str(key)]))
		merged_file.write(line+"\n")
		#print("Output:")
		#print(line)
		#print("Removing written data")
		for index in bucket[smallest_term]:
			bucket.pop(str(index),None)
		del bucket[smallest_term]
		#pprint.pprint(bucket)

		
		#closeAll(blocks)
	merged_file.close()
	deleteBlocks(files)

