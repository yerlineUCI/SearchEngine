from collections import defaultdict
import os

def merging(directory):
    indexing_file = open("FullIndex.txt", 'a+')
    files = []
    for file in os.listdir(directory):
        files.append(file)
    print(files)
    for file in sorted(files):
        print(file)
        if file != "numbers.txt" and file != ".DS_Store":
            f = open(directory + "/" + str(file), 'r')
            index = defaultdict(list)
            for line in f:
                parsed = line.split()
                #parsed =  "["token", "->", "(DOCid", "[freq,", "if bold,", "if title,", "if heading])"]
                key = parsed[0]
                value = (parsed[2][1:], "".join(parsed[3:])[:-1])
                index[key].append(value)

            for k in sorted(index.keys()):
                frequency = 0
                for posting in index[k]:
                    #posting = (DOCid, [freq, bold, title, heading])
                    frequency += int(eval(posting[1])[0])
                #k = word, frequency = freq in corpus, [Posting list of tuples (docID, freq in doc)]
                indexing_file.write("{}>{}>{}\n".format(k, frequency, str(index[k])))

    f = open(directory + "/numbers.txt", "r")
    index = defaultdict(list)
    for line in f:
        parsed = line.split()
        key = parsed[0]
        value = (parsed[2][1:], "".join(parsed[3:])[:-1])
        index[key].append(value)

    for k in sorted(index.keys()):
        frequency = 0
        for posting in index[k]:
            frequency += int(eval(posting[1])[0])
        indexing_file.write("{}>{}>{}\n".format(k, frequency, str(index[k])))
    
if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'mini_indexes')
    merging(path)
