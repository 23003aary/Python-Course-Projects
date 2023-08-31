
'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Returns the cosine between two dicitionaries vec1 and vec2.
    Converts vec1 and vec2 into lists'''
    vec1value = [*vec1.values()]
    vec2value = [*vec2.values()]
    vec1key = [*vec1.keys()] 
    vec2key = [*vec2.keys()]
    num = 0
    dem = norm(vec1) * norm(vec2)
    for i in range(len(vec1key)):
        for j in range(len(vec2key)):
            if vec1key[i] == vec2key[j]:
                num += vec1value[i] * vec2value[j]
    return num/dem

def build_semantic_descriptors(sentences):
    '''Returns dictionary d, by taking a list of lists sentences. 
    Returns the wordz in the list of lists and any corresponding word'''

    d = {}
    for i in sentences:
        wordz = []
        for j in i:
            if j not in wordz:
                wordz.append(j)
        for k in wordz:
            if k not in d:
                d[k] = {}
            for l in wordz:
                if k != l:
                    if l not in d[k]:
                        d[k][l] = 0
                    d[k][l] += 1
    return d


def build_semantic_descriptors_from_files(filenames):
    '''Returns an altered file. Files are taken in and punctuation is replaced with space or  '.' delimeters
    to allow for build_semantic_descriptors to run'''
    sentences = []
    for i in range(len(filenames)):
        store = []
        filez = open(filenames[i], "r", encoding = "latin1").read().lower()
        filez = filez.replace("?", ".")
        filez = filez.replace("!", ".")
        filez = filez.replace("\n"," ")
        filez = filez.replace(",", " ")
        filez = filez.replace(";", " ")
        filez = filez.replace(":", " ")
        filez = filez.replace("-", " ")
        filez = filez.replace("<", " ")
        filez = filez.replace(">", " ")
        filez = filez.replace("---", " ")
        filez = filez.replace("--", " ")
        newfilez = filez.split(".")
        for i in newfilez:
            store.append(i.split())
        sentences += store
    return build_semantic_descriptors(sentences)

   
def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''Returns a list containing words with most similarity'''
    data = []
    if word not in semantic_descriptors:
        return -1
    for choice in choices:
        if choice not in semantic_descriptors:
            data.append(-1)
            continue
        data.append(similarity_fn(semantic_descriptors[word], semantic_descriptors[choice]))

    return choices[data.index(max(data))]
  

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''Returns percentage of correct_gueses to total made by most_similar-word'''
    file = open(filename, encoding="latin1").read().split("\n")
    test_choices = []
    correct_gueses = 0
    total = 0
    for i in range(len(file)-1):
        if i != " ":
            test_choices.append(file[i].split(" "))
    for j in test_choices:
        if j[1] == most_similar_word(j[0], j[2:], semantic_descriptors, similarity_fn):
            correct_gueses += 1
        total += 1
    return (correct_gueses/total)*100





