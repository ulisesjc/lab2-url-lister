# Lab 2 Solution — UrlCount

Ulises Cortez

Solution description: My solution uses the `re` module in Python with the pattern
`href="([^"]*)"` to filter URLs out of the data. So instead of writing every token
like `Mapper.py` does, I only write URLs. The reducer is about the same as
`Reducer.py`, except it sums the counts and only prints a URL if the count is
greater than 5. I used the Hadoop streaming API instead of the Java version, so
the mapper and reducer are `URLMapper.py` and `URLReducer.py`.

The software required to run this is: Python 3, Apache Hadoop 3.3.6, and GNU make.
On dataproc the streaming jar is at `/usr/lib/hadoop/hadoop-streaming.jar`, not the
path in the original Makefile, so I pass it in:
`make urlstream STREAM_JAR=/usr/lib/hadoop/hadoop-streaming.jar`


My output looks like this:
```
#	18
https://en.wikipedia.org/wiki/Doi_(identifier)	18
https://en.wikipedia.org/wiki/Google_File_System	6
https://en.wikipedia.org/wiki/ISBN_(identifier)	18
https://en.wikipedia.org/wiki/MapReduce	6
https://en.wikipedia.org/wiki/S2CID_(identifier)	14
mw-data:TemplateStyles:r1295599781	33
mw-data:TemplateStyles:r1333133064	7
mw-data:TemplateStyles:r1333433106	121
mw-data:TemplateStyles:r886049734	12
```

There were 1973 distinct URLs total and only 10 of them showed up more than 5
times, so almost all of them appear exactly once. I got the same numbers running it
locally with `cat input/* | python3 URLMapper.py | sort | python3 URLReducer.py`,
which is how I debugged it.

When I run it on Google Cloud dataproc and time it, I get these results:

1 master 2 workers:
real    0m56.704s
user    0m14.234s
sys     0m0.837s

1 master 4 workers:
real    1m3.803s
user    0m13.228s
sys     0m0.640s
