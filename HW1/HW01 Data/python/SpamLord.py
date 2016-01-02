import sys
import os
import re
import pprint


#my_first_pat = '(\w+)@(\w+).edu'
#my_first_pat = '([\w-]+)\s*(?:@\s*|at\s+|WHERE)\s*([\w-]+[.]?\w*)\s*(?:\.|DOM|dot)\s*(?:edu|EDU|[edu]+)'
my_first_pat = '([\w-]+\.?[\w]+)\s*(?:@\s*|at\s+|WHERE)\s*([\w-]+)\s*(?:[.]?|[dot]{0,3})\s*(\w*)\s*(?:\.|DOM|dot)\s*(?:edu|EDU|[edu]+)'

#<script> obfuscate('stanford.edu','jurafsky'); </script>
obfuscate = '^obfuscate\(\'([\w+])\.edu\',\'(\w+)\'\)$'

number_match = '\+?1?\s*\(?(\d{3})[\)\s-]+(\d{3})[-\s]+(\d{4})'

"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.‰
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        matches = re.findall(my_first_pat,"".join(line.split('-')).replace(';','.'))
        for m in matches:
            #print (m)
            if (m[2] == ''):
                email = '%s@%s.edu' % m[0:2]
            else:
                email = '%s@%s.%s.edu' % m

            res.append((name,'e',email))

        obfuscate_matches = re.findall(obfuscate, line)
        for l in obfuscate_matches:
            print (l)
            email = '%s@%s.edu' % (l[1],l[0])
            res.append((name, 'e', email))

        number_matches = re.findall(number_match, line)
        for n in number_matches:
            number = '%s-%s-%s' % n
            res.append((name, 'p', number))

    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r', encoding='latin1')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r', encoding='latin1')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print ('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print ('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) == 1):
        main('../data/dev', '../data/devGOLD')
    elif (len(sys.argv) == 3):
        main(sys.argv[1],sys.argv[2])
    else:
        print ('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
