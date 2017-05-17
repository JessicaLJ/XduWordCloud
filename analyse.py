import os,sys,json,traceback
from nltk import Tree
#from jsonschema._validators import pattern
         
class Statistics:
    "the class to count phrase frequency and generate json file"
    printf=0                                                    #output on screen,1->print json,2->print leaves,3->print tree
    
    __rootdir__='.\Data'
    __jspath__='Json'
    __spath__='Pattern'
    __pfile__='Output\partition.txt'
    __ext__='.json'
    __outn__='model_'
    
    def __init__(self):
        "create root direction and read partiton names"
        if not(os.path.isdir(self.__rootdir__)):
            os.mkdir(self.__rootdir__)        
        if not(os.path.isdir(self.__rootdir__+'\\'+self.__jspath__)):
            os.mkdir(self.__rootdir__+'\\'+self.__jspath__)
                
    def Census(self):
        
        os.chdir(self.__rootdir__) 
        print(os.getcwd())
        partlist=self.__FromFile__(self.__pfile__)
        for partn in partlist:
            outdir=self.__jspath__+'\\'+partn
			
            if not(os.path.isdir(outdir)):
                os.mkdir(outdir)            
            data=self.__FromFile__(self.__spath__+'\\'+partn+self.__ext__)
            sjdata=json.loads(data[0])
            patterns=sjdata['patren_list']
            for num in range(len(patterns)):
                pattern=patterns[num]
                tup=self.__Count__([pattern['pattern']]+pattern['sentences'])
                dicdata={'model_num':str(num+1),'frequency':str(tup[1]-1),'data':tup[0]}
                jsdata=json.dumps(dicdata)
                if self.printf >=1 : print (jsdata)             #output on screen,1->print
                dfile=outdir+'\\'+self.__outn__+str(num+1)+self.__ext__
                self.__ToFile__(jsdata,dfile)                    
        os.chdir(os.path.dirname(os.getcwd()))
                 
        
    def __ModelLeaves__(self,model,tree,leaves):
        "get leaves of the tree by using model tree"
        if model.label()!=tree.label():
            return False
        if len(model)==0:
            leaves.append(self.__TreeLeaves__(tree))
        else:
            num=int(0)
            for tchild in tree:
                if num<len(model) and self.__ModelLeaves__(model[num],tchild,leaves):                        
                    num+=1
        return True  
    
    def __TreeLeaves__(self,tree):
        "get all leaves of the tree,and combine them to one string."
        bleaf=str()
        for leaf in tree.leaves():
            if len(bleaf)==0:
                bleaf=leaf
            else:
                bleaf+=' '+leaf
        return bleaf            
                       
    def __ToFile__(self,tobject,path):
        "write the object into the file"
        fp=open(path,'w')
        fp.write(tobject)
        fp.close()  
        
    def __FromFile__(self,path):                                
        "read object from the file"                            #only list,dict,tuple can be read
        try:
            fp=open(path,'r')      
            tobject=[line.strip() for line in fp.readlines()]
            fp.close()  
            return tobject        
        except:
            traceback.print_exc()
            exit()   
    
    def __Count__(self,stens):
        "get leaves according to model tree and count the number of apperance of each phrase "
        dlist=list()
        modeltree=Tree.fromstring(stens[0])
        for pos in range(1,len(stens)):                         #one sentence
            leaves=list()
            ttree=Tree.fromstring(stens[pos])
            self.__ModelLeaves__(modeltree,ttree,leaves) 
            self.__PrintTree__(leaves,ttree)                    #output on screen 
            count=0
            for leaf in leaves:
                leaf=leaf.lower()                                
                if(leaf[0].isalpha()):
                    if(count>=len(dlist)):
                        dlist.append(dict())
                    if(leaf in dlist[count]):
                        dlist[count][leaf]+=1
                    else:
                        dlist[count][leaf]=1  
                    count+=1   
        return (dlist,len(stens))
    
    def __PrintTree__(self,leaves,tree):                        #output on screen
        "decide whether print leaves and tree"
        if self.printf>=2: 
            print(leaves)
            if self.printf>=3:
                tree.draw()   


############################  test                              
if __name__ == '__main__':
    st=Statistics()
    st.printf=1
    st.Census()
    print(os.getcwd())
############################  end  