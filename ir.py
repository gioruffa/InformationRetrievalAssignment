import argparse
import glob
import os
import pprint
from nltk.stem import PorterStemmer
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import defaultdict



def get_glossaries_files(glossary_folder):
    return glob.glob(os.path.join(glossary_folder, "*_glossary.txt"))


def get_glossaries_dict(glossary_folder):
    to_ret = dict()
    for glossary_file in get_glossaries_files(glossary_folder):
        cat = os.path.split(glossary_file)[-1].split("_")[0]
        to_ret[cat] = {"file":glossary_file}
    return to_ret


def get_raw_glossaries(glossary_folder):
    glossaries_dict = get_glossaries_dict(glossary_folder)
    for category in glossaries_dict.keys():
        glossaries_dict[category]['category'] = category
        with open(glossaries_dict[category]["file"], "r") as infile:
            word_list = []
            for line in infile:
                word_list.append(line.replace("\n", ""))
            glossaries_dict[category]['word_list'] = word_list
    return glossaries_dict


def get_glossaries(glossary_folder):
    """ We are already sure that each line is a single word """
    glossaries_dict = get_raw_glossaries(glossary_folder)
    # stem and uniq
    ps = PorterStemmer()
    for category in glossaries_dict.keys():
        glossaries_dict[category]['word_list'] = \
            list(set(list(map(lambda x: ps.stem(x), glossaries_dict[category]['word_list']))))


    #get the highest minimum number

    min_unique_words = min(
        list(
            map(
                lambda x: len(glossaries_dict[x]['word_list']),
                glossaries_dict.keys()
            )
        )
    )

    pp.pprint("Number of minimum unique words in the glossary: {}".format(min_unique_words))

    #cutting
    for category in glossaries_dict.keys():
        glossaries_dict[category]['word_list'] = glossaries_dict[category]['word_list'][:min_unique_words]

    return glossaries_dict


def preprocess_document(doc_file):
    with open(doc_file, 'r') as infile:
        doc = infile.read()
        stopset = stopwords.words('english')
        stemmer = PorterStemmer()
        tokens = wordpunct_tokenize(doc)
        clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
        final = [stemmer.stem(word) for word in clean]

    return list(set(final))

def get_postings(glossary, corpus):
    postings = defaultdict()
    for doc in corpus:
        for term in doc:
            postings[term] = postings[term] + 1 if term in postings.keys() else 1
    return postings


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--glossaries-folder", type=str, default="glossaries")
    parser.add_argument("-c", "--corpus-folder", type=str, default="corpus")

    args = parser.parse_args()

    #get the glossaries
    glossaries_dict = get_glossaries(args.glossaries_folder)
    pp.pprint(glossaries_dict)

    documents = [
        preprocess_document(document_file) for document_file in glob.glob(os.path.join(args.corpus_folder, "*"))
    ]
    #get the corpus and treat it
    pp.pprint(documents)


    # calculate document frequency for each term of the glossary
    # postings: a defaultdict whose keys are terms of the glossay, and whose
    # corresponding values are the so-called "postings list" for that
    postings_cars = defaultdict(dict)
    postings_fashion = defaultdict(dict)
    postings_pizza = defaultdict(dict)




    #user profiles


    #process the snippet





