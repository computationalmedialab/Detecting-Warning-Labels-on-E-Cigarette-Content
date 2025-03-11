
output = open('cleaned_img_text.csv','w')

#read the file
with open('image_text.csv','r') as f:
    data = f.read()

lines = data.split('\n')
#print(len(lines))

for line in lines:
    #print(line)
    parts = line.split(',')
    #print(parts)
    if len(parts) > 1 and len(parts[1]) > 0:
        #print(line)
        output.write(line+'\n')

output.close()

