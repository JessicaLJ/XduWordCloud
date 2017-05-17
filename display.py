import json
from os import path,listdir
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, ImageColorGenerator
    
class draw:
    def __init__(self,color = "#FAFAD2",sectionColor = "#EEE8AA"):
        self.color = color
        self.sectionColor = sectionColor

    #画一个模式中所有单词的词云，
    #接受mode['data'],生成的词云所在路径path，和词云模板图片所在路径images,背景色bg作为参数
    #返回一个模式的词云列表
    def drawwordcloud(self,model_num,data,section,bg):
        wordcloudList = []

        for i in range(len(data)):
            freq=data[i]
            #绘制一个词云的mask
            im = Image.new("RGBA",(100,80),"white")
            #根据单词的数量和长度，调整词云的大小
            width = im.width
            for s in freq.keys():
                if width < len(s)*10:
                    width = len(s)*10
            height = len(freq) * 30
            if height<80:
                height = 80
            im = im.resize((width,height),Image.ANTIALIAS)
            drawmask = ImageDraw.Draw(im)
            drawmask.ellipse((0,0,width,height),fill = "black")
            del drawmask

            # read the mask / color image taken from
            alice_coloring = np.array(im)

            #绘制词云，背景色透明
            wc = WordCloud(background_color = None, max_words=2000, mask=alice_coloring,
                                max_font_size=40,random_state=42, 
                               prefer_horizontal = 1, mode = "RGBA")
            wc.generate_from_frequencies(freq)
        
            # create coloring from image
            image_colors = ImageColorGenerator(alice_coloring)
            wc.recolor(color_func=image_colors)
            img1=wc.to_image()

            #生成每个词云的圆形背景
            ellipse = Image.new("RGBA",(width,height),self.sectionColor)
            #ellipse = Image.open("./data/images/mask/circle.png")
            draw = ImageDraw.Draw(ellipse)
            draw.ellipse((0,0,width,height),fill = bg)
            del draw
            #将词云和背景组合在一起
            r,g,b,a = img1.split()
            ellipse.paste(img1,(0,0),mask = a)
            wordcloudList.append(ellipse)

        #返回一个模式的词云列表  
        return wordcloudList

    #将单词拼接成句子
    #接受模式号mode_num(从1开始),文章部分名k为参数
    #返回一个模式图片
    def image_joint(self, model_num, section):
        #每个模式词云的颜色随机生成
        bgword = ["#87CEEB","#DDA0DD","#EE82EE","#FFFF00","#90EE90",
                  "#B0C4DE","#9ACD32"]
        bg = bgword[random.randint(0,len(bgword)-1)]
        
        with open("./data/json/%s/model_%s.json" % (section,model_num)) as f:
            mode = json.load(f)
        #获得每个模式的词云列表
        imageList = self.drawwordcloud(model_num,mode["data"],section,bg)
        
        
        width = [] #一个模式中各个图片的宽度列表
        height = [] #一个模式中各个图片的高度列表
        for im in imageList:
            width.append(im.width)
            height.append(im.height)

        #把词云拼接成一个模式
        new_img = Image.new("RGB",(sum(width)+(len(width)-1)*10,max(height)),self.sectionColor)

        draw = ImageDraw.Draw(new_img)
        #拼接起始点
        x = 0
        for i in range(len(imageList)):
            y = int((max(height) - height[i])/2)           
            new_img.paste(imageList[i],(x,y))
            x = width[i] + x + 10
        #绘制中间连线
        x = 0
        for i in range(len(imageList)):
            y = int((max(height) - height[i])/2)           
            draw.line((x+width[i]-2,y+height[i]/2,x+width[i]+12,y+height[i]/2),fill = bg,width = 10)
            x = width[i] + x + 10
        del draw
        return new_img



    #给图片的4个角加椭圆
    def circle_corder_image(self,im):
        rad = 20  # 设置半径 
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im


    #将模式组合成文章段落  
    #接受模式数目num，文章段落名k作为参数
    #返回段落图片
    def pastemode(self,num,section):


        imageList = []
        totalWidth = []
        totalHeight = []
        for i in range(num):
            with open("./data/json/%s/model_%s.json" % (section,str(i+1))) as f:
                mode= json.load(f)
            img = self.image_joint(i+1, section)
            imageList.append(img)
            totalWidth.append(imageList[i].width)
            totalHeight.append(imageList[i].height)
                
        im = Image.new("RGBA",
                        (max(totalWidth) + 20,sum(totalHeight)+len(imageList)*15+20),self.sectionColor)
        y = 20
        for i in range(num):
            x = (max(totalWidth) - totalWidth[i]) // 2 + 10
            im.paste(imageList[i],(x,y))
            y = y + imageList[i].height + 15
        im = self.circle_corder_image(im)
        return im


    #绘制文章
    def drawpaper(self):

        #读取partition文件，获得论文段落信息
        file = open("./data/Output/partition.txt","r")
        line = file.readline().split('\n')[0]
        partition = []
        while line:
            partition.append(line)
            line = file.readline().split('\n')[0]
        file.close()    
        #for i in range(len(partition)-1):
         #   temp = partition[i];
          #  temp = temp[:len(temp)-1]
            #partition[i] = temp

        #获取每个段落的图片
        imageList = []
        for k in partition:
            modelList = listdir("./data/json/%s" % k)
            imageList.append(self.pastemode(len(modelList),k))

 
        #获取每个段落图片信息
        totalWidth = []
        totalHeight = []
        for img in imageList:
            totalWidth.append(img.width)
            totalHeight.append(img.height)

        #将多个段落拼接成文章  
        im = Image.new("RGBA",
                        (max(totalWidth)+80,sum(totalHeight)+len(imageList)*150+300),self.color)
        #设置文章标题字体
        ft = ImageFont.truetype("C:\\Windows\\Fonts\\seguihis.ttf",80)
        #设置文章段落标题字体
        ftt = ImageFont.truetype("C:\\Windows\\Fonts\\seguihis.ttf",50)
        
        draw = ImageDraw.Draw(im)
        draw.text((int(max(totalWidth)/2)-80,20), "Paper", font = ft, fill = "black")
        y = 200
        for i in range(len(imageList)):
            draw = ImageDraw.Draw(im)
            draw.text((int(max(totalWidth)/2)-80,y), partition[i], font = ftt, fill = "#8B4513")
            temp = imageList[i]
            temp = temp.resize((max(totalWidth),temp.height),Image.ANTIALIAS)
            r,g,b,a = temp.split()
            im.paste(temp,(40,y+100), mask = a)
            y = y + imageList[i].height + 120

        im.save("./data/images/result.png" , quality = 95)
       

