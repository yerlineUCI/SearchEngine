import re
from collections import defaultdict
from nltk.stem import PorterStemmer
import os
import json
import time
import pickle


#CHANGE THIS -- everytime you create a new index as well 
#Brenda:
seeking_index = {'a': 0, 'b': 4801658, 'c': 7495102, 'd': 12705053, 'e': 15819781, 'f': 18784570, 'g': 21594438, 'h': 23272686, 'i': 25293025, 'j': 28673733, 'k': 29512457, 'l': 30216001, 'm': 32275751, 'n': 35668567, 'o': 37554401, 'p': 39805133, 'q': 44645761, 'r': 44917689, 's': 47454465, 't': 53342322, 'u': 57399837, 'v': 58875641, 'w': 59910680, 'x': 62132953, 'y': 62247607, 'z': 62649861, '0': 62909980, '1': 64901289, '2': 71989904, '3': 75984737, '4': 78195568, '5': 80153397, '6': 82024148, '7': 83510547, '8': 85045377, '9': 86337952}
word_index = dict()
#Yerline:
#seeking_index = {97: 0, 98: 4819521, 99: 7528726, 100: 12763100, 101: 15892301, 102: 18874819, 103: 21695727, 104: 23386459, 105: 25418632, 106: 28808495, 107: 29652333, 108: 30364033, 109: 32434235, 110: 35846779, 111: 37742775, 112: 40001013, 113: 44871154, 114: 45144478, 115: 47693820, 116: 53612419, 117: 57684407, 118: 59167040, 119: 60206878, 120: 62436907, 121: 62552900, 122: 62957123, 48: 63220750, 49: 65250711, 50: 72436611, 51: 76479113, 52: 78726776, 53: 80716846, 54: 82615867, 55: 84129979, 56: 85695661, 57: 87009889}

def load_seeking_index(file_path):
        with open(file_path, 'rb') as handle: 
                global word_index
                word_index = pickle.load(handle)

def Check_Positions(words)->bool:
        for parts in words:
                if '\"' in parts:
                        return True
                else:
                        return False

def tokenize(phrase) -> list:
        tokens = []
        tokens += re.findall(r"[a-zA-Z0-9]+", phrase.lower())
        return tokens

def and_boolean_search(search):
        query_tokens = tokenize(search)
        ps = PorterStemmer()
        stemmed_query = []
        Intersecting = defaultdict(list)
        for word in query_tokens:
               stemmed_query.append(ps.stem(word))
        #CHANGE THIS
        fullindex = open("FullIndex.txt", 'r') #<- Brenda
        #fullindex = open("FullIndex.txt", 'rb') #<- Yerline
        for token in stemmed_query:
                #CHANGE THIS
                fullindex.seek(seeking_index[token[0]]) #<- Brenda
                #fullindex.seek(seeking_index[ord(token[0])]) #<- Yerline
                
                for line in fullindex: #for finding term in the fullindex
                        #CHANGE THIS (get rid of the decode part)
                        split_line = line.split(">") #<- Brenda
                        #split_line = line.decode('utf-8').split() #<- Yerline
                        if (split_line[0]==token):
                                postingsList = split_line[2]
                                PList = eval(postingsList)
                                for post in PList:
                                        if Intersecting[post[0]] == []:
                                                Intersecting[post[0]] = [int(post[1])]
                                        else:
                                                Intersecting[post[0]].append(int(post[1]))
        had_all = []
        for values in Intersecting:
                if len(Intersecting[values]) == len(stemmed_query):
                        had_all.append((values, sum(Intersecting[values])))
        srted = sorted(had_all, key = lambda x: x[1], reverse = True)
        urls = open('URLids.txt', 'r')
        
        if len(srted) >= 10:
                to_show = 10
                print(f'{len(srted)} results')
        elif len(srted) == 0:
                to_show = 0
                print("0 results")
        else:
                to_show = len(srted)
                print(f'{to_show} results')
        for item in range(to_show):#range(len(srted)):
                for line in urls:
                        splitted = line.split()
                        if splitted[0] == srted[item][0]:
                                #print(splitted)
                                print(splitted[2], srted[item][1])
                                print()
                urls.seek(0)


        #add postings list to postings list
        fullindex.close()

def calc_tf(token):
        #CHANGE THIS
        fullindex = open("FullIndex.txt", 'r')  # <- Brenda
        #fullindex = open("FullIndex.txt", 'rb') #<- Yerline
        fullindex.seek(seeking_index[token[0]])  # <- Brenda
        #fullindex.seek(seeking_index[ord(token[0])]) #<- Yerline

        tf = 0
        for line in fullindex:  # for finding term in the fullindex
                #CHANGE THIS (get rid of the decode part)
                split_line = line.split(">")  # <- Brenda
                #split_line = line.decode('utf-8').split() #<- Yerline

                if (split_line[0] == token):
                        postingsList = ''.join(split_line[3:])
                        PList = eval(postingsList)
                        for post in PList:
                                pass
        return tf


def calc_idf(token):
        return

def calc_tf_idf(token):
        tf = calc_tf(token)
        idf = calc_idf()
        return tf*idf

def search():#search_term):
        # what the user will see (not the final one)
        print("---------------------------------------------------------------\n")
        search_term = input("Enter term(s) to search: ")
        print()
        print("---------------------------------------------------------------\n")
        print("The user inputted: ", search_term)
        start_time = time.time()
        sectioned = search_term.split(' ')
        order_matters = Check_Positions(sectioned)
        if order_matters:
                # they used "" and we should rank based on positioning
                print("it matters")
        else:
                # they didnt use "". Check for positioning AND td-idf
                and_boolean_search(search_term)
                print("The search engine took", time.time() - start_time, "seconds to run")


search()


""" ###################################################
#CHANGE THIS
#for file in os.listdir('DEV\\www_ics_uci_edu'): # <- Yerline
for file in os.listdir('DEV/www_ics_uci_edu'): #<- Brenda
        ###################################################
        #CHANGE THIS
        #f = open('DEV\\www_ics_uci_edu\\'+ file, 'r') #<- Yerline
        f = open('DEV/www_ics_uci_edu/'+ file, 'r') #<- Brenda
        ###################################################
        text = f.read(55)
        if text == '{"url": "https://www.ics.uci.edu/~eppstein/pubs/pubs.ff':
                print(file)
        f.close()
 """
