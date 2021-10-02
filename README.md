# SearchEngine for CS class
Project by Yerline Herrera and Brenda Cid. Originally created on Mar 13, 2020 on bcid's github account and reuploaded to yerlineUCI's github. Current UCI students, do not copy our project/code as that is considered plagerism.

## Link to web version: http://yerlineh.pythonanywhere.com/
(Had to make small alterations to code for the web version. Web python files are flask_app.py and processing.py)

## To recreate Indexing files necessary to search: 
- 1. Have DEV/ folder be in the same directory as the parsing_files.py, merging.py, create_tfidf_index.py, create_alphabet_index.py, IndexForIndex.py and inverted_index.py directory
- 2. Run parsing_files.py
- 3. Run merging.py
- 4. Run create_tfidf_index.py
- 5. Run create_alphabet_index.py
- 6. Run IndexForIndex.py on Windows, not Mac

## To search locally: (for Windows)
- 1. Will need python files: IndexForIndex.py, and search_testing.py. 
- 2. These two python files will create the alphabet_seeking_indexes directory, and URLIndex_Full.pkl. These are necessary for making the search run fast and accurately.
- 3. To run the search, run search_testing.py and input any search terms. Have fun (:
