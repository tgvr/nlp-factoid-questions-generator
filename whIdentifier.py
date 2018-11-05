import os, nltk, sys

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk

def NERTagging():
    st = nltk.tag.StanfordNERTagger('english.all.3class.distsim.crf.ser.gz',
                                    'stanford-ner.jar',
                                    encoding='utf-8')
    tagged_sent = st.tag(sys.argv[1].split())

    named_entities = get_continuous_chunks(tagged_sent)
    named_entities_str_tag_3class = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

    st = nltk.tag.StanfordNERTagger('english.conll.4class.distsim.crf.ser.gz',
                                    'stanford-ner.jar',
                                    encoding='utf-8')
    tagged_sent = st.tag(sys.argv[1].split())

    named_entities = get_continuous_chunks(tagged_sent)
    named_entities_str_tag_4class = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

    st = nltk.tag.StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz',
                                    'stanford-ner.jar',
                                    encoding='utf-8')
    tagged_sent = st.tag(sys.argv[1].split())

    named_entities = get_continuous_chunks(tagged_sent)
    named_entities_str_tag_7class = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

    d3 = dict(named_entities_str_tag_3class)
    d4 = dict(named_entities_str_tag_4class)
    d7 = dict(named_entities_str_tag_7class)

    return d3, d4, d7

def getQuestionPhraseNP():
    pass

def main():
    # d3, d4, d7 = NERTagging()
    with open('txt/3.3.1.txt') as fp:
        line = fp.readline()
    t = nltk.tree.Tree.fromstring(line)

    height = t.height()
    length_flag = -1
    answerPhraseList = []
    questionPhraseList = []

    # Identify Answer Phrases
    for pos in t.treepositions():
        if length_flag != -1:
            if len(pos) == length_flag:
                length_flag = -1
        if length_flag == -1 and not isinstance(t[pos], str):
            if t[pos].label() == ('NP' or 'PP' or 'SBAR'):
                answerPhraseList.append(pos)
                length_flag = len(pos)

    # for pos in answerPhraseList:
    #     print('***************')
    #     print(t[pos])
    #     print('***************')

    # Generate Question Phrases
    for pos in answerPhraseList:
        if (t[pos].label() == 'SBAR'):
            questionPhraseList.append('What')
        elif (t[pos].label() == 'PP'):
            # assuming PP --> prep NP
            questionPhraseList.append(getQuestionPhraseNP(t[pos][1]))
        elif (t[pos].label() == 'NP'):
            questionPhraseList.append(getQuestionPhraseNP(t[pos]))


if __name__ == "__main__":
    main()
