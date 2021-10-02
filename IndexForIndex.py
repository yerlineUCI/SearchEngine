#file to create an .pkl index for the indices to store in memory of the 
#to seek() when searching for URLids.txt and for alphabet_indexes directory

import pickle
import time
import os

def create_small_file_indexes():
    '''creates alphabet_seeking_indexes directory where seeking indexes 
    for the alphabet_indexes are stored'''
    domains = []
    word_index = dict()

    try:
        os.mkdir("alphabet_seeking_indexes")
        print("alphabet_seeking_index directory created")
    except FileExistsError:
        pass

    domain_path_dir: str = os.path.join(os.getcwd(), 'alphabet_indexes')  # < Sensitive
    for domain in os.listdir(domain_path_dir):
            domains.append(domain)

    for domain in domains:
        print(f"in domain: {domain}")
        #path_dir: str = "alphabet_seeking_indexes\\" + str(domain[0])+".pkl"  # <- Yerline
        path_dir: str = "alphabet_seeking_indexes/" + str(domain[0])+".pkl"  # <- Brenda
        indexer = open(path_dir, 'wb+')
        letter_index_dir = f"alphabet_indexes/{domain}" # <- Brenda
        letter_index = open(letter_index_dir, 'r')
        word_index = dict()
        seek_number = 0
        for line in letter_index:
            parsed = line.split(">") # <- Brenda
            word_index[parsed[0]] = seek_number
            seek_number += len(line)
        pickle.dump(word_index, indexer, protocol=pickle.HIGHEST_PROTOCOL)
        indexer.close()
        word_index = dict()

def create_urlids_seeking_file():
    '''creates URLids_Full.pkl pickle file for URLids.txt file'''
    #urlindex = open("URLids.txt", 'rb')
    urlindex = open("URLids.txt", 'r')
    url_index = dict()

    seek_number = 0
    for line in urlindex:
        #CHANGE THIS
        parsed = line.strip().split() # <- Brenda
        #parsed = line.decode('utf-8').split()  # <- Yerline
        url_index[parsed[0]] = seek_number
        seek_number += len(line)
    urlindex.close()

    #writing dictionary to pickle file to load later
    indexer = open("URLIndex_Full.pkl", 'wb+')
    # highest protocol saves space
    pickle.dump(url_index, indexer, protocol=pickle.HIGHEST_PROTOCOL)
    indexer.close()

create_small_file_indexes()
create_urlids_seeking_file()
