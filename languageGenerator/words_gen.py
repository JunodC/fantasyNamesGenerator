import random
import sys

#FILE: vowels consumns max_syllables syllable_patterns
#or syllables list: max word length in syllables then one line = one syllable

#takes a file with one word per line, converts it into a list of words        
def get_info(inf):
    txt=""
    with open(inf,'r') as f:
        txt=f.read()
    info = txt.split()
    return info

def generate_syllable(v,c,patterns):
    pattern = random.choice(patterns)
    s = ''
    for symbol in pattern:
        if symbol=='v':
            s += random.choice(v)
        else:
            s += random.choice(c)
    return s

def generate_word(info):
    v = list(info[0])
    c = list(info[1])
    length = random.randint(1,int(info[2])) 
    patterns = info[3:]
    word = ''
    for i in range(0,length):
        s = generate_syllable(v,c,patterns)
        word += s
    return word



#randomly generates several words using vowels and consumns as source
#saves the generated words in savefiles (<- appends the names to it)
def generate_many(info, nb, savefile=''):
    for i in range(0,nb):
        n=generate_word(info)
        print(n)
        if(savefile!=''):
            with open(savefile,'a+') as f:
                f.write(n+'\n')

#wrapper for generate_many(), needs the source file instead of the info          
def generate(source_file, save_file='', nb=10):
    info = get_info(source_file)
    generate_many(info,nb,save_file)


#CLI interface  
def main():
    if(len(sys.argv)<2):
        print("USAGE: this program prints randomly generated words to the console interface.")
        print("It takes 4 arguments: <source_file> <number> <save_file>\n")
        print("<source_file>: contains the list of vowels then consumns to use for generation\n")
        print("<number>: (optional) the number of words you want to generate. Defaults to 10 if the argument is not provided.")
        print("<save_file>: (optional) the file where you want to save the generated names. New names are appended to the file (so no data is lost). If you don't provide a file name, the program won't save the generated names\n")
    else:
        source = sys.argv[1]
        save = ''
        nb = 10
        ncr = 2
        if(len(sys.argv)>2):
            nb = int(sys.argv[2])
        if(len(sys.argv)>3):
            save = sys.argv[3]
            
        generate(source,save,nb)
    
            

if __name__ == "__main__":
    main()