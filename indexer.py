
import pprint
class Indexer:
	def __init__(self): #(pair,odd) # options...
		self.dictionary = dict()
		self.ordered_tokens = [[]]

		self.tokens = []
	def addIndex(self,token,doc_id,n=1): # assuming assuming array of 2, changeble compared to tuples
		if token in self.dictionary.keys():
			self.dictionary[token]+=[[doc_id,n]]
		else:
			self.dictionary[token] = [[doc_id,n]]                     
		
		#return True
	def uploadArray(self, doc_id,array):
		pass
	def print(self):
		pprint.pprint(self.dictionary)
	def orderTokens(self):
		temp = [[]]
		for token in self.dictionary.keys():
			n = 0
			for obj in self.dictionary[token]:
				n+=obj[1]
			if len(str(n))-1 < len(temp):
				temp[len(str(n))-1]+=[str(n)+"-"+token]
			else:
				for i in range(len(temp),len(str(n))):
					temp+=[[]]
				temp[len(str(n))-1]+=[str(n)+"-"+token]
		#pprint.pprint(temp)
		for array in temp:
			self.ordered_tokens+=[sorted(array,reverse=True)]
			
		
		#self.ordered_tokens = sorted(self.dictionary.keys())
		#print(sorted(unordered_list))

	def top10(self):
		temp = []
		index = len(self.ordered_tokens)
		while len(temp)< 10:
			index -= 1
			if index < 0:
				print("Error: top10 failed!, not enough words")
				break;
			for word in self.ordered_tokens[index]:
				temp += [word]
				if len(temp) >= 10:
					break
		print(temp)#return this

		
	def rarest10(self):
		temp = []
		index = -1

		while len(temp) < 10:
			index+=1
			if index >= len(self.ordered_tokens):
				print("Error: rarest10 failed!, not enough words")
			temp += self.ordered_tokens[index]

		print(sorted(temp)[:10])# shoudl be returning

		
	def writeIndexes(self): 
		pass
	def vocabularySize(self):
		return len(self.dictionary.keys())