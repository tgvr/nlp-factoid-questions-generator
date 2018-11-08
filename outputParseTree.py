import os, nltk, sys

def main():
    parser = nltk.parse.corenlp.CoreNLPParser(url='http://localhost:9000')
    t = next(parser.raw_parse(sys.argv[1]))
    print(' '.join(str(t).split()))

if __name__ == "__main__":
    main()
