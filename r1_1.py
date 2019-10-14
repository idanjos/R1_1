import re
import pprint as pp
import Stemmer
import time 
import indexer
import document





docid = 0
collection = []						#Collection of existing documents
indexer1 = indexer.Indexer()		#Indexer of tokenizer1

i = 0;
start = time.time()
with open("data_ri_2","r",errors="ignore") as f:
	
	text = ""
	pmid = 0
	for line in f:
		
		if "PMID-" in line:		
			pmid = line.split(" ")[1]
		if "TI  -" in line:
			text += (line.strip().split("-")[1]) if len(line.strip().split("-")) > 1 else ""
		if "PG  -" in line:
			temp = document.Document(docid,pmid,text)
			temp.tokenize1()

			for token in temp.getTokens1():
				indexer1.addIndex(token,temp.getDocID(),len(temp.getTokV1()[token]))

			collection+=[temp]
			docid+=1
			text = ""
			i+=1
		elif "TI" not in line and len(text) > 0:		#We are concatenating text
			text += " "+line.strip()
		#print(line) if "PMID" in line or "TI" in line else None
		#print(line)
		#if i > 100000:
		#	break;


	
print(len(collection))
#indexer1.print()
indexer1.orderTokens()
indexer1.rarest10()
print(indexer1.vocabularySize())
print("--- %s seconds ---" % (time.time() - start))