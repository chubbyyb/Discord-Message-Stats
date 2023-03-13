import csv
import pandas as pd
import time
from collections import Counter
import pickle
import json



def loadbar(iteration, total, prefix='',suffix='',decimals=5,length=200,fill='>'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}& {suffix}', end='\r')
    if iteration == total:
        print()



def filterWords(word_counts):
    path = r'data\english.csv'

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            if(line.strip() in word_counts):
                del word_counts[line.strip()]
    
    with open(r'data\word_counts.pickle', 'wb') as f:
        pickle.dump(word_counts, f)

    # Save the word counts as a JSON file
    with open(r'data\word_counts.json', 'w') as jsonfile:
        json.dump(word_counts, jsonfile)
    



def wordStats():
    path = r'data\concatenated_data.csv'
    sentences = []
    words = []
    n = 0
    j = 0

    df = pd.read_csv(path) 

    # Get the sentences
    for i in df['Contents']:
        sentences.append(i)

    # Get the words
    while n < sentences.__len__():
        words.extend(str(sentences[n]).split())
        n=n+1

    # Clean
    words = [x.lower() for x in words] # lowers shit
    words = [x.strip() for x in words] # strips shit
    wordSet = set(words)  # Unique words

    #total_unique_words = len(wordSet) # Num of unique words
    #unique_words = list(words_set)

    # Count
    word_counts = Counter(words)
    filterWords(word_counts)
