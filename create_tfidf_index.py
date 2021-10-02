import re
from collections import defaultdict
import time
import math


def create_tfidf_file():
    '''creates FullIndex file that contains (DOCID, TFIDF) values for postings'''
    # 1. Open FullIndex.txt
    #CHANGE THIS
    fullindex = open("FullIndex.txt", 'r') # <- Brenda
    #fullindex = open("FullIndex.txt", 'rb')  # <- Yerline

    # 2. Open FullIndex_WithTFIDF.txt
    tfidf_fullindex = open("FullIndex_WithTFIDF.txt", 'a+')

    # 3. Go through each line and do the following:
    for line in fullindex:
            # 4. Split line on ">" where the result is in the format of the result = 
            # ["token", "int(freq of token in corpus)", "[('DOCid', '[Frequency_In_Doc,If_Bold,If_Title,If h1]'), (...)]"]
            #CHANGE THIS:
            split_line = line.split(">") # <- Brenda
            #split_line = line.decode('utf-8').split(">") #<- Yerline

            # 5.Evaluate/Load the Postings List aka eval(split_line[2])
            PostingsList = eval(split_line[2])

            # 6.    Store length of Postings List 
            PList_length = len(PostingsList)

            # 7.    idf = math.log(36061/(length of postings list))
            idf = math.log(36163 / PList_length)

            # 8.    tfidf_postings = []
            tfidf_postings = []

            # 9.    For each Posting where the format is ('DOCid', '[freq, if_bold, if_title, if_header]')
            for posting in PostingsList:

                    # if (number of times term appeared in doc which is Posting[1][0])) != 0:
                    p_info = eval(posting[1]) #p_info = Posting[1] = list of information of posting
                    if p_info[0] != 0:

                            # 10. tf = 1 + math.log(number of times term appeared in doc which is Posting[1][0])
                            tf = 1 + math.log(p_info[0])

                            #CHECK IF THERE ARE ANY TITLES:
                            # if Posting[1][2] == 1: #(if the title value is 1)
                            if p_info[2] == 1:
                                    #tf = tf + (tf/4) #(add 25%)
                                    tf = tf * 2 #MIGHT HAVE ISSUES HERE BC OF LONGS/INTS/ETC

                            #CHECK FOR HEADINGS
                            #if Posting[1][3] == 1: #(if the heading value is 1)
                            if p_info[3] == 1:
                                    #tf = tf + ((tf/10)*2) #(add 20%)
                                    tf = tf + ((tf/10)*2) #MIGHT HAVE ISSUES HERE BC OF LONGS/INTS/ETC

                            #CHECK FOR BOLD
                            #if Posting[1][1] == 1: #(if the bold value is 1)
                            if p_info[1] == 1:
                                    #tf = tf + (tf * 0.15) #(add 15%)
                                    tf = tf + (tf * 0.15) #MIGHT HAVE ISSUES HERE BC OF LONGS/INTS/ETC

                            # 11. tfidf_postings.append((DOCid which is Posting[0], tf*idf))
                            tfidf_postings.append((posting[0], tf*idf)) #MIGHT HAVE ISSUES HERE BC OF LONGS/INTS/ETC
                    #else:
                    else:
                            tf = 0
            # 12. After going thru the line, write it to the new file so FullIndex_withTFIDF.write(str(tfidf_postings))
            tfidf_fullindex.write(f'{split_line[0]}>{split_line[1]}>{str(tfidf_postings)}\n')

    tfidf_fullindex.close()
    print("Finished populating FullIndex_withTFIDF.txt file")

if __name__ == "__main__":
    create_tfidf_file()
