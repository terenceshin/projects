import streamlit as st
import numpy as np
from scipy.sparse import csr_matrix
import scipy
from numpy import abs
import re
from re import finditer
from math import log
import nltk
from stop_words import get_stop_words
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')

#############################
######### ALGORITHM #########
#############################

# Step 1: Extracting and Separating Sentences
def get_sentences(doc):

    sentence_list = nltk.tokenize.sent_tokenize(doc)

    return sentence_list


# Step 2: Get Bag of Words
# Part A: Cleaning Sentences
def clean(s):

    pattern = r"[a-z]+('[a-z])?[a-z]*"

    return [match.group(0) for match in finditer(pattern, s.lower())]


# Part B: Remove Stop Words and Convert to Root Words
stop_words = get_stop_words('english')
stemmer = SnowballStemmer("english")

def bag_of_words(sentences):
    
    bag_of_words = []
    for sentence in sentences:
        words = clean(sentence)
        
        temp = []
        for word in words:
            if word not in stop_words:
                word = stemmer.stem(word)
                temp.append(word)
        bag_of_words.append(set(temp))
        
    return bag_of_words

# Step 3: Assign scores for each sentence based on word importance
# Part A: Generate IDs for words
def allwords(bags):
    
    all_words = set()
    for bag in bags:
        all_words |= bag
    word_to_id = {w: k for k, w in enumerate(all_words)}
    id_to_word = {k: w for k, w in enumerate(all_words)}
    
    return word_to_id, id_to_word


# Part B: Construct Coordinates for Sparse Matrix and Calculate SVD
def gen_coords(bags, word_to_id):
    m, n = len(word_to_id), len(bags)
    rows, cols, vals = [], [], []
    
    # Construct rows, cols, and vals:
    # Rows:
    for bag in bags:
        for word in bag:
            rows.append(word_to_id[word])
            
    # Columns:
    for bag in bags:
        index = bags.index(bag)
        for word in bag:
            cols.append(index)
            
    # Values:
    all_words = []
    for bag in bags:
        for word in bag:
            all_words.append(word)
    all_words = set(all_words)
    
    word_count = {}
    for word in all_words:
        count = 0
        for bag in bags:
            if word in bag:
                count +=1
        word_count[word] = count
        
    for bag in bags:
        for word in bag:
            ni = word_count[word]
            value = 1/log((n+1)/ni)
            vals.append(value)
        
    # Returns your arrays:
    return rows, cols, vals


def A_matrix(row, col, val, word_to_id, bags):

    A = csr_matrix((val, (row, col)), shape=(len(word_to_id), len(bags)))
    return A


def get_svds_largest(A):
    
    u, s, v = scipy.sparse.linalg.svds(A, k=1, which='LM', return_singular_vectors=True)
    return s, abs(u.reshape(A.shape[0])), abs(v.reshape(A.shape[1]))


# Step 4: Rank Words and Sentences
def rank_words(u0, v0):
    ###
    rank_dict = dict(enumerate(u0, start=0))
    
    final = sorted(rank_dict, key=rank_dict.get, reverse=True)
    final = np.asarray(final)
    return final

def rank_sentences(u0, v0):
    ###
    rank_dict = dict(enumerate(v0, start=0))
    
    final = sorted(rank_dict, key=rank_dict.get, reverse=True)
    final = np.asarray(final)
    return final






