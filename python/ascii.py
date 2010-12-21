#!/usr/bin/env python 
# extended ascii chart
# 2010 openuniverse
#
# license: cc0 http://creativecommons.org/publicdomain/zero/1.0/

print " " , "0 1 2 3 4 5 6 7 8 9 a b c d e f"
print "0" , " " , u"\u263a", u"\u263b", u"\u2665", 
print u"\u2666", u"\u2663", u"\u2660", u"\u2022", 
print u"\u25d8", u"\u25cb", u"\u25d9", u"\u2642", 
print u"\u2640", u"\u266a", u"\u266b", u"\u263c"

print "1" , u"\u25ba", u"\u25c4", u"\u2195", u"\u203c", 
print u"\u00b6", u"\u00a7", u"\u25ac", u"\u21a8",
print u"\u2191", u"\u2193", u"\u2192", u"\u2190", 
print u"\u221f", u"\u2194", u"\u25b2", u"\u25bc"

x = 1
y = 2
print "2" , 
for p in range(32, 127):
    print chr(p),
    x += 1
    if x > 16: print ; x = 1 ; y += 1 ; print y,

print u"\u2302"

print "8" , u"\u00c7", u"\u00fc", u"\u00e9", u"\u00e2",
print u"\u00e4", u"\u00e0", u"\u00e5", u"\u00e7", 
print u"\u00ea", u"\u00eb", u"\u00e8", u"\u00ef", 
print u"\u00ee", u"\u00ec", u"\u00c4", u"\u00c5" 

print "9" , u"\u00c9", u"\u00e6", u"\u00c6", u"\u00f4", 
print u"\u00f6", u"\u00f2", u"\u00fb", u"\u00f9", 
print u"\u00ff", u"\u00d6", u"\u00dc", u"\u00a2", 
print u"\u00a3", u"\u00a5", u"\u20a7", u"\u0192" 

print "a" , u"\u00e1", u"\u00ed", u"\u00f3", u"\u00fa", 
print u"\u00f1", u"\u00d1", u"\u00aa", u"\u00ba", 
print u"\u00bf", u"\u2310", u"\u00ac", u"\u00bd", 
print u"\u00bc", u"\u00a1", u"\u00ab", u"\u00bb" 

print "b" , u"\u2591", u"\u2592", u"\u2593", u"\u2502", 
print u"\u2524", u"\u2561", u"\u2562", u"\u2556", 
print u"\u2555", u"\u2563", u"\u2551", u"\u2557", 
print u"\u255d", u"\u255c", u"\u255b", u"\u2510" 

print "c" , u"\u2514", u"\u2534", u"\u252c", u"\u251c", 
print u"\u2500", u"\u253c", u"\u255e", u"\u255f", 
print u"\u255a", u"\u2554", u"\u2569", u"\u2566", 
print u"\u2560", u"\u2550", u"\u256c", u"\u2567" 

print "d" , u"\u2568", u"\u2564", u"\u2565", u"\u2559", 
print u"\u2558", u"\u2552", u"\u2553", u"\u256b", 
print u"\u256a", u"\u2518", u"\u250c", u"\u2588", 
print u"\u2584", u"\u258c", u"\u2590", u"\u2580" 

print "e", u"\u03b1", u"\u00df", u"\u0393", u"\u03c0", 
print u"\u03a3", u"\u03c3", u"\u03bc", u"\u03c4", 
print u"\u03a6", u"\u0398", u"\u03a9", u"\u03b4", 
print u"\u221e", u"\u03c6", u"\u03b5", u"\u2229" 

print "f" , u"\u2261", u"\u00b1", u"\u2265", u"\u2264", 
print u"\u2320", u"\u2321", u"\u00f7", u"\u2248", 
print u"\u00b0", u"\u2219", u"\u00b7", u"\u221a", 
print u"\u207f", u"\u00b2", u"\u25a0"