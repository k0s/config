#!/usr/bin/env python

import os

dictionary = []

def read_dictionary(f):
    for name in f.readlines():
        name = name.strip('\n')
        word = ''.join(name.split()).lower()
        dictionary.append(word)

def is_in(string1, string2):

    string2 = list(string2)

    try:
        for i in string1:
            string2.remove(i)
    except ValueError:
        return None

    return ''.join(string2)

def anagramize(theword, wordlist, level=0):

    if 0:
        print '%s%s : %s' % ('-' * level, theword, wordlist)

    anagrams = []

    # start the search with a new word
    for index in range(len(wordlist)):
        word = wordlist[index]
        subword = is_in(word, theword)
        if subword == '':
            anagrams.append(word)
            continue

        if subword is None:
            continue


        sublist = [ i for i in wordlist[index:]
                    if is_in(i, subword) is not None ]
        subgram = anagramize(subword, sublist, level+1)

        if subgram is not None:
            anagrams += [ ' '.join((word, i)) for i in subgram ]

    if 0:
        print '%s%s returning %s' % ('-' * level, theword, anagrams)

    if anagrams:
        return anagrams
    return None
    
if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-f", dest="filename", help="dictionary to read",
                      default='')
    (options, args) = parser.parse_args()

    if not os.path.exists(options.filename):

        dicts = [ '/home/jhammel/docs/dict.txt',
                  '/usr/share/dict/cracklib-small',
                  '/usr/share/dict/american-english' ]

        for i in dicts:
            if os.path.exists(i):
                options.filename = i
                break
        else:
            print 'Dictionary not found'
            parser.print_help()
            sys.exit(1)

    if not args:
        print 'please provide an anagram'
        sys.exit(0)

    f = file(options.filename, 'r')
    read_dictionary(f)

    # XXX could cleanup
    anagram = ' '.join(args)
    anagram = ''.join(anagram.split()).lower()

    # don't use letter names
    dictionary = [ i for i in dictionary if (len(i) > 1) or i in 'ai' ]

    wordlist = [ i for i in dictionary
                 if i and is_in(i, anagram) is not None ]
    
    anagrams = anagramize(anagram, wordlist)
    
    print '\n'.join(anagrams)
