#file that writes to mini_indexes
import os

def addToInvIndex(counterID, stems):
        #counterID = URLid of document that was just parsed
        #CHANGED FORMAT OF STEMS:
        #stems: dict({stem of word: [frequency, if bold = 1; 0 if not, if title = 1 if not not empty})
        try:
                os.mkdir("mini_indexes")
                print("mini_index directory created")
        except FileExistsError:
                pass
        
        for pair in stems:
                try:
                        int(pair[0])
                        # NUMBERS in file numbers.txt
                        f = open("mini_indexes/numbers.txt", "a+")
                        #CHANGE THIS: for yerline, add \r before \n
                        f.write(f'{pair} -> ({counterID} {stems.get(pair)})\n')
                        
                except ValueError:
                        # LETTERS in file LETTER.txt "a.txt, b.txt, ..."
                        #print(str(pair[0])+".txt")
                        path_dir: str = "mini_indexes/"+str(pair[0])+".txt"
                        f = open(path_dir, "a+")
                        #CHANGE THIS: for yerline, add \r before \n
                        f.write(f'{pair} -> ({counterID} {stems.get(pair)})\n')
