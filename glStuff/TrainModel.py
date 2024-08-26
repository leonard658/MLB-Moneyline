import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import lightgbm as lgbm
import structureboost as stb
import ml_insights as mli
from structureboost import log_loss

#df22 = pd.read_csv('2022TrainingData.csv')
#df23 = pd.read_csv('2023TrainingData.csv')


#dfComp = pd.concat([df22, df23], axis=0)

#dfComp.to_csv('dfComp.csv', index=False)
x_train = pd.read_csv('train.csv')
x_eval = pd.read_csv('eval.csv')
x_test = pd.read_csv('2021TrainingData.csv')

y_train = x_train.pop('home_win')
y_eval = x_eval.pop('home_win')
y_test = x_test.pop('home_win')



lgbm1 = lgbm.LGBMClassifier(n_estimators=1000, learning_rate=.02, max_depth=3)
lgbm1.fit(x_train, y_train, eval_set=(x_eval, y_eval), eval_metric='logloss', 
          callbacks=[lgbm.early_stopping(stopping_rounds=50), lgbm.log_evaluation(10)])
preds_lgbm = lgbm1.predict_proba(x_test)[:,1]

hv_mean = y_test.sum() / len(y_test)
print(log_loss(y_test, preds_lgbm))
print(log_loss(y_test, hv_mean*np.ones(len(y_test))))


