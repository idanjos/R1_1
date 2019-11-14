import re
import pprint as pp
import Stemmer
import psutil
import time 
import indexer as Indexer
import document
import sys
import gc
import os
import merge
import random
import calculations

# Document id
docid = 0
# Collection of Documents, for future purposes
#collection = []						#Collection of existing documents
indexer = Indexer.Indexer()			#Indexer of tokenizer


# Begin the timer.
start = time.time()

#Now loads all files from input folder
def getFiles(path):
	files = os.listdir(path)
	output = []
	for file in files:
		#print(file.split("-"))
		if os.path.isdir(file):
			print(file)
			continue
		if path[-1] == "/":
			
			output += [path+file]
		else:
			output += [path+"/"+file]
	return output


print(sys.argv)
# Paramenter filename
if len(sys.argv) < 4:
	print("Error: no parameters found, usage: python r1_1.py [tokenizer=(1 | 2)] [number (0-1 activate prob of block creation after each doc)| (>=1 activates fixed size)] [folder of documents]")
	exit(1)
inputFiles = getFiles(sys.argv[-1])
option = float(sys.argv[2])
if option <= 0:
	print("Number needs to be greater than 0")
	exit(1)
for i in inputFiles:
	with open(i,"r",errors="ignore") as f:
		indexer.setPath("result/")
		text = ""
		pmid = 0
		for line in f:
			#Saving PMID for future use, I am not 100% certain
			if "PMID-" in line:		
				pmid = line.split(" ")[1]
			#Extracting the titles of each document
			if "TI  -" in line:
				text += (line.strip().split("-")[1]) if len(line.strip().split("-")) > 1 else ""
			#Assuming that the document structure is the same for all documents, each title ends when "PG -""  appears
			if "PG  -" in line:
				temp = document.Document(docid,pmid,text)
				#Token the title using both tokenizers
				# Adding the tokens to the indexeres, 
				if sys.argv[1] == "1":
					temp.tokenize1()
					for token in temp.getTokens1():
						indexer.addIndex(token,temp.getDocID(),temp.getTokV1()[token])
				elif sys.argv[1] == "2":
					temp.tokenize2()
					for token in temp.getTokens2():
						indexer.addIndex(token,temp.getDocID(),temp.getTokV2()[token])
				
				
				
				del temp
				
				#Saving the document for future purposes
				#collection+=[temp]
				#Next Document id, trivial
				docid+=1
				text = ""
				if option >= 1:
					if docid % option==0:
						indexer.orderTokens()
						indexer.writeIndexes()
						indexer.clear()
				else:
					if random.random() < option:
						indexer.orderTokens()
						indexer.writeIndexes()
						indexer.clear()
					
					
					
			#There are scenarios where are titles with \n
			elif "TI" not in line and len(text) > 0:		#We are concatenating text
				text += " "+line.strip()
			

indexer.orderTokens()
indexer.writeIndexes()
indexer.clear()
print("--- %s seconds ---" % (time.time() - start))
print("Indexing finished")

merge.merge("merge/merged.txt")
print("--- %s seconds ---" % (time.time() - start))
print("Merge finished")

calculations.calculateIndexes(docid,"merge/merged.txt")
print("--- %s seconds ---" % (time.time() - start))
print("Calculations finished")


'''
TODO LIST:
'''




	