import os
from bs4 import BeautifulSoup
import json
import sys
import re
from nltk.stem import PorterStemmer
from collections import defaultdict, Counter
from urllib.parse import urlparse, urldefrag
import inverted_index
import hashlib
import html5lib

URLids = defaultdict(list)
Word_Dictionary = defaultdict(list)
Word_Counter = 0
blacklist = ['document', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style', 'nbsp', 'sup']

def stemming(tokens:list)->dict:
        ''' takes a list of tokens and returns dictionary of format: {stemmed word: frequency count}'''
        # list will have the format: dict({stemmed word: frequency count})
        ps = PorterStemmer()
        stemmed = defaultdict(int)
        global blacklist, Word_Dictionary, Word_Counter
        for word in tokens:
                if word not in blacklist:
                        stemmed[ps.stem(word)] += 1
                        if Word_Dictionary[ps.stem(word.lower())] == []:
                                Word_Counter+=1
                                Word_Dictionary[ps.stem(word.lower())] = int(hashlib.blake2b(ps.stem(word.lower()).encode('utf-8'), digest_size=4).hexdigest(), 16)
        return stemmed


def is_valid(url):
        #checks for links with fragments
        parsed = urlparse(url)
        if parsed.fragment != '':
                return is_valid(urldefrag(url)[0])
        return True

def Title_or_Bold(html):
        pattern = r"<title>(.*?)</title>"
        pattern2 = r"<strong>(.*?)</strong>"
        pattern3 = r"<b>(.*?)</b>"
        pattern4 = r"<h.+?>(.*?)</h.+?>"
        title = re.findall(pattern, html, flags=0)
        bold = re.findall(pattern2, html, flags=0)
        bold += re.findall(pattern3, html, flags=0)
        headings = re.findall(pattern4, html, flags=0)
        # headings += re.findall(pattern4, html, flags=0) Dont need this. We only added to strong b/c there were two keywords
        return (title, bold, headings) # they are in lists

def iterate():
        #iterate through each folder and get the files
        domains = [] #domains in each folder
        counterID = 0 #number of ids we've encountered
        path_dir: str = os.path.join(os.getcwd(), 'DEV')  # < Sensitive
        urlids_file = open("URLids.txt", "a+")

        for domain in os.listdir(path_dir): # adds all the domains to the list
                domains.append(domain)
        
        for webpage in sorted(domains): # loops through all the files for each domain
                print(f'In Webpage: {webpage}')
                for file in os.listdir(path_dir+"/"+str(webpage)):
                                f=open(path_dir+"/"+str(webpage)+"/"+str(file), "r")
                                text = str(f.read())
                                resp = json.loads(text) # load the json to a string
                                if is_valid(resp['url']): 

                                        content = resp["content"]

                                        #getting titles and bolded words 
                                        important_words = Title_or_Bold(content)
                                        #important_words[0] is Title
                                        #important_word[1] is Bold
                                        #important_word[2] is Headers
                                        titles= tokenize(important_words[0])
                                        bolded = tokenize(important_words[1])
                                        headers = tokenize(important_words[2])
                                        tokens = ParseClean(content)

                                        #getting all other text that is not important
                                        all_others = stemming(tokens)
                                        stems = merge_lists_of_tokens(bolded, titles, headers, all_others)
                                        
                                        #simhashing
                                        h = hash_values_together(stems)
                                        Fingerprint = fingerprint(h)
                                        copy = False
                                        for page in URLids:
                                                #if near duplicates or duplicates, mark them as copies
                                                if similarity(URLids[page][1], Fingerprint) >= 31:
                                                       copy = True 
                                        if not copy:
                                                counterID+=1
                                                num_of_words_in_doc = 0

                                                #to get length of doc
                                                for t in stems: 
                                                        num_of_words_in_doc += stems[t][0]

                                                #adding to URLids.txt file 
                                                URLids[resp["url"]] = [counterID, Fingerprint, num_of_words_in_doc]
                                                #writing "URLid -> Actual_URL Document_Length [Title]""
                                                to_write = f'{counterID} -> {resp["url"]} {num_of_words_in_doc} [{important_words[0]}]\n'
                                                urlids_file.write(to_write)

                                                #writing to mini_indexes files
                                                inverted_index.addToInvIndex(counterID, stems) # adding info to index
        urlids_file.close()
                                        
def ParseClean(html)->list:
        # tokenizes content
        soup = BeautifulSoup(html, 'lxml')

        #getting rid of script and style parts of the html
        for items in soup(["script", "style"]):
                items.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        tokens = []
        for words in lines:
                tokens += re.findall(r"[a-zA-Z0-9]+", words.lower())
        return tokens

def tokenize(list_of_items: list)->list:
        tokens = []
        for item in list_of_items:
                tokens.extend( re.findall(r"[a-zA-Z0-9]+", item.lower()))
        return tokens 

def merge_lists_of_tokens(bolded: list, titles: list, headers: list, all_others: dict)->dict:
        '''returns dict of format {stem: [frequency in doc, if bold, if title, if header]}'''
        final = defaultdict(list)
        ps = PorterStemmer()
        global blacklist
        global Word_Dictionary
        global Word_Counter
        
        #adds the frequency as the first element of the values from all the stems
        #frequency
        for stem in all_others:
                final[stem].extend([all_others[stem],0, 0, 0])
        
        for bolded_word in bolded:
                if bolded_word not in blacklist:
                        if bolded_word in final:
                                final[ps.stem(bolded_word)][1] += 1
                        if bolded_word not in final:
                                final[ps.stem(bolded_word)] = [1, 1, 0, 0]
                                if ps.stem(bolded_word) not in Word_Dictionary:
                                        Word_Counter += 1
                                        Word_Dictionary[ps.stem(bolded_word.lower())] = int(hashlib.blake2b(ps.stem(bolded_word.lower()).encode('utf-8'), digest_size=4).hexdigest(), 16)
        
        for title in titles:
                if title not in blacklist:
                        if title in final:
                                final[ps.stem(title)][2] += 1
                        if title not in final:
                                final[ps.stem(title)] = [1,0,1,0]
                                if ps.stem(title) not in Word_Dictionary:
                                        Word_Counter += 1
                                        Word_Dictionary[ps.stem(title.lower())] = int(hashlib.blake2b(
                                                ps.stem(title.lower()).encode('utf-8'), digest_size=4).hexdigest(), 16)
        for heading in headers:
                if heading not in blacklist:
                        if heading in final:
                                if len(final[ps.stem(heading)]) == 4: 
                                        final[ps.stem(heading)][3] +=1
                                else:
                                        final[ps.stem(heading)] = [1, 0, 0, 1]
                        else:
                                final[ps.stem(heading)] = [1, 0, 0, 1]
                                if ps.stem(heading) not in Word_Dictionary:
                                        Word_Counter += 1
                                        Word_Dictionary[ps.stem(heading.lower())] = int(hashlib.blake2b(ps.stem(heading.lower()).encode('utf-8'), digest_size=4).hexdigest(), 16)
        return final
        
                

#SIMHASHING STUFF 
def hash_values_together(Freq_dict:dict)->list:
    ''' Add if one, subtract if 0 '''
    #Freq_dict is a dictionary of format: {Stem: [frequency, if bolded, *opt if title]}
    position = 0
    Final_List_Form =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for digit in Final_List_Form:
        for pair in Freq_dict: 
                # find “Fish” in Word_Dictionary
                global Word_Dictionary
                Hash_value = str('{0:032b}'.format(Word_Dictionary.get(pair)))
                cur_Index = Hash_value[position]

                if cur_Index == '1':
                #add the weight of “Fish” to Final_List_Form[position]
                        Final_List_Form[position] = Final_List_Form[position] + Freq_dict.get(pair)[0]
                else:
                        #subtract the weight of “Fish” to Final_List_Form[position]
                        Final_List_Form[position] = Final_List_Form[position] - Freq_dict.get(pair)[0]
        position+=1
    #pass the list to the fingerprint() func
    return Final_List_Form


def fingerprint (withWeight: list) -> int:
    ''' Final fingerprint after turning it to 1s and 0s'''
    final = ""
    for num in withWeight:
        if (num > 0):
            final+="1"
        else:
            final+="0"
    return final

def similarity(f1, f2):
    ''' takes 2 fingerprint strings and compares each bit'''
    similar = 0
    for bit in range(32):
        if f1[bit] == f2[bit]:
            similar += 1
    return similar

if __name__ == "__main__":
        iterate()
