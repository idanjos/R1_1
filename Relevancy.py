import os
import argparse
import pprint
import math

class Relevancy():
	def __init__(self):
		self.scores = []
		self.times = []
		self.profResults = dict()
		self.pmids = []
		self.index = 0
		with open ("pmid/pmids.txt","r") as f:
			for line in f:
				self.pmids += [line.split(":")[1].strip()]
		with open("query/queries.relevance.txt") as f:
			for line in f:
				key = line.split("\t")[0]
				if key in self.profResults.keys():
					self.profResults[key] += [(line.split("\t")[1],int(line.split("\t")[2]))]
				else:
					self.profResults[key] = [(line.split("\t")[1],int(line.split("\t")[2]))]
		#pprint.pprint(self.profResults)
		
		#print(self.pmids)
	def addTime(self,data):
		self.times += [data]
		
	def setResult(self,data,i):
		
		self.scores = data[1]
		self.index = i
		#print(self.scores)
	def getSimpleMetrics(self):
		relevantDocs = []
		pmid = []
		for rdoc in self.profResults[str(self.index)]:
			relevantDocs += [rdoc[0]]
		index = 0
		ap = 0
		p = 0
		r = 0
		for score in self.scores:
			index += 1
			if self.pmids[int(score[1])] in relevantDocs:
				ap += (len(pmid)+1)/index
				pmid += [(index,(len(pmid)+1)/index)]
		p = len(pmid)/index
		r = len(pmid)/len(relevantDocs)
		Map = ap/len(relevantDocs)

		fm = 0
		if p+r > 0:
			fm = (2*r*p)/(r+p)
		

		return (p,r,Map,fm) 
		pass
	
	def getRecall(self):
		pass
	def getFMeasures(self):
		pass
	def getRelevance(self,pmid,lista):
		for obj in lista:
			if obj[0] == pmid:
				return 3-int(obj[1])
		return 0
	def getNDCG(self):
		relevantDocs = []
		pmid = []
		for rdoc in self.profResults[str(self.index)]:
			relevantDocs += [(rdoc[0],rdoc[1])]
		dcg = self.getRelevance(self.pmids[int(self.scores[0][1])],relevantDocs)
		index = 1
		ndcg_reli = [dcg]
		dcg_reli = [dcg]
		
		for score in self.scores[1::]:
			index += 1
			r = self.getRelevance(self.pmids[int(score[1])],relevantDocs)
			dcg_reli += [r]
			dcg+= r/math.log(index,2)
			ndcg_reli += [r]
		ndcg_reli = sorted(ndcg_reli,reverse=True)
		idcg = ndcg_reli[0] 
		for i in range(1,len(ndcg_reli)):
			idcg+=ndcg_reli[i]/math.log(i+1,2)
		#print(dcg)
		#print(idcg)
		#print(dcg_reli)
		#print(ndcg_reli)
		if idcg <= 0:
			return 0
		if dcg >= idcg:
			print(dcg)
			print(idcg)
			print(dcg_reli)
			print(ndcg_reli)
		return dcg/idcg

		pass