import pandas as pd

with open('language_score.csv','r') as f:
    data = f.readlines()

text_lst = []
confidence_lst = []
lang_lst = []
for line in data:
    print(line)
    parts = line.split(';')
    if len(parts)>3:
        text = ';'.join(parts[:-2])
    else:
        text = parts[0]
    text_lst.append(text)
    confidence_lst.append(parts[-1])
    lang_lst.append(parts[-2])
df = pd.DataFrame({'text':text_lst,'lang':lang_lst,'confidence':confidence_lst})    


#df = pd.read_csv('language_score.csv',delimiter=';')
print(len(df))
print(len(df.get('text').unique()))
df_unique = df.drop_duplicates(subset='text')
print(len(df_unique))
df_unique.to_csv('unique_lang_score.csv',index=False)

