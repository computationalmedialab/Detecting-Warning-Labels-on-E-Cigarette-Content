
with open('cleaned_img_text.csv', 'r') as f:
    data = f.read().split('\n')

out = open('uniq_text.csv','w')

lst = []
for line in data:
    if len(line) > 0:
        name, rest = line.split('.mp4')
        time, text = rest.split('.jpg,')
        label = f'{name}#{text}'
        if label not in lst:
            out.write(line+'\n')
            lst.append(label)
out.close()

