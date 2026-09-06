#!/usr/bin/env python
"""URLMapper.py

Map step: read the input documents line by line and emit one
(url, 1) pair for every href="..." link found on the line.

This is the only real difference from the WordCount Mapper.py:
instead of emitting every whitespace-separated token, we emit
only the URLs found inside HTML anchor attributes.
"""

import re
import sys

# href="        -- the literal attribute name, quote included
# ([^"]*)       -- capture group: any run of characters that is NOT a quote
# "             -- the closing quote
#
# [^"] rather than . is important. `.*` is greedy and would match all the
# way to the LAST quote on the line, gluing several links into one token.
# "Not a quote" can only stop at the very next quote, which is what we want.
HREF = re.compile(r'href="([^"]*)"')

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # findall returns every match on the line, not just the first --
    # a single line of Wikipedia HTML often holds many links
    for url in HREF.findall(line):
        # skip the degenerate href="" case
        if not url:
            continue
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for URLReducer.py
        #
        # tab-delimited; the count for a single sighting is 1
        print('%s\t%s' % (url, 1))
