#!/usr/bin/python
#
#   Authors: Giorgio Ruffa - Federico Ungolo
#

import os
import glob
from collections import defaultdict
import pprint
import argparse
import codecs
import pandas as pd
import numpy as np

from nltk.corpus import stopwords
from gensim import corpora, models, similarities
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer


def clean_raw_doc(raw_doc):
    stopwordslist = stopwords.words('english')
    tokens = wordpunct_tokenize(raw_doc)
    cleaned_tokens = list(map(lambda x: x.lower(), tokens))
    cleaned_tokens = [token for token in cleaned_tokens if token not in stopwordslist and len(token) > 2]
    stemmer = PorterStemmer()
    cleaned_tokens = list(map(lambda x: stemmer.stem(x), cleaned_tokens))
    return cleaned_tokens


def get_doc_category(doc_name):
    if 'p' in doc_name:
        return "pizza"
    if 'f' in doc_name:
        return "fashion"
    if 'm' in doc_name:
        return "cars"


def load_raw_corpus(corpus_folder):
    corpus_list = []
    for filename in glob.glob(os.path.join(corpus_folder, "*")):
        with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as infile:
            to_insert = defaultdict()
            to_insert['filename'] = os.path.split(filename)[1]
            to_insert['category'] = get_doc_category(to_insert['filename'])
            to_insert['raw_content'] = infile.read()
            corpus_list.append(to_insert)
    return corpus_list


def clean_raw_corpus(loaded_corpus):
    for doc in loaded_corpus:
        doc['cleaned_content'] = clean_raw_doc(doc['raw_content'])
    return loaded_corpus


def generate_user_profiles(num_users = 5):
    fashion = np.random.randint(2, size=num_users)
    cars = np.random.randint(2, size=num_users)
    pizza = np.random.randint(2, size=num_users)
    to_ret = pd.DataFrame(data={"fashion":fashion, "cars":cars, "pizza":pizza})
    to_ret.index.name = "users"
    return to_ret


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corpus-folder", type=str, default="corpus")
    parser.add_argument("snippet_content", type=str, help="content of the incoming document, enclosed by \"\"")

    args = parser.parse_args()

    print("Generating user profiles")
    user_profiles_df = generate_user_profiles()
    print("Users profiles are:")
    print(user_profiles_df)

    print()
    print("The text snippet is: ")
    pp.pprint(args.snippet_content)

    print()

    raw_corpus = load_raw_corpus(args.corpus_folder)
    cleaned_corpus = clean_raw_corpus(raw_corpus)

    # pp.pprint(cleaned_corpus)

    # get a dictionary to calculate the vector representation more easily
    dictionary = corpora.Dictionary(list(map(lambda x: x['cleaned_content'], cleaned_corpus)))

    # calculate the vector representation
    corpus_vectors = list(map(
        lambda x: dictionary.doc2bow(x['cleaned_content']),
        cleaned_corpus
    ))

    # vectors with term frequencies, the coordinates are ids, created by the dictionary
    # pp.pprint(corpus_vectors)

    tfidf_model = models.TfidfModel(corpus_vectors, dictionary=dictionary)

    # pp.pprint(tfidf_model)
    # for further explanations see this tutorial https://radimrehurek.com/gensim/tutorial.html
    # calculate proximity with cosine
    index = similarities.SparseMatrixSimilarity(corpus_vectors, num_features=len(dictionary))

    # time to get the query vector treated
    query_vector = dictionary.doc2bow(
        clean_raw_doc(args.snippet_content)
    )
    query_tfidf = tfidf_model[query_vector]  # compute the tfid of the query vector
    # pp.pprint(query_tfidf)
    sim = index[query_tfidf]
    # pp.pprint(sim)
    ranked_docs = sorted(enumerate(sim), key=lambda x: x[1], reverse=True)
    # pp.pprint(ranked_docs[:5])

    # the closest doc will get us the category to which te query belongs
    closest_doc = cleaned_corpus[ranked_docs[0][0]]

    print(
        "The closest document to the text snippet belongs to the category \"{}\" and its content is:".format(
            closest_doc['category']
        )
    )
    pp.pprint(closest_doc['raw_content'])

    # get the users interested in the category
    interested_users = user_profiles_df[user_profiles_df[closest_doc['category']] == 1].index.values
    print()
    print("The user id interested in the topic {} are: {}".format(closest_doc['category'], interested_users))




