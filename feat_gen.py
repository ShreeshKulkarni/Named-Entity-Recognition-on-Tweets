#!/bin/python

def parse_files(files):
    B_SET = set()
    I_SET = set()
    for file in files:
        with open('./data/'+file, 'r') as f:
            for line in f.readlines():
                tokens = line.split()
                if tokens:
                    B_SET.add(tokens[0].lower())
                    del tokens[0]
                    for tok in tokens:
                        I_SET.add(tok.lower())
    # B_SET.update(I_SET)
    # I_SET.clear()
    return B_SET, I_SET


def preprocess_corpus(train_sents):
    """Pre-process annotated tweets and build suitable sets.
	
    Called one-time only at start-up.
    """
	
    global B_COMPANY, I_COMPANY, B_FACILITY, I_FACILITY, B_GEO, I_GEO, B_MOVIE, I_MOVIE, B_MUSIC_ARTIST, I_MUSIC_ARTIST
    global B_PERSON, I_PERSON, B_PROD, I_PROD, B_SPORTSTEAM, I_SPORTSTEAM, B_TVSHOW, I_TVSHOW, OTHER

    B_COMPANY, I_COMPANY = parse_files(['automotive.make','business.brand','business.consumer_company','business.sponsor','cvg.cvg_developer','venture_capital.venture_funded_company'])
    B_FACILITY, I_FACILITY = parse_files(['education.university','government.government_agency','transportation.road','venues'])
    B_GEO, I_GEO = parse_files(['location', 'location.country'])
    B_PERSON, I_PERSON = parse_files(['people.person'])
    B_PROD, I_PROD = parse_files(['automotive.model','business.consumer_product','cvg.computer_videogame','cvg.cvg_platform','product'])
    B_SPORTSTEAM, I_SPORTSTEAM = parse_files(['sports.sports_team','sports.sports_league'])
    B_TVSHOW, I_TVSHOW = parse_files(['tv.tv_program'])

    for file in ['firstname.5k']:
        with open('./data/'+file, 'r') as f:
            for line in f.readlines():
                token = line.strip()
                if token:
                    B_PERSON.add(token.lower())
    for file in ['lastname.5000','people.family_name','people.person.lastnames']:
        with open('./data/'+file, 'r') as f:
            for line in f.readlines():
                token = line.strip()
                if token:
                    I_PERSON.add(token.lower())

    OTHER = set()
    for file in ['english.stop','lower.10000']:
        with open('./data/'+file, 'r') as f:
            for line in f.readlines():
                token = line.strip()
                if token:
                    OTHER.add(token.lower())

    B_MOVIE = set()
    I_MOVIE = set()
    with open('movies', 'r') as f:
        for line in f.readlines():
            tokens = line.split()
            if tokens:
                B_MOVIE.add(tokens[0].lower())
                del tokens[0]
                for tok in tokens:
                    I_MOVIE.add(tok.lower())

    B_MUSIC_ARTIST = set()
    I_MUSIC_ARTIST = set()
    with open('musicartists', 'r') as f:
        for line in f.readlines():
            tokens = line.split()
            if tokens:
                B_MUSIC_ARTIST.add(tokens[0].lower())
                del tokens[0]
                for tok in tokens:
                    I_MUSIC_ARTIST.add(tok.lower())


def token2features(sent, i, add_neighs = True):
    """Compute the features of a token and return a set of strings that represent those features.

    All the features are boolean, i.e. they appear or they do not.
    The token is at position i, and the rest of the sentence is provided as well.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
	
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")

    ##################

    global B_COMPANY, I_COMPANY, B_FACILITY, I_FACILITY, B_GEO, I_GEO, B_MOVIE, I_MOVIE, B_MUSIC_ARTIST, I_MUSIC_ARTIST
    global B_PERSON, I_PERSON, B_PROD, I_PROD, B_SPORTSTEAM, I_SPORTSTEAM, B_TVSHOW, I_TVSHOW, OTHER
    word_lower = word.lower()

    if word_lower in B_COMPANY:
        ftrs.append("IS_B_COMPANY")
   
    if word_lower in I_COMPANY:
        ftrs.append("IS_I_COMPANY")

    if word_lower in B_FACILITY:
        ftrs.append("IS_B_FACILITY")
    if word_lower in I_FACILITY:
        ftrs.append("IS_I_FACILITY")

    if word_lower in B_GEO:
        ftrs.append("IS_B_GEO")
    if word_lower in I_GEO:
        ftrs.append("IS_I_GEO")

    if word_lower in B_PERSON:
        ftrs.append("IS_B_PERSON")
    if word_lower in I_PERSON:
        ftrs.append("IS_I_PERSON")

    if word_lower in B_PROD:
        ftrs.append("IS_B_PROD")
    if word_lower in I_PROD:
        ftrs.append("IS_I_PROD")

    if word_lower in B_SPORTSTEAM:
        ftrs.append("IS_B_SPORTSTEAM")
    if word_lower in I_SPORTSTEAM:
        ftrs.append("IS_I_SPORTSTEAM")

    if word_lower in B_TVSHOW:
        ftrs.append("IS_B_TVSHOW")
    if word_lower in I_TVSHOW:
        ftrs.append("IS_I_TVSHOW")

    if word_lower in B_MOVIE:
        ftrs.append("IS_B_MOVIE")
    if word_lower in I_MOVIE:
        ftrs.append("IS_I_MOVIE")

    if word_lower in B_MUSIC_ARTIST:
        ftrs.append("IS_B_MUSIC_ARTIST")
    if word_lower in I_MUSIC_ARTIST:
        ftrs.append("IS_I_MUSIC_ARTIST")

    if word_lower in OTHER:
        ftrs.append("IS_OTHER")

    ##################

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    return ftrs


if __name__ == "__main__":
    sents = [
    [ "I", "love", "comics" ],
    [ "Nokia", "announces", "a", "new", "launch" ],
    [ "Alexander", "built", "this", "library" ]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
