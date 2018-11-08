#!/usr/bin/bash

# 3.3.1 - Marking Unmovable Phrases
python ./outputParseTree.py "$1" > ./txt/parseTree.txt
./tsurgeon.sh -s -treeFile ./txt/parseTree.txt ./tsurgeon/3.3.1_mark_unmv > ./txt/3.3.1.txt

# 3.3.3 - Verb Decomposition
./tsurgeon.sh -s -treeFile ./txt/3.3.1.txt ./tsurgeon/3.3.3_verb_d > ./txt/3.3.3.txt

# 3.3.2 - Identifying Answer Phrases and generate corresponding question phrases
python ./questionGenerator.py "$1"
