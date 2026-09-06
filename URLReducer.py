#!/usr/bin/env python
"""URLReducer.py

Reduce step: sum the counts for each URL and report only those
URLs referenced more than 5 times.

Hadoop guarantees the reducer's input is SORTED BY KEY, so every
line for a given URL arrives in one contiguous run. We accumulate
while the key stays the same and flush the total when it changes.
"""

import sys

THRESHOLD = 5

current_url = None
current_count = 0
url = None


def emit(u, c):
    """Report a URL, but only if it cleared the threshold.

    The test lives HERE, at the point where the count for `u` is
    final and complete. It must never be applied to a partial count
    (e.g. in a combiner): a URL seen 3 times by one mapper and 4
    times by another totals 7 and belongs in the output, but each
    partial count on its own would fail a `> 5` test and the URL
    would disappear entirely.
    """
    if c > THRESHOLD:
        print('%s\t%s' % (u, c))


# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from URLMapper.py
    url, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: url) before it is passed to the reducer
    if current_url == url:
        current_count += count
    else:
        if current_url:
            emit(current_url, current_count)
        current_count = count
        current_url = url

# do not forget to output the last url if needed!
if current_url == url:
    emit(current_url, current_count)
