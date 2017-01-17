import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from scipy.stats.stats import pearsonr
from scipy import stats
 
data = web.DataReader("^gspc", data_source='yahoo', start='1960-01-01', 
          end='1989-12-31')['Open','High','Low','Close']
 
data['OC'] = abs(data.Open - data.Close)
data['HL'] = abs(data.High - data.Low)
data['Ratio'] = data.OC/data.HL
data['Loss'] = (data.Close/data.Open - 1)*100  # daily loss in percent
 
events = data[(data.Ratio > 0.95)  & (data.Loss < 0)]
print(events.shape[0])

pr, pvalue = pearsonr(events.Loss.values, events.Volume.values)
slope, intercept, r_value, p_value, std_e = stats.linregress(events.Loss.values,
                                                  events.Volume.values)
 
print(pr, pvalue)           
print(r_value**2, p_value)  

plt.figure(num=1, figsize=(13, 6))
plt.plot(events.Loss, events.Volume, 'ro')
x = np.linspace(-100, 0, 100)
y = slope*x + intercept
plt.plot(x, y, 'k:')
plt.xlim([np.min(events.Loss), np.max(events.Loss)])
plt.ylim([np.min(events.Volume), np.max(events.Volume)])
plt.xlabel('Daily Loss [%]')
plt.ylabel('Volume')
plt.show()
 
plt.savefig('fig01.png', format='png')

del data, events
 
data = web.DataReader("^gspc", data_source='yahoo', start='2000-01-01', 
                        end='2016-03-01')['Open','High','Low','Close']
 
data['OC'] = abs(data.Open - data.Close)
data['HL'] = abs(data.High - data.Low)
data['Ratio'] = data.OC/data.HL
data['Loss'] = (data.Close/data.Open - 1)*100
 
events = data[(data.Ratio > 0.95)  & (data.Loss < 0)]
print(events.shape[0])

ev1 = events[(events.index.year >= 2000) & (events.index.year <= 2002)]
ev2 = events[(events.index.year >= 2007) & (events.index.year <= 2008)]
 
plt.figure(num=2, figsize=(13, 6))
plt.scatter(100*events.HF, events.Loss, c='black', edgecolors='black', s=50)
plt.scatter(100*ev1.HF, ev1.Loss, c='red', edgecolors='red', s=50)
plt.scatter(100*ev2.HF, ev2.Loss, c='yellow', edgecolors='yellow', s=50)
plt.legend(['2000-2016', '2000-2002', '2007-2008'], loc=4)
plt.xlim([0, 25])
plt.ylim([-10, 1])
 
plt.xlabel('Human Factor [%]')
plt.ylabel('Daily Loss [%]')
plt.show()
 
plt.savefig('fig02.png', format='png')

# Detecting Human Fear in Electronic Trading
# (c) 2016 Pawel Lachowicz, QuantAtRisk.com
