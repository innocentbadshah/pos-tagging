tags = {"ADV":0,
"ART":1,
"UNC":2,
"PRON":3,
"SUBST":4,
"VERB":5,
"INTERJ":6,
"CONJ":7,
"ADJ":8,
"PREP":9,
"":10
}

N = 11
confusion_matrix = [ [ 0 for i in range(N) ] for j in range(N) ]



import os
from natsort import natsorted
import xml.etree.ElementTree as ET
from multiprocessing import Pool
from time import time

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


l = [line.rstrip('\n') for line in open(PROJECT_DIR+"/generated_files/outfreq.txt",'r+' ,encoding='utf-8')]

correct = 0
incorrect = 0
wordtag = {}
wordprob = {}

for i in range(0,len(l)):
        l[i] = l[i].rsplit(":",1)
        l[i][0] = l[i][0][1:-1]
        
        l[i][0] = l[i][0].rsplit("_",1)
        l[i][1] = int(l[i][1])

for word in l:
    if word[0][0] not in wordprob:
        wordprob[(word[0][0])] = word[1]
        wordtag[(word[0][0])] = word[0][1]
    elif wordprob[(word[0][0])] < word[1]:
        wordprob[(word[0][0])] = word[1]
        wordtag[(word[0][0])] = word[0][1]



def process_file(file_name):
    global correct
    global incorrect
    
    #opening the xml file
    tree = ET.parse(DATA_DIR+file_name)
    
    #fetching the root tag of read xml file
    root = tree.getroot()
    
    #fetching all the word tags inside root
    strings = root.iter('w')
    
    #empty processed sting to store words in word_POS format
    processed_string = ''
    
    #iterating over found word tags
    for item in strings:
        word = item.text
        word = str(bytes(word,'utf-8'))[2:-1]
        pos_tag = item.attrib['pos']
        gussed_tag = wordtag[(word.strip())]
        confusion_matrix[tags[pos_tag]][tags[gussed_tag]] += 1
    
    

DATA_DIR = PROJECT_DIR+'/files/testdata/'

NUM_PROCESSES = 1
all_filenames = natsorted(os.listdir(DATA_DIR))

all_filenames = [file for file in all_filenames if '.xml' in file]


start = time()
#pool = Pool(NUM_PROCESSES)
#pool.map(process_file, all_filenames)
for fi in all_filenames:
    process_file(fi)
time_taken = time() - start

for i in range(0,10):
    sum = 0
    for j in range(0,11):
        sum = sum+confusion_matrix[i][j]
    for j in range(0,11):
        confusion_matrix[i][j] = confusion_matrix[i][j]/sum

print(confusion_matrix)


