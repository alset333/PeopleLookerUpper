# http://stackoverflow.com/a/1520716

from __future__ import print_function
import itertools
import operator
import sys

def most_common(L):
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print 'SL:', SL
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    # auxiliary function to get "quality" for an item
    def _auxfun(g):
      item, iterable = g
      count = 0
      min_index = len(L)
      for _, where in iterable:
        count += 1
        min_index = min(min_index, where)
      # print 'item %r, count %r, minind %r' % (item, count, min_index)
      return count, -min_index
    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def percentEncode(startingText):
    encodedText = startingText
    et = encodedText

    et = et.replace(' ', '%20')
    et = et.replace(',', '%2C')

    encodedText = et
    return encodedText