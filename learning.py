# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 22:26:22 2017

@author: 李娇
"""

import os
import nltk
import json

class TextProc:
    def transtotext(self, finput):
        pdfname = './Data/Input/'+finput
        trans  = "pdftotext.exe -nopgbrk -layout"
        os.system("%s %s" % (trans, pdfname))
        textname = './Data/Input/'+finput.split('.')[0]+".txt"
        print(os.getcwd())
        textresult = open("%s" % textname, "r", encoding = "latin-1")
        #read line by line
        self.raw_data = textresult.readlines()
      # print(self.raw_data)
        #line number
        self.lineNum = self.raw_data.count
        textresult.close()
        os.remove(textname)
     
    def isSentence(self,sent):
        unSentToken = ['@', '\\', '//', '/', '=', '{', '}','~','+']
        for token in sent:
            if token in unSentToken:
               return False
            else:
                continue               
        return True
              
    def preprocess(self, pdfnum):
        #print(self.raw_data)
        self.abstr = []
        self.intro = []
        self.theor = []
        lineAbs = 0
        lineRef = 0
        num = 0
        for line in self.raw_data:
            if('Abstract' in self.raw_data[num]):
                lineAbs = num
            if('References' in self.raw_data[num]):
                lineRef = num
            num = num+1
        #back to parent directory
        #os.chdir(os.path.dirname(os.getcwd()))
        os.chdir('./Data/')
        flag1 = os.path.exists(".\Output")
        if not flag1:
            os.makedirs(".\Output")
        par = open(".\Output\partition.txt", "w+", encoding="latin-1")
        par.writelines("abstract\n")
        par.writelines("introduction\n")
        par.writelines("theory\n")
        par.close()
        #remove \n remove 连词
    #    punc = [',','.',':','?','-']
        count = lineAbs
        self.textString = ""
        while(count<lineRef):
            if(self.raw_data[count]!='\n'):
                if(self.raw_data[count][-2] == '-'):
                    self.textString = self.textString+self.raw_data[count].strip()
                else:
                    self.textString = self.textString+" "+self.raw_data[count].strip()
            count = count+1
    #    print(self.textString)##此时已经出现了eval- uate
        #filter
        textFilterText = ""
        sent_token = nltk.sent_tokenize(self.textString)
 #       print(sent_token)
        for sent in sent_token:
           if self.isSentence(sent):
               textFilterText = textFilterText+" "+sent
   #     print(textFilterText)
        absindex = textFilterText.find("Abstract")
        keyindex = textFilterText.find("Keywords")
        introindex = textFilterText.find("Introduction")
        theoindex = textFilterText.find("2.")
        self.abstr = textFilterText[absindex+9:keyindex]
        self.intro = textFilterText[introindex+12:theoindex]
        self.theor = textFilterText[theoindex+2:]
        os.chdir(".\Output")
        pdfnumstr = str(pdfnum)
        flag2 = os.path.exists(".\output" +pdfnumstr)
        if not flag2:
            os.makedirs(".\output%s"% pdfnumstr)
        os.chdir(".\output"+pdfnumstr)
        self.abstr = nltk.sent_tokenize(self.abstr)
        with open("./abstract.json",'w') as f:
            f.write(json.dumps(self.abstr))
        self.intro = nltk.sent_tokenize(self.intro)
        with open("./introduction.json",'w') as f:
            f.write(json.dumps(self.intro))
        self.theor = nltk.sent_tokenize(self.theor)
        with open("./theory.json",'w') as f:
            f.write(json.dumps(self.theor))
        os.chdir(os.path.dirname(os.getcwd()))
        os.chdir(os.path.dirname(os.getcwd()))
        os.chdir(os.path.dirname(os.getcwd()))
   # def count(self, sentlist):
    #    chCount = 0
        #for ch in sentlist:
    def process(self):
        dirs = os.listdir("./Data/Input/")
        
        for (d,i) in zip(dirs,range(1,len(dirs)+1)):
            self.transtotext(d)
            self.preprocess(i)
		
            
            
        
        
        
                
if __name__ == "__main__":
	
    tp = TextProc()
    tp.process()
    
    
  