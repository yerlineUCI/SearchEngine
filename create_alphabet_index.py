import os

def create_alphabet_indexes():
    fullindex = open("FullIndex_withTFIDF.txt", 'r')
    try:
            os.mkdir("alphabet_indexes")
            print("alphabet_index directory created")
    except FileExistsError:
            pass

    prev = "a"
    current = open("alphabet_indexes/a_index.txt", 'a+') # <- SENSITIVE

    for line in fullindex:
        if line[0] != prev:
            current.close()
            prev = line[0]
            path_dir = f'alphabet_indexes/{line[0]}_index.txt' #<- SENSITIVE
            current = open(path_dir, 'a+')
        current.write(line) #<- SENSITIVE

if __name__ == "__main__":
    create_alphabet_indexes()
