import json
import csv
from os import listdir
from os.path import isfile, join
base_dir = 'data'
list_files = [f for f in listdir(base_dir) if isfile(join(base_dir,f))]
list_scores = []
for f in list_files:
    with open(join(base_dir,f)) as open_file:
        list_articles = json.load(open_file)
        acc = 0
        count = 0
        for a in list_articles:
            score = a['score']
            if score != 0:
                acc += score
                count+=1
        if count != 0:
            avg_score = acc/count
        else:
            avg_score = 0
        list_scores.append([f.split(".")[0],str(avg_score)])

def cmp(a):
    return a[0]
list_scores.sort(key=cmp)
with open(join(base_dir,'scores.csv'),'w') as o:
    writer = csv.writer(o, delimiter=',')
    for s in list_scores:
        writer.writerow(s)

'''            
ifile = open('test.csv', "rb")
reader = csv.reader(ifile)
ofile = open('ttest.csv', "wb")
writer = csv.writer(ofile, delimiter='', quotechar='"', quoting=csv.QUOTE_ALL)

for row in reader:
    writer.writerow(row)
'''