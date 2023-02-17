import re
from random import choice
import sys
# -*- coding: utf-8 -*-

# ------------------ names generator ------------------
# This program generates names (or words) based on a statistical (n-gram) approach.
# It uses existing words as a source to generate from; remember, the more the merrier!
# The file containing the source words must contain one word per line. It must be saved as ASCII or utf-8.
#
# USAGE: 
# this program prints statistically generated names to the console interface.
# It takes 4 arguments: <source_file> <n of n-gram> <save_file> <number>
# <n of n-gram>: nb of letters to take in the n-grams (default is 2)
# <source_file>: contains the list of names (or words) you want to generate new words from. The file must contain one word per line.
# <save_file>: (optional) the file where you want to save the generated names. New names are appended to the file (so no data is lost). 
#              If you don't provide a file name, the program won't save the generated names
# <number>: (optional) the number of names you want to generate. Defaults to 20 if the argument is not provided.


#takes a file with one word per line, converts it into a list of words        
def file_tolist(inf):
    txt=""
    with open(inf,'r') as f:
        txt=f.read()
    return txt.split()

#retrieves all possible n-grams (nb_letters) from a list of single words
def getkeys(names,nb_letters=2):
    #_LL... (word start)
    #...LL_ (word end)
    keys=set()
    for name in names:
        l=len(name)
        if(l<nb_letters):
            continue
        #debut + fin
        beginning = " " + name[0:nb_letters-1]
        end = name[len(name)-nb_letters+1:] + " "

        keys.update([beginning])
        keys.update([end])
        for i in range(0,l - nb_letters):
            key = name[i:i+nb_letters]
            keys.update([key])
    return keys

# generates the general dictionary structure
# keys = all possible n-grams
# values = another dictionary. Its keys are the letters found after the current trigram in the given names,
# values are how many times this letter appears after the current trigram. They'll be used as weights later.
def ngrams_dico(names,nb_letters=2):
    keys = getkeys(names,nb_letters)
    dico=dict()
    for name in names:
        name=' '+name+' '
        for ngram in keys:
            if ngram in name:
                #place = the letter after the n-gram
                place = name.find(ngram)+len(ngram)
                letter=' '
                if(place<len(name)):
                    letter = name[place]
                if(ngram in dico.keys()):
                    if(letter in dico[ngram]):
                        dico[ngram][letter] = dico[ngram][letter]+1
                    else:
                        dico[ngram][letter] = 1
                else:
                    dico[ngram] = dict()
                    dico[ngram][letter]=1
    return dico

#for printing our dictionary structure       
def print_subdico(dico):
    for k in dico.keys():
        print(k+": "+str(dico[k]))
        
#ngram_dico = one n-gram's dict
#selects one random letter from the subdictionary, following the distribution given by the weights.
def select_random(ngram_dico):
    n = sum([ngram_dico[k] for k in ngram_dico.keys()]) #sum of of each letter's number of apparitions 
    
    s=0
    keyvals=dict()
    for k in ngram_dico.keys():
        s=s+ngram_dico[k]
        keyvals[k] = s
    
    c = choice(range(1,n+1))
    for k in keyvals.keys():
        if(c<=keyvals[k]):
            return k
    return None

#randomly generates a name using nameslist as source
def generate_name(nameslist,nb_letters=2):
    dico = ngrams_dico(nameslist,nb_letters)
    firsts = [x for x in list(dico.keys()) if x[0]==' ']
    name = choice(firsts)
    nextchar = select_random(dico[name])
    while(nextchar!=' '):
        name=name+nextchar
        l=len(name)
        gram = name[l-nb_letters:]
        if(gram not in dico.keys()):
            return name
        nextchar = select_random(dico[gram])
    name = name.replace(' ','')
    return name

#randomly generates a name using nameslist as source, ensures it doesn't exist in the list
def generate_new_name(nameslist,nb_letters=2):
    name = generate_name(nameslist,nb_letters)
    while(name in nameslist):
        name = generate_name(nameslist,nb_letters)
    return name.replace(' ','')

#randomly generates several names using nameslist as source, ensures they don't exist in the list
#saves the generated names in savefile (<- appends the names to it)
def generate_many(allnames, nb, nb_letters=2,savefile=''):
    for i in range(0,nb):
        n=generate_new_name(allnames,nb_letters)
        print(n)
        if(savefile!=''):
            with open(savefile,'a+') as f:
                f.write(n+'\n')

#wrapper for generate_many(), needs the source file instead of the names list               
def generate(source_file, nb_letters=2, save_file='', nb=10):
    allnames = file_tolist(source_file)
    generate_many(allnames,nb,nb_letters,save_file)
    
#CL interface  
def main():
    if(len(sys.argv)<2):
        print("USAGE: this program prints randomly generated names to the console interface.")
        print("It takes 4 arguments: <source_file> <n of n-gram> <save_file> <number>\n")
        print("<n of n-gram>: nb of letters to take in the n-grams (default is 2)")
        print("<source_file>: contains the list of names (or words) you want to generate new words from. The file must contain one word per line.\n")
        print("<save_file>: (optional) the file where you want to save the generated names. New names are appended to the file (so no data is lost). If you don't provide a file name, the program won't save the generated names\n")
        print("<number>: (optional) the number of names you want to generate. Defaults to 20 if the argument is not provided.")
    else:
        source = sys.argv[1]
        save = ''
        nb=20
        nb_letters = 2
        if(len(sys.argv)>2):
            nb_letters = int(sys.argv[2])
        if(len(sys.argv)>3):
            save = sys.argv[3]
        if(len(sys.argv)>4):
            nb = int(sys.argv[4])
        generate(source,nb_letters,save,nb)
    
            

if __name__ == "__main__":
    main()