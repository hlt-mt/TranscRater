import sys
import numpy as np

def load_lex(lexfile):
    lexdict = {}
    f = open(lexfile)
    for line in f:
        line_tok = line.strip().split()
        lexdict[line_tok[0]] = ' '.join(line_tok[1:])
    f.close()
    return lexdict

def load_phonecat(phonecatfile):
    phonecat = {}
    f = open(phonecatfile)
    for line in f:
        line_tok = line.strip().split()
        phonecat[line_tok[0]] = line_tok[1]
    f.close()
    return phonecat

lexfile = sys.argv[1]
phonecatfile = sys.argv[2]

lexfeat = {}

lexdict = load_lex( lexfile )
phonecat = load_phonecat ( phonecatfile )

f = open( lexfile )
for line in f:
    feat = []
    word = line.strip().split()[0]
    wordpro = lexdict[ word ]
    feat += [lexdict.values().count(wordpro)] # Number of homophones
    
    lexical_neighbors = 0
    tmp_pro = '.*'+'.*'.join(wordpro)+'.*'
    for pros in lexdict.values():
        try:
            tmp = re.search(tmp_pro, pros).group()
            if len(tmp) == len(wordpro)+1 or len(tmp) == len(wordpro)-1:
                lexical_neighbors += 1
        except:
            continue
    feat += [lexical_neighbors] # Number of Lexical Neighbors    

    phonecat_feats = [0, 0, 0, 0, 0, 0]
    for phoneme in wordpro.strip().split():
        if phoneme in phonecat.values():
            if phonecat[phoneme] == 'Fricative':
                phonecat_feats[0] += 1
            elif phonecat[phoneme] == 'Liquid':
                phonecat_feats[1] += 1
            elif phonecat[phoneme] == 'Nasal':
                phonecat_feats[2] += 1
            elif phonecat[phoneme] == 'Stop':
                phonecat_feats[3] += 1
            else:               # else, it is Vowel
                phonecat_feats[4] += 1
        else:
            phonecat_feats[5] += 1

    feat += phonecat_feats

    
    print word, 
    for ft in feat:
        print str(ft),
    print ""

f.close()
        


    
        
