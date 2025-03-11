import oci
import time
import json

ai_client = oci.ai_language.AIServiceLanguageClient(oci.config.from_file())
#specifying the compartment id here
compartment_id = "ocid1.tenancy.oc1..aaaaaaaaxi45g3u4zzzwaf3izq2jcpi7xrwuhismvvwvm25ohufq3vnkczqq"
#input file
file_path = '/mnt/youtube-project/04-LangDetect/uniq_text.csv'

#read in the file
with open(file_path, 'r') as f:
    data = f.read()
#split the data into lines
lines = data.split('\n')

#batch size is because it doesn't accept more than a certain number of characters for each request
batch_size = 10
output_lst = []
count = 0
text_lst = []
for j in range(1,len(lines)-1,batch_size):
    print(f'processing lines {j} to {j+batch_size-1}')
    documents = []
    for i in range(j,j+batch_size):
        key = f'doc{i}'
        if ',' in lines[i]:
            text = lines[i].split(',')[1]
            #print(key)
            #print(text)
            #print('#######################')

            #language Detection of Input Documents
            doc = oci.ai_language.models.DominantLanguageDocument(key=key, text=text)
            #add the docs to the document list
            documents.append(doc)
            text_lst.append(text)
        else:
            print('reached end point!')
            break
    count += 1
    #we want to stop after 40 requests and sleep for 5 seconds so we dont get server errors!
    if count == 40:
        time.sleep(5)
        count = 0

    batch_detect_dominant_language_details = oci.ai_language.models.BatchDetectDominantLanguageDetails(documents=documents, compartment_id=compartment_id)

    output = ai_client.batch_detect_dominant_language(batch_detect_dominant_language_details)
    output_lst.append(output.data)
    #print(output_lst)

#print(len(data_json_object))
#print(len(text_lst))

with open('extracted_lang_output.txt', 'w') as f:
    f.write(f'{output_lst}')

with open('text.txt','w') as f:
    for line in text_lst:
        f.write(line+'\n')

