#!/usr/bin/env python

loldict = { 'am': 'is',
            'and': 'n',
            'are': 'r',
            'ate': 'eated',
            'back': 'bak',
            'business': 'bizness',
            'bye': 'bai',
            'cat': 'kitteh',
            'cheeseburger': 'cheezburger',
            'cute': 'kyooot',
            'food': 'foodz',
            'fucking': 'fuxing',
            'have': 'has',
            'help': 'halp',
            'hi': 'hai',
            'is': 'iz',
            'kitty': 'kitteh',
            'later': 'l8r',
            'making': 'makin',
            'means': 'meens',
            'more': 'moar',
            'news': 'newz',
            'please': 'plz',
            'power': 'powr',
            'saturday': 'caturday',
            'says': 'sez',
            'takes': 'takez',
            'thanks': 'kthx',
            'time': 'tiem',
            'the': 'teh',
            'there': 'thar',
            'this': 'dis',
            'towel': 'towul',
            'uses': 'uzes',
            'young': 'yung',
            'your': 'ur'
            }

def translate(string):
    retval = []
    for word in string.split():
        retval.append(loldict.get(word.lower(), word))
    return ' '.join(retval)

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        print translate(' '.join(sys.argv[1:]))
    else:
        print translate(sys.stdin.read())

