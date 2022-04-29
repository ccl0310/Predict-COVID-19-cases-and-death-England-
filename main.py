import random
import matplotlib.pyplot as plt
from google.colab import files

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length "{length}" bytes'.format(name=fn, length=len(uploaded[fn])))

import pandas as pd
sheet = pd.read_excel(fn)

def case_model(day):
  peep=[] #人數
  pect=[] #病例成長率
  pect_r=0
  max = 0 #病例數極大值
  maxd = 0 #死亡數極大值
  days = []
  for t in range(0,day):
    days.append(t+1) 
  for b in range(0,day):
    pt = (sheet['每日新增病例數'][b]-sheet['每日新增病例數'][b+1])/sheet['每日新增病例數'][b+1] #算出病例成長率(30天)
    pect.append(round(pt*100,1))
  for i in range(0,day):
      peep.append(sheet['每日新增病例數'][i])
  for com1 in range(0,day): #算出病例極大值
    if peep[com1] > max:
      max = peep[com1]
  min = peep[0] #病例成長率極小值
  for com2 in range(0,day):
    if peep[com2] < min:
      min = peep[com2] #算出病例極小值
  for k in range(0,day-1):
    pect_r = pect_r + (round(abs(pect[k]-pect[k+1]),1))
  pect_r = round(pect_r/(k-1),1)
  firnum=peep[day-1]
  firper=pect[0]
  new = []
  newd = []
  count = 0
  countlow = 0
  while count <= day-1:
    if count >= 60:
      newpp = (1+(random.uniform(-pect_r,pect_r)/100)+countlow/100)
      newp = int(firnum*newpp) #預測未來病例數(範圍在max到min間(大約0.85~1.15左右),再將最新一期的病例數乘上成長率)
      newpd = int(newp*random.uniform(0.0007,0.0010))
      if newpp < 1: #新增一個變數"countlow",其目的是讓病例數更精準的關鍵:利用條件子讓病例數不再探底，而是快速竄升。
        countlow = countlow + 1.8
      elif newpp > 1.1:
        if newp > peep[0]*2.5: #製造障礙，不再讓病例數以倍數成長
          countlow = countlow - newpp*2.2
        else:
          countlow = countlow - newpp
      if newp > min:
        if newp > max:
          max = newp
        if newpd > maxd:
          maxd = newpd
        new.append(round(newp,0))
        newd.append(round(newpd,0))
        count = count + 1
        firnum = newp
    else:
      newpp = (1+(random.uniform(-pect_r,pect_r)/100))
      newp = int(firnum*newpp)
      newpd = int(newp*random.uniform(0.0007,0.0015))
      if newp > min:
        new.append(round(newp,0))
        newd.append(round(newpd,0))
        count = count + 1
        firnum = newp
  print("以下是預測",day,"天的病例數")
  print(new)
  print("以下是預測",day,"天的死亡數")
  print(newd)
  plt.figure(figsize=(30,10),dpi=100,linewidth=10)
  plt.plot(days,new,color='#4287f5',label='eng')
  plt.title("Predict of cases",x=0.5,y=1.03)
  plt.xlim([0.5,day+0.5])
  plt.ylim([0,max+5000])
  plt.figure(figsize=(30,10),dpi=100,linewidth=10)
  plt.plot(days,newd,color='black',label='eng')
  plt.title("Predict of deaths",x=0.5,y=1.03)
  plt.xlim([0.5,day+0.5])
  plt.ylim([0,maxd+10])
x = int(input("輸入你要預測的天數 "))
case_model(x)
