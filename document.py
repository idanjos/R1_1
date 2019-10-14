import indexer
import Stemmer
import re
stopWords = open("stopwords.txt","r").read()
stemmer = Stemmer.Stemmer('english')
class Document:
	DOCID = 0
	def __init__(self,docid,pmid="0",ti=""):
		self.doc_id = docid
		docid+=1
		self.pmid = pmid
		self.ti = ti
		
		self.TokV1Dict = dict()
		self.TokV2Dict = dict()
		#self.stopwords = open("stopwords.txt","r").read() <------
	def __str__(self):
		return str(self.pmid) 
	def setPMID(self,pmid):
		self.pmid = pmid
	def setTI(self,ti):
		self.ti = ti
	def getTI(self):
		return self.ti
	def getDocID(self):
		return self.doc_id
	def getPMID(self):
		return self.pmid
	def addTI(self, ti):
		self.ti += ti
	def getTokens1(self):
		return self.TokV1Dict.keys()
	def getTokV1(self):
		return self.TokV1Dict
	def getTokV2(self):
		return self.TokV2Dict
	def tokenize1(self):
		temp = re.sub('[^a-zA-Z]+'," ",self.ti).lower()
		i = 0
		for substring in temp.split(" "):
			i+=1
			if len(substring) >= 3:
				#self.tokensv1 += [substring]

				if substring in self.TokV1Dict.keys():
					self.TokV1Dict[substring] += [i]
				else:
					self.TokV1Dict[substring] = [i]
	def tokenize2(self):
		if len(self.TokV1Dict.keys()) < 1:
			self.tokenize1() #avoid repeated code
		
		temp = self.TokV1Dict.keys()

		for key in temp:
			if key not in stopWords:
				self.TokV2Dict[stemmer.stemWord(key)] = self.TokV1Dict[key]
			
		#filter stop words