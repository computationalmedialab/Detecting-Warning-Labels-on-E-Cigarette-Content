import pandas as pd

condition1 = pd.read_csv('condition1.csv')
condition2 = pd.read_csv('condition2.csv')

print('count (condtition1):',len(condition1))
print('count (condtition2):',len(condition2))
print('Total:',len(condition1)+len(condition2))