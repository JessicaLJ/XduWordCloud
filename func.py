import sys

def getFilenames():
	#get filename list
	if(len(sys.argv) < 2):
		print('Error using')
		return None
	res = []
	for i in range(1,len(sys.argv)):
		res.append(sys.argv[i])
	return res
	
def getLevel(tpl,t):
	tmp = [tt[0] for tt in tpl if tt[1]==t]
	if len(tmp) == 0:
		return None;
	return tmp[0]	
def getTpl(t):
	tpos = t.treepositions()
	tlevel = [len(l) for l in tpos]
	tpl = []
	for i in range(0,len(tlevel)):
		tpl.append([tlevel[i],t[tpos[i]]])
	return tpl
def getTreeByLevel(tpl,tlevel):
	return [tree[1] for tree in tpl if tree[0] == tlevel]
	
def getChildren(tpl,t):
	l = getLevel(tpl,t);
	if(l is None):
		return []
	trees = list(t.subtrees())
	res = [tree for tree in trees if getLevel(tpl,tree)==(l+1)]
	return res

def getSents(filename):
	#get sents
	#filenames = func.getFilenames()
	if filename == None:
		return None	
	with open(filename,encoding='UTF-8') as file:
		if file is None:
			print('cann\'t open file : '+filename)
			return None
		res = [sent for sent in file.readlines()]
	return 	res