# Yerline's Version
import re
from collections import defaultdict
from nltk.stem import PorterStemmer
import os
import json
import time
import pickle
from functools import lru_cache

word_index = dict()
ps = PorterStemmer()


def tokenize(phrase) -> list:
        tokens = []
        tokens += re.findall(r"[a-zA-Z0-9]+", phrase.lower())
        return tokens


def and_boolean_search(search):
        query_tokens = tokenize(search)
        global ps
        stemmed_query = []

        loaded_indexes = dict()
        #loaded_indexes is a dict of all the seeking indexes loaded in the format:
        # { 'a': {'aWord': seekingNumber, 'anotherWord': seekingNumber}, 'b': {'banother': seekingNumber} }

        opened_indexes = dict()
        #opened indexes is a dict with the open files corresponding to the indexes needed for the query
        # {'a': (what you get when you do "open('alphabet_index\\a_index.txt'"), 'b': (file descriptor)}

        found_tokens = 0
        docs = defaultdict(list)

        for word in query_tokens:
               stemmed_query.append(ps.stem(word))

        for token in stemmed_query:
                if token[0] not in loaded_indexes:
                        #CHANGE THIS
                        # <- Yerline
                        seeking_path = f'alphabet_seeking_indexes/{token[0]}.pkl'
                        pickle_in = open(seeking_path, 'rb')
                        loaded_indexes[token[0]] = pickle.load(pickle_in)
                        pickle_in.close()

                        index_path = f'alphabet_indexes/{token[0]}_index.txt'
                        opened_indexes[token[0]] = open(index_path, 'r')

                try:  # just in case a token is not in the files

                        opened_indexes[token[0]].seek(
                            loaded_indexes[token[0]][token])
                        found_tokens += 1  # so that we dont waste time

                        line = opened_indexes[token[0]].readline()
                        #CHANGE THIS
                        #split_line = line.split(">")  # <- Brenda
                        split_line = line.split(">")  # <- Yerline"

                        postingsList = split_line[2]
                        PList = eval(postingsList)
                        for post in PList:
                                # post format = [(DOCid, tfidf), (DOCid2, tfidf2) ]
                                # i.e. [('5916', 3.848543), (...)]
                                docs[post[0]].append(post[1])

                except KeyError:
                        print("something is not right.")
                        #print(f'We have never seen this word before: {token}')

        srted = []
        max_length = 0
        tiers = defaultdict(list)
        # i.e. range(3) = [0,1,2] this is to make it go backwards
        for tier in range(len(query_tokens), 0, -1):
                for doc in docs:
                        if len(docs[doc]) == tier:
                                tiers[tier].append(doc)  # 3 being the lowest

        result_count = 0
        for tier in sorted(list(tiers.keys()), reverse=True):
                # sort only tier one, If less than 10 move onto tier 2, etc
                to_sort = []
                if result_count <= 10:
                        for doc in tiers[tier]:
                                result_count += 1
                                to_sort.append((doc, sum(docs[doc])))
                        srted.extend(
                            sorted(to_sort, key=lambda x: x[1], reverse=True))
                        if result_count >= 10:
                                break
                else:
                        break

        urls = open('URLids.txt', 'r')
        pickle_in = open("URLIndex_Full.pkl", 'rb')
        url_seeker = pickle.load(pickle_in)
        pickle_in.close()
        print(url_seeker['2'])
        for i in range(1650, 1700):
                urls.seek(url_seeker[str(i)])
                print(urls.readline())

        if len(srted) >= 10:
                to_show = 10
                print(f'{len(srted)} results')
        elif len(srted) == 0:
                to_show = 0
                print("0 results")
        else:
                to_show = len(srted)
                print(f'{to_show} results')
        returning = []
        for item in range(to_show):  # range(len(srted)):
                print(srted[item])
                print(url_seeker[srted[item][0]])
                urls.seek(url_seeker[srted[item][0]])
                url_line = urls.readline()
                print(url_line)
                splitted = url_line.split()
                print(splitted)
                returning.append(splitted[2])
        return returning


@lru_cache()
def caching(search_term):
        return and_boolean_search(search_term)


def search():  # search_term):
        print("---------------------------------------------------------------\n")
        search_term = input("Enter term(s) to search: ")
        print()
        print("---------------------------------------------------------------\n")

        start_time = time.time()
        results = caching(search_term)
        finish = time.time()
        print(results)
        print()
        print(f'The search engine took:\n\t{finish - start_time} seconds to run')
        print()
        print()
        #caching.cache_clear()


search()
