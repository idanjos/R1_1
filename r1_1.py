import re
import pprint as pp
import Stemmer
import time 
import indexer
import document
import sys

# Document id
docid = 0
# Collection of Documents, for future purposes
collection = []						#Collection of existing documents
indexer = indexer.Indexer()		#Indexer of tokenizer


# Begin the timer.
start = time.time()

print(sys.argv)
# Paramenter filename
if len(sys.argv) < 3:
	print("Error: no parameters found, usage: python r1_1.py [tokenizer=(1 | 2)] [filename] [more files seperated by spaces]")
for i in range(2,len(sys.argv)):
	with open(sys.argv[i],"r",errors="ignore") as f:
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
				if sys.argv[1] == "1":
					temp.tokenize1()
				elif sys.argv[1] == "2":
					temp.tokenize2()
				# Adding the tokens to the indexeres, 
				for token in temp.getTokens1():
					indexer.addIndex(token,temp.getDocID(),len(temp.getTokV1()[token]))
				for token in temp.getTokens2():
					indexer.addIndex(token,temp.getDocID(),len(temp.getTokV2()[token]))

				#Saving the document for future purposes
				collection+=[temp]
				#Next Document id, trivial
				docid+=1
				text = ""
				
			#There are scenarios where are titles with \n
			elif "TI" not in line and len(text) > 0:		#We are concatenating text
				text += " "+line.strip()
			


	#indexer1.print()
	#Sorting the tokens
	
	indexer.orderTokens()
	
	#Writing to file
	indexer.writeIndexes(sys.argv[i]+"_"+str(sys.argv[1])+"_tokens.txt")

print("--- %s seconds ---" % (time.time() - start))


	