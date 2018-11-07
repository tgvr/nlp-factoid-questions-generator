import os, nltk, sys, re
import spacy

def find_noun_phrases(tree):
    return [subtree for subtree in tree.subtrees(lambda t: t.label()=='NP')]

def find_head_of_np(np):
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    top_level_trees = [np[i] for i in range(len(np)) if type(np[i]) is nltk.tree.Tree]
    ## search for a top-level noun
    top_level_nouns = [t for t in top_level_trees if t.label() in noun_tags]
    if len(top_level_nouns) > 0:
        ## if you find some, pick the rightmost one, just 'cause
        return top_level_nouns[-1][0]
    else:
        ## search for a top-level np
        top_level_nps = [t for t in top_level_trees if t.label()=='NP']
        if len(top_level_nps) > 0:
            ## if you find some, pick the head of the rightmost one, just 'cause
            return find_head_of_np(top_level_nps[-1])
        else:
            ## search for any noun
            nouns = [p[0] for p in np.pos() if p[1] in noun_tags]
            if len(nouns) > 0:
                ## if you find some, pick the rightmost one, just 'cause
                return nouns[-1]
            else:
                ## return the rightmost word, just 'cause
                return np.leaves()[-1]

def getQuestionPhraseNP(t, d, t_full):
    head = find_head_of_np(t)
    personalPronouns = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours',
                        'you', 'your', 'yours', 'he', 'she', 'it', 'him', 'her',
                        'his', 'hers', 'its', 'they', 'them', 'their', 'theirs']
    locationPOS = ['LOC', 'GPE', 'FAC']
    timePOS = ['DATE', 'TIME']
    numberPOS = ['CD', 'QP']

    try:
        d[head]
    except KeyError:
        d[head] = -1

    # where
    if (d[head] in locationPOS):
        return 'Where'
    # when
    if ((d[head] in timePOS) or (re.match(r"[1|2]\d\d\d", head))):
        return 'When'

    # whose NP
    head_pos = t_full.leaf_treeposition(t_full.leaves().index(head))
    temp = list(head_pos[:-2])
    temp.append(head_pos[-2]+1)
    head_pos_right_sibling = tuple(temp)

    temp = []
    for pos in t.pos():
        if len(pos) == 1 and pos != 0:
            temp.extend(t[pos].leaves())
    mod_NP = " ".join(temp).strip('.').rstrip()

    try:
        if (d[head] == 'PERSON' and t_full[head_pos_right_sibling].label() == 'POS'):
            return 'Whose ' + mod_NP
    except IndexError:
        pass

    # who
    if (d[head] == 'PERSON' or head.lower() in personalPronouns):
        return 'Who'

    # how many NP
    if t[0].label() in numberPOS:
        temp = []
        for pos in t.pos():
            if len(pos) == 1 and pos != 0:
                temp.extend(t[pos].leaves())
        a = " ".join(temp).strip('.').rstrip()
        return 'How many ' + a

    # what
    return 'What'

def main():
    with open('txt/3.3.1.txt') as fp:
        line = fp.readline()
    t = nltk.tree.Tree.fromstring(line)

    with open('txt/parseTree.txt') as fp:
        line = fp.readline()
    t0 = nltk.tree.Tree.fromstring(line)

    height = t.height()
    length_flag = -1
    answerPhraseList = []
    questionPhraseList = []
    answerPhrasePOS = ['NP', 'PP', 'SBAR']

    # Identify Answer Phrases
    for pos in t.treepositions():
        if length_flag != -1:
            if len(pos) == length_flag:
                length_flag = -1
        if length_flag == -1 and not isinstance(t[pos], str):
            if t[pos].label() in answerPhrasePOS:
                answerPhraseList.append(pos)
                length_flag = len(pos)

    nlp = spacy.load('en')
    doc = nlp(sys.argv[1])
    d = dict([(X.text, X.label_) for X in doc.ents])

    # Generate Question Phrases
    for pos in answerPhraseList:
        if (t[pos].label() == 'SBAR'):
            questionPhraseList.append('What')
        elif (t[pos].label() == 'PP'):
            # assuming PP --> prep NP
            prepositions = ['on', 'in', 'at', 'over', 'to']
            if (t0[pos][0].leaves()[0].lower() in prepositions):
                questionPhraseList.append(getQuestionPhraseNP(t0[pos][1], d, t0))
            else:
                questionPhraseList.append(-1)
        elif (t[pos].label() == 'NP'):
            questionPhraseList.append(getQuestionPhraseNP(t0[pos], d, t0))

    # for i in range(0, len(answerPhraseList)):
    #     print('****************')
    #     print(t0[answerPhraseList[i]].leaves())
    #     print(questionPhraseList[i])
    #     print('****************')

if __name__ == "__main__":
    main()
