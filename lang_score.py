import json

with open('extracted_lang_output.txt','r') as f:
    output_lst = f.read()

with open('text.txt','r') as f:
    text_lst = f.read().split('\n')

#write to the file
f = open('language_score.csv','w')

data_json_object = json.loads(str(output_lst))
#getting the name of the language and the confidence (0.7) from the server response

count = 0
threshold = 0.9
for i in range(len(data_json_object)):
    line = data_json_object[i]
    documents = line.get('documents')
    errors = line.get('errors')
    if len(errors) > 0:
        print('We have an error: ', errors)
    for doc in documents:
        key = doc.get('key')
        languages = doc.get('languages')
        langs_lst = []
        scores_lst = []
        for lang in languages:
            if lang.get('score') > threshold:
                langs_lst.append(lang.get('name'))
                scores_lst.append(lang.get('score'))
            else:
                count += 1
        if len(langs_lst)==0:
            print('bad text',text_lst[i])
        else:
            f.write(f'{text_lst[i]};{langs_lst};{scores_lst}\n')
f.close()

