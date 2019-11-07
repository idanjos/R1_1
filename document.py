import indexer
import Stemmer
import re
stopWords = open("stopwords.txt","r").read() 		#Stopwords
stemmer = Stemmer.Stemmer('english')				#Stemmer
regex = re.compile('[^a-zA-Z]')
class Document:
	DOCID = 0
	def __init__(self,docid,pmid="0",ti=""):
		#incremental doc id
		self.doc_id = docid
		#PMID possible disposal unless the user searcher by this name
		self.pmid = pmid
		#Title possible disposal unless the need to reindex phrases becomes a thing
		self.ti = ti
		self.TokV1Dict = dict()
		self.TokV2Dict = dict()
	
	#Getters
	def getDocID(self):
		return self.doc_id
	def getTokens1(self):
		return self.TokV1Dict.keys()
	def getTokens2(self):
		return self.TokV2Dict.keys()
	def getTokV1(self):
		return self.TokV1Dict
	def getTokV2(self):
		return self.TokV2Dict
	#Append to ti, possible disposal
	def addTI(self, ti):
			self.ti += ti

	#Tokenizer 1
	def tokenize1(self):
		#Non alphabetical characters are replaced with a space
		temp = regex.sub(" ",self.ti).lower()
		i = 0
		for substring in temp.split(" "):
			i+=1
			if len(substring) >= 3:
				#self.tokensv1 += [substring]

				if substring in self.TokV1Dict.keys():
					self.TokV1Dict[substring] += [i]
				else:
					self.TokV1Dict[substring] = [i]
	#Tokenizer 2
	def tokenize2(self):
		#Im using the tokens from the tokenizer 1, this helps deal with characters like  ’, -, @, etc
		if len(self.TokV1Dict.keys()) < 1:
			self.tokenize1() #avoid repeated code
		
		temp = self.TokV1Dict.keys()

		for key in temp:
			#Adding non stopWords to the dictionary, stemmer applied

			if key not in stopWords:
				if key == "and":
					print(key)
				self.TokV2Dict[stemmer.stemWord(key)] = self.TokV1Dict[key]
			
		