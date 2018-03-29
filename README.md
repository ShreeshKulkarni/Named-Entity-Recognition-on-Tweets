# Named-Entity-Recognition-on-Tweets
Computes the best sequence of named entity tags, given a corpus of annotated tweets.


Description
-----------
Sequence Tagging in NLP can be defined as predicting a sequence of labels, one for each token in the sentence. Named entity recognition (NER) is a great example of this. This project aims at solving two main challenges in sequence tagging problems: feature engineering (feat_gen.py) and inference/tagging (viterbi.py). This project implements Viterbi Algorithm - a dynamic programming algorithm that computes the best sequence and its score, given the start, end, transition and emission scores. After computation, the predicted best tag sequence is obtained by backtracking. The algorithm is described in more detail in viterbi_alg_pseudo.pdf file in the repository.


Input
-----
The data comes from Twitter, with named entities labeled. The files contain a line for each token with its label separated by a whitespace, and with sentences separated by empty lines. The tweets are annotated with their named entities in the BIO format (Beginning of an entity, Inside an entity, Outside of entities). There are 10 entity types and 21 possible classes. The entity types are company, facility, geographical location, movie, music artist, person, product, sports team, TV show, and other.

feat_gen.py needs a list of sentences, where each sentence is represented as a list of words in it. 
viterbi.py takes the following as input:
- Emission scores, an NxL array
- Transition scores (Word_prev -> Word_curr), an LxL array
- Start transition scores (Start -> Word), an Lx1 array
- End transition scores (Word -> End), an Lx1 array
where N is the number of tokens (length of sentence) and L is the number of labels.


Output
------
feat_gen.py prints a list of features, for each word in the input.
viterbi.py returns a tuple (best_score, y) where best_score is the score of the best sequence and y is a size N array of integers representing the best sequence of tags.


Acknowledgements
----------------
The starter code for this project and the lexicon input data files (annotated tweets) were provided as part of CSCI 544:Applied NLP class at USC.
