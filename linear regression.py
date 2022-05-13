import random
import numpy as np
import matplotlib.pyplot as plt
import random
from google.colab import files
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length "{length}" bytes'.format(name=fn, length=len(uploaded[fn])))

import pandas as pd
sheet = pd.read_excel(fn)

daily_case = [int(i) for i in sheet['每日確診數']]
daily_death = [int(i) for i in sheet['每日死亡數']]
# plt.scatter(day,daily_case)
# plt.show()
x = sheet['檢核日期'].values.reshape(-1,1)
y = sheet['每日確診數'].values.reshape(-1,1)
model = make_pipeline(PolynomialFeatures(2),linear_model.LinearRegression())
model.fit(x,y)
ppred = []
d = []
lastnum = 33954
s = []
for i in range(125,215):
    x_pred = [[i]]
    y_pred = model.predict(x_pred)
    d.append(i)
    ppred.append(y_pred)
    x = np.append(x,x_pred)
    x = x.reshape(-1,1)
    y = np.append(y,random.uniform(y_pred-(lastnum*0.3),y_pred+(lastnum*0.4)))
    y = y.reshape(-1,1)
    model.fit(x,y)
    lastnum = y_pred
for i in ppred:
    s.append(int(i))
plt.scatter(x,y)
plt.show()
plt.plot(d,s,color='#4287f5',label='eng')
plt.show()
