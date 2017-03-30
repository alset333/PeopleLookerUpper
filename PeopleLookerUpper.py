#!/usr/bin/env python3

import Lookup
import Utilities

info = {'name': input('Enter a name:\n')}

lu = Lookup.Lookup(info) # Enters in info

lu.runLookup() # Runs the lookup

res = lu.getResults() # Gets the results

print("lu.getResults():\t", res) # Prints the results

print("Nice display:\n")
for key in res:
    value = res[key]
    mostCommonAnswerInCategory = Utilities.most_common(value)
    print(key, ':\t\t', mostCommonAnswerInCategory)
