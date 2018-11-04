#!/usr/bin/bash

# java -Xmx2g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

# 3.3.1 - Marking Unmovable Phrases
python ./python/outputParseTree.py "$1" > ./txt/parseTree.txt
./tsurgeon.sh -treeFile ./txt/parseTree.txt ./tsurgeon/3.3.1_mark_unmv > ./txt/3.3.1.txt
