import os
import pprint as pp
import document
import math
import argparse
import time

#Argument parser
def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()
   

    # Optional arguments
    parser.add_argument("-b", "--bm25", help="Enable BM25 1, else 0", type=int, default=0)
    parser.add_argument("-t", "--tokenizer", help="Tokenizer version 1,2", type=int, default=2)
   
    # Print version
    parser.add_argument("--version", action="version", version='%(prog)s - Version 3.0')

    # Parse arguments
    args = parser.parse_args()
   
    if args.tokenizer not in [1,2]:
    	print("Supported tokenizer version: 1 or 2")
    	exit(1)



    return args



class RankRetrieval():
	
	def __init__(self,t=1):
		self.indice = {} # Position of letter in array
		self.t = t
		self.array = []  # Array of tuples (term,idf)
		self.docLengths = []
		self.avdl = 0
		self.b = 0
		self.k = 0
		
		pass

	def load(self):
		files = os.listdir("index")
		for file in files:
			#print(file)
			with open("index/"+file,"r") as f:
				for line in f:
					term = line.split(":")[0]
					idf = float(line.split(":")[1].split(";")[0])
					if term[0] not in self.indice.keys():
						self.indice[term[0]] = len(self.array)
					self.array+=[(term,idf)]
		with open("length/doclength.txt","r") as f:
			for line in f:
				self.docLengths += [float(line.strip().split(":")[1])]
		self.avdl = self.getAvgDocLength()
		

		#print(self.array)
		
		pass

	def __getitem__(self):
		pass

	def __repr__(self):
		return str(self.array)

	def getAvgDocLength(self):
		output = self.docLengths[0]
		for i in range(1,len(self.docLengths)):
			output = ((output * i) + self.docLengths[i])/(i+1)

		return output
	def getTF(self,tf,dl):
		
		alpha = (1 - self.b + self.b * (dl/self.avdl))
		tf2 = tf * (self.k + 1) / (self.k * alpha + tf)
		return tf2

	def BM25Score(self,lines,tokens):
		documents = dict()
		for line in lines:
			term = line.split(";")[0].split(":")[0]
			array = line.split(";")[1::]
			for doc in array:
				docid = doc.split(":")[0]
				wt = doc.split(":")[1]
				if docid in documents.keys():
					documents[docid] += tokens[term][0] * self.getTF(tokens[term][1],self.docLengths[int(docid)]) * float(wt)
				else:
					documents[docid] = tokens[term][0] * self.getTF(tokens[term][1],self.docLengths[int(docid)]) * float(wt)
		#pp.pprint(documents)
		return documents
		pass
	
	def queryParse(self,string,bm25 = False):
		query = document.Document(0,"",string)
		query.tokenize2() if self.t == 2 else query.tokenize1() 
		tokens = (query.getTokV2() if self.t == 2 else query.getTokV1())
		#pp.pprint(tokens)
		for key in tokens.keys():
			if key[0] not in self.indice.keys():
				continue
			index = 0 + self.indice[key[0]]
			while index < len(self.array):
				
				#print(self.array[index][0])
				if self.array[index][0] == key:
					
					idf = float(self.array[index][1])
					tf = (math.log(len(tokens[key]),10)+1)
					#print(idf)
					
					tokens[key] = (idf,tf)
					
					break

				else:
					
					if self.array[index][0][0] != key[0] or (index+1) == len(self.array):
						tokens[key] = 0
						print("not found")
						break
				index+=1
		
		qL = self.queryLength(tokens)
		for key in tokens.keys():
			
			tokens[key] = (tokens[key][0]/qL,tokens[key][1]) if qL > 0 else tokens[key]
		#print("Query length: " + str(qL))
		#pp.pprint(tokens)
		docs = self.queryDocuments(tokens)

		return self.queryScoreLNC_LTC(docs,tokens) if not bm25 else self.BM25Score(docs,tokens)

	def queryScoreLNC_LTC(self,lines,tokens):
		documents = dict()
		for line in lines:
			term = line.split(";")[0].split(":")[0]
			array = line.split(";")[1::]
			for doc in array:
				docid = doc.split(":")[0]
				wt = doc.split(":")[1]
				if docid in documents.keys():
					documents[docid] += tokens[term][0] * tokens[term][1] * float(wt)
				else:
					documents[docid] = tokens[term][0] * tokens[term][1] * float(wt)
		#pp.pprint(documents)
		return documents
		pass

	def queryLength(self,tokens):
		output = 0
		for key in tokens.keys():
			
			output+= (tokens[key][0]*tokens[key][1]) ** 2
		return math.sqrt(output)
		pass

	def unweightedQuery(self):
		'''
		No weighting on query terms§Assume each query term occurs only once•Then for ranking, 
		don’t need to normalize query vector§Slight simplification ofprevious algorithm
		'''
		pass

	def termElimination(self):
		'''
		Only consider high-idfquery terms§low idfare treated as stop words and do not contribute to the score•Only consider docs containing many query terms
		'''
		pass

	def documentProduct(self):
		'''
		For multi-term queries, only compute scores for docs containing several of the query terms, example 3/4 something
		'''

	def queryDocuments(self,tokens):
		letters = { x[0] for x in tokens.keys() }
		documents = []
		for letter in letters:
			i = 0
			flag = 0
			while True:
				if not os.path.exists("index/index_"+letter+str(i)+".txt"):
					#print("nOT FOUND "+("index/index_"+letter+str(i)))
					break;

				with open("index/index_"+letter+str(i)+".txt","r") as f:
					
					for line in f:

						if line.split(":")[0] in tokens.keys():
							documents += [line]
							#print(line)
							flag = 1
							break;
				if flag == 1:
					break
				i += 1

		print(letters)
		return documents


def main(args):
	rr = RankRetrieval(t=args.tokenizer)
	rr.load()
	i = 0
	with open("query/queries.txt","r") as f:
		for line in f:
			i+=1
			startT = time.time()
			result = 0
			if args.bm25 == 1:
				results = rr.queryParse(line.strip(),bm25=True)
			else:
				results = rr.queryParse(line.strip())
			temp = []
			for key in results.keys():
				temp += [(results[key],key)]
			output = open("queryResults/query"+str(i)+".txt","w")
			output.write(line.strip()+"\n")
			output.write(str(sorted(temp[0:50],reverse=True)))
			output.write("\n"+str(time.time() - startT))
			output.close()
			print(str(time.time() - startT)+"s")
	pass
		
if __name__== "__main__":
	main(parseArguments())


'''
2) Calculate Query Vector length, I have manage to extract IDF from file and preform tf-idf for wt -> LNC.LTC SCHEME
12-4) queryDocuments is getting the lines of each term from the index database. Calculate score of the documents found
12-5) queryParse now returns results of each queries
12-6) Now order the results by score, and do precision, recall, f-measure, average precision, precision at rank 10 and NDCG for each queries. 
50 queries then divide by 50 for the average. 
Then rocchio algorithm and repeat.
'''
