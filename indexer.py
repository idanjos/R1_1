import gc
import pprint
class Indexer:
	def __init__(self): #(pair,odd) # options...
		self.dictionary = dict()
		self.filename = ""
		self.idf = []
		self.block_number = 0
		# Matrix that hold sorted tokens by size and alphabetically
		self.ordered_tokens = [[]]
	def clear(self):
		self.dictionary = dict()
		self.ordered_tokens = [[]]
		gc.collect()
		#print("Cleared")
	def setPath(self,filename):
		self.filename = filename
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
	# OrderTokens is design to order tokens by number and string. To do so, 
	# the number is added to token as a prefix string, separating both with a '-'.
	# The function sorted() then can sort tokens by their size and then by name.
	# The problem here is how can one know when 531-and > 1-octopus. By using a matrix,
	# lines corresponding to the number of digits of the document frequency, thus making it easier
	# to save to file by size then alphabetically
	def orderTokens(self):
		temp = [[]]
		for token in self.dictionary.keys():
			n = 0
			for obj in self.dictionary[token]:
				n+=len(obj[1])
			if len(str(n))-1 < len(temp):
				temp[len(str(n))-1]+=[str(n)+"-"+token]
			else:
				for i in range(len(temp),len(str(n))):
					temp+=[[]]
				temp[len(str(n))-1]+=[str(n)+"-"+token]
		#pprint.pprint(temp)
		for array in temp:
			self.ordered_tokens+=[sorted(array,reverse=True)]
	
	#Write to file
	def writeIndexes(self):

		self.block_number += 1
		file = open(self.filename+"-"+str(self.block_number), "w")
		
		for key in sorted(self.dictionary.keys()):
			output = key
			for l in self.dictionary[key]:
				output += ";"+str(l[0])+":"+str(l[1])
					
				#print(output)
			file.write(output+"\n")
		file.close()
		pass
	
	