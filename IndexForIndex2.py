#Yerline's version
#file to create a smaller index to store in memory of the FullIndex to seek() when searching

alphabet_index1 = {'a': 0, 'b': 4801658, 'c': 7495102, 'd': 12705053, 'e': 15819781, 'f': 18784570, 'g': 21594438, 'h': 23272686, 'i': 25293025, 'j': 28673733, 'k': 29512457, 'l': 30216001, 'm': 32275751, 'n': 35668567, 'o': 37554401, 'p': 39805133, 'q': 44645761, 'r': 44917689, 's': 47454465, 't': 53342322, 'u': 57399837, 'v': 58875641, 'w': 59910680, 'x': 62132953, 'y': 62247607, 'z': 62649861, '0': 62909980, '1': 64901289, '2': 71989904, '3': 75984737, '4': 78195568, '5': 80153397, '6': 82024148, '7': 83510547, '8': 85045377, '9': 86337952}

def create_index_for_index(file_path):
    alphabet_index = dict()
    fullindex = open(file_path, 'rb')
    seek_number = 0
    for line in fullindex:
        if line[0] not in alphabet_index:
            #print(line[0])
            alphabet_index[line[0]] = seek_number
        seek_number += len(line)
    
    print(alphabet_index)
    for letter in alphabet_index:
        print(alphabet_index[letter])
        fullindex.seek(alphabet_index[letter])
        print(fullindex.read(20))

    fullindex.close()

create_index_for_index('FullIndex.txt')
