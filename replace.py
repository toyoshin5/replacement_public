import pandas as pd
import random
import time
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm

data = pd.read_csv("students.csv")
stuSum = len(data)
numlist = list(range(stuSum))

#席替え
data['place'] = 0 
for index,item in data.iterrows():
    randP = random.randint(0,len(numlist)-1)#要素番号をランダムで指定
    if item['near-sight']:
        randP = random.randint(0,int(len(numlist)/2-1))#近視の人は前の方から指定
    data.loc[index,'place'] = numlist.pop(randP)

data = data.sort_values(by = 'place',ascending = True)

#コンソール出力
i = 0
print("\n=============================黒板==============================\n")
print("　　　　　　　　　　　　　　 教卓\n")
for index,item in data.iterrows():
    for _ in range(2-len(str(item["席"]))):
        print(" ",end = "")
    print(str(item["席"]) + " " + item["姓"],end = "",flush = True)
    for _ in range(4-len(item["姓"])):
        print("　",end = "")
    
    i += 1    
    time.sleep(1.5)
    if i%6 == 0:
        print("\n")
    
    
#pdf出力
#parameters
pdfW = 29.7*cm
pdfH = 21.0*cm
gap = 0.3*cm
outOfArea = 1.2*cm
columnsn = 6


pdfFile = canvas.Canvas('result.pdf',pagesize=landscape(A4))
pdfFile.saveState()
pdfFile.setAuthor('Toyoshin')
pdfFile.setTitle('席替え')
pdfFile.setSubject('')
pdfFile.setPageSize((pdfW,pdfH))#A4
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
pdfFile.setFont('HeiseiKakuGo-W5',18)

offset = 2*cm
rowsn = int(stuSum/columnsn) + 1
w = (pdfW-(columnsn-1)*gap-2*outOfArea)/columnsn
h = (pdfH-(rowsn-1)*gap-2*outOfArea-offset)/rowsn

pdfFile.setFillColorRGB(0,0,0)
pdfFile.rect(10.2*cm, 0.7*cm, 9.2*cm, 1.9*cm, stroke=1, fill=0)
pdfFile.drawCentredString(14.85*cm, 1.5*cm,'教 卓')
pdfFile.drawString(1*cm, 1*cm,'3I 座席表')

i = 0
for index,item in data.iterrows(): 
    x = pdfW - (outOfArea + w *((i%columnsn) + 1 )+ gap * (i%columnsn)) 
    y = outOfArea + offset + h * int(i/columnsn) + gap * int(i/columnsn)
    if item['sex'] == 'm':
        pdfFile.setFillColorRGB(0.7,1,1)
    elif 'f':
        pdfFile.setFillColorRGB(1,0.8,0.9)
    pdfFile.rect(x, y, w, h, stroke=1, fill=1)
    pdfFile.setFillColorRGB(0,0,0)
    pdfFile.setFont('HeiseiKakuGo-W5',18)
    pdfFile.drawCentredString((x+w/2), (y+h/3),item['姓']+" "+item['名'])
    pdfFile.setFont('HeiseiKakuGo-W5',10)
    pdfFile.drawCentredString(x+0.5*cm, y +0.2*cm,str(item["席"]))
    pdfFile.setFont('HeiseiMin-W3',10)
    pdfFile.drawCentredString((x+w/2), (y+h/3+0.7*cm),item['せい']+" "+item['めい'])
    i+=1

pdfFile.save()