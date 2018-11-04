import os, nltk, sys
import requests

def main():
    parser = nltk.parse.corenlp.CoreNLPParser(url='http://localhost:9000')
    print(next(
        parser.raw_parse(sys.argv[1])
    ))

if __name__ == "__main__":
    main()
