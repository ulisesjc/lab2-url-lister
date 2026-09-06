USER=$(shell whoami)

##
## Configure the Hadoop classpath for the GCP dataproc enviornment
##

HADOOP_CLASSPATH=$(shell hadoop classpath)

WordCount1.jar: WordCount1.java
	javac -classpath $(HADOOP_CLASSPATH) -d ./ WordCount1.java
	jar cf WordCount1.jar WordCount1*.class	
	-rm -f WordCount1*.class

prepare:
	-hdfs dfs -mkdir input
	curl https://en.wikipedia.org/wiki/Apache_Hadoop > /tmp/input.txt
	hdfs dfs -put /tmp/input.txt input/file01
	curl https://en.wikipedia.org/wiki/MapReduce > /tmp/input.txt
	hdfs dfs -put /tmp/input.txt input/file02

filesystem:
	-hdfs dfs -mkdir /user
	-hdfs dfs -mkdir /user/$(USER)

run: WordCount1.jar
	-rm -rf output
	hadoop jar WordCount1.jar WordCount1 input output


##
## You may need to change the path for this depending
## on your Hadoop / java setup
##
HADOOP_V=3.3.6
STREAM_JAR = /usr/local/hadoop-$(HADOOP_V)/share/hadoop/tools/lib/hadoop-streaming-$(HADOOP_V).jar

stream:
	-rm -rf stream-output
	hadoop jar $(STREAM_JAR) \
	-mapper Mapper.py \
	-reducer Reducer.py \
	-file Mapper.py -file Reducer.py \
	-input input -output stream-output

##
## UrlCount -- Hadoop Streaming (Python) version
##

## Fetch the two Wikipedia articles into a LOCAL input/ directory
## (no HDFS). Used by the `localtest` rule below.
localprepare:
	mkdir -p input
	curl -sL https://en.wikipedia.org/wiki/Apache_Hadoop > input/file01
	curl -sL https://en.wikipedia.org/wiki/MapReduce > input/file02

## Simulate the whole Map/Reduce pipeline with Unix pipes -- `sort`
## stands in for Hadoop's shuffle. No Hadoop or HDFS required, so
## this is the fast edit-debug loop.
localtest:
	cat input/file01 input/file02 | python3 URLMapper.py | sort | python3 URLReducer.py

## The real thing: run UrlCount on Hadoop via the streaming API.
urlstream:
	-hdfs dfs -rm -r url-output
	hadoop jar $(STREAM_JAR) \
	-mapper URLMapper.py \
	-reducer URLReducer.py \
	-file URLMapper.py -file URLReducer.py \
	-input input -output url-output

## Show the results after `make urlstream`
urloutput:
	hdfs dfs -cat url-output/part-*
