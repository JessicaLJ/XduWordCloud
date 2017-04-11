import os
import nltk
from nltk.tree import Tree
from nltk.parse import stanford
import queue
import func
import sys

parser = stanford.StanfordParser(model_path = './englishPCFG.ser.gz')
#'E:/stanford-parser-full-2016-10-31/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')


class singleFileParten:
	def __init__(self,file,yz=0.05):
		self.file = file
		self.score = 0
		self.fenmu = 0
		self.yz = yz
		self.wj = []
		self.pattern = self.__getSingleFilePattern()
	def __convertTree(self,sent):
		tree = parser.parse(nltk.word_tokenize(sent))
		return tree
	def __toWenJian(self,tree):
		return ' '.join(str(tree)[6:-1].split('\n'))
	def __getSingleFilePattern(self):
		self.treePattern = ""
		self.score = 0
		self.fenmu = 0
		res = []
		sents = func.getSents(self.file)
		trees = [list(self.__convertTree(sent))[0] for sent in sents]
		notInRes = []
		mark = [0 for i in range(0,len(trees))]
		for i in range(0,len(trees)):
			if mark[i] == 0:
				for j in range(i+1,len(trees)):
					if mark[j] == 0:
						
						#hasn't in
						self.socre = 0
						l1 = len(list(trees[i].subtrees()))
						l2 = len(list(trees[i].subtrees()))
						self.fenmu = (l1 if l1 > l2 else l2) -1
						mt = matchTree(trees[i],trees[j],self.fenmu)
						self.score = mt.score
						
						#self.tmp[(i,j)] = [mt.treePattern,str(trees[i])]
						if abs(self.score- 1) <= self.yz:
							mark[j] = 1
							notInRes.append([i,j])
		#combine
		mark = [0 for i in range(0,len(trees))]
		if len(notInRes) != 0:
			notInRes = sorted(notInRes)
			notIn = []
			ntmp = set(notInRes[0]);
			for i in range(1,len(notInRes)):
				if notInRes[i][0] == notInRes[i-1][0]:
					ntmp.union(set(notInRes[i]))
				else:
					notIn.append(list(ntmp))
					ntmp = set()
					ntmp.union(set(notInRes[i]))
			notIn.append(list(ntmp))
			for item in notIn:
				if len(item) == 0:
					continue
				for it in item:
					mark[it] = 1
					self.wj.append(self.__toWenJian(trees[it]))
				res.append([trees[item[0]],self.wj])
				self.wj = []
		self.wj = []
		for i in range(0,len(trees)):
			if mark[i] == 0:
				self.wj.append(self.__toWenJian(trees[i]))
				res.append([trees[i],self.wj])
				self.wj = []
		return res
		
class matchTree:
	def __init__(self,t1,t2,fenmu):
		self.treePattern = ""
		self.score = 0
		self.t1 = t1
		self.t2 = t2
		self.tpl1 = func.getTpl(t1)
		self.tpl2 = func.getTpl(t2)
		self.fenmu = fenmu
		self.__matchTree(self.t1,self.t2)
	def __matchTree(self,t1,t2):
		if t1.label() == t2.label():
			t1ch = func.getChildren(self.tpl1,t1)
			t2ch = func.getChildren(self.tpl2,t2)
			if t1.label() != 'ROOT':
				self.treePattern = self.treePattern + \
					'('+t1.label();
				self.score = self.score +1/self.fenmu
			if len(t1ch) > len(t2ch):
				t1ch,t2ch = t2ch,t1ch
			for i in range(0,len(t1ch)):
				tc1 = t1ch[i]
				for j in range(i,len(t2ch)):
					tc2 = t2ch[j]
					if tc1.label() == tc2.label():
						self.__matchTree(tc1,tc2)
						break
			if t1.label() != 'ROOT':
				self.treePattern = self.treePattern+')'
		
		
		
class mulFilePattern:
	def __init__(self,files,yz = 0.8):
		#file is a list
		self.treePattern = ""
		self.score = 0
		self.fenmu = 0
		self.yz = yz
		self.pattern = dict()
		self.files = files
		self.singleFilePartens = dict()
		self.__getAllSinglePattern()
		self.res = self.__getMulFilePattern(files)
		
	def __getAllSinglePattern(self):
		'''sgp is [tree,[wenjian ...]] '''
		for file in self.files:
			self.singleFilePartens[file] = singleFileParten(file).pattern
		
	def __getMulFilePattern(self,files):
		''' [pattern, [wenjian ...]] '''
		for i in range(0,len(files)):
			for j in range(i+1,len(files)):
				p = self.getTwoFilePattern(files[i],files[j])
				if len(p) > 0:
					for sp in p:
						tmp = []
						tmp.append(sp[1])
						if sp[0] not in self.pattern.keys():
							self.pattern[sp[0]] = [1,sp[1]]
						else:
							p1 = self.pattern[sp[0]][0]+1
							tmp = []
							for s in sp[1]:
								if s not in self.pattern[sp[0]][1]:
									tmp.append(s)
							p2 = self.pattern[sp[0]][1] + tmp
							self.pattern[sp[0]] = [p1,p2]
			
		tmp = [(v[0],(k,v)) for k,v in self.pattern.items()]
		tmp = sorted(tmp,reverse=True)
		res = []
		for item in tmp:
			res.append([item[1][0],item[1][1][1]])
		return res
		
	def getYZ(self,slen):
		pass
		
	def getTwoFilePattern(self,file1,file2):
		'''[treePttern,[wenjian ...]'''
		self.fenmu = 0
		res = []
		p1 = self.singleFilePartens[file1]
		p2 = self.singleFilePartens[file2]
		#print(p1)
		for i in range(0,len(p1)):
			for j in range(0, len(p2)):
				self.treePattern = ""
				self.score = 0
				l1 = len(list(p1[i][0].subtrees()))
				l2 = len(list(p2[j][0].subtrees()))
				self.fenmu = l1 if l1 > l2 else l2
				self.fenmu = self.fenmu -1
				mt = matchTree(p1[i][0],p2[j][0],self.fenmu)
				self.score = mt.score
				self.treePattern = mt.treePattern
				if self.score >= self.yz:
					p = []
					wenjian = p1[i][1] + p2[j][1]
					p.append(self.treePattern)
					p.append(wenjian)
					res.append(p)
		return res
class patternMatch:
	def __init__(self,yz=0.8):
		self.yz = yz
		self.res = []
		if 'Pattern' not in os.listdir('.'):
			os.mkdir('./Pattern')
		with open('./Output/partition.txt') as partition:
			ps = [line for line in partition.readlines()]
		self.ps = ps
		self.dirnum = len(os.listdir('./Output'))-1
		dirnames = ['./Output/output'+str(i) for i in range(1,self.dirnum+1)]
		for i in range(0,len(ps)):
			tmp = [ps[i]]
			filenames = [mdir+'/'+ps[i]+'.txt' for mdir in dirnames]
			tmp.append(mulFilePattern(filenames,self.yz).res)
			self.res.append(tmp)
		self.__writeInFile()
	def __writeInFile(self):
		
		for p in self.ps:
			i = 1
			r = self.getResIn(p)
			for rr in r:
				with open('./Pattern/'+p+str(i)+'.soi','w') as file:
					file.write(rr[0]+'\n')
					for s in rr[1]:
						file.write(s+'\n')
				i = i+1
						
		
	def gerRes(self):
		return self.res;
	def getResIn(self,p):
		return [item[1] for item in self.res if item[0]==p][0]
	
			
if __name__=='__main__':
	res = patternMatch()
	r = res.getResIn('text')
	print(r)
	
	