import os, nltk, sys, re
import spacy
import copy

def find_noun_phrases(tree):
    return [subtree for subtree in tree.subtrees(lambda t: t.label()=='NP')]

def find_head_of_np(np):
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    top_level_trees = [np[i] for i in range(len(np)) if type(np[i]) is nltk.tree.Tree]
    top_level_nouns = [t for t in top_level_trees if t.label() in noun_tags]
    if len(top_level_nouns) > 0:
        return top_level_nouns[-1][0]
    else:
        top_level_nps = [t for t in top_level_trees if t.label()=='NP']
        if len(top_level_nps) > 0:
            return find_head_of_np(top_level_nps[-1])
        else:
            nouns = [p[0] for p in np.pos() if p[1] in noun_tags]
            if len(nouns) > 0:
                return nouns[-1]
            else:
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

    with open('txt/3.3.3.txt') as fp:
        line = fp.readline()
    vd_tree = nltk.tree.Tree.fromstring(line)

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

    # DEBUG CODE - START
    # for i in range(0, len(answerPhraseList)):
    #     print(t0[answerPhraseList[i]].leaves())
    #     print(questionPhraseList[i])
    # DEBUG CODE - END

    main_verb_pos = -1
    verb_decomposition_flag = 0
    for pos in vd_tree.treepositions():
        if (not isinstance(vd_tree[pos], str)) and vd_tree[pos].label() == 'mainvp':
            main_verb_pos = pos
            break

    vt = copy.deepcopy(t0)
    vt_list = []
    if main_verb_pos != -1:
        # Verb Decomposition
        new_verb_list = nltk.corpus.wordnet._morphy(t0[main_verb_pos][0,0], pos='v')
        if t0[main_verb_pos][0].label() == 'VBD':
            aux_verb = 'did'
        elif t0[main_verb_pos][0].label() == 'VBZ':
            aux_verb = 'does'
        else:
            aux_verb = 'do'
        vt[main_verb_pos].insert(0, nltk.tree.Tree(t0[main_verb_pos][0].label(), [aux_verb]))
        for i in range(0, len(new_verb_list)):
            vt[main_verb_pos][1,0] = new_verb_list[i]
            vt_list.append(copy.deepcopy(vt))
        verb_decomposition_flag = 1
    else:
        vt_list.append(vt)
        main_verb_pos_list = []
        for pos in t.treepositions():
            if (not isinstance(t[pos], str)) and t[pos].label() == 'VP':
                main_verb_pos_list.append(pos)
        main_verb_pos_list.sort(key = len)
        main_verb_pos = main_verb_pos_list[0]

    # DEBUG CODE - START
    # for item in vt_list:
    #     print(item)
    # DEBUG CODE - END

    questionList = []

    # Generating Yes/No Questions
    for item in vt_list:
        yn = copy.deepcopy(item)
        temp = yn[main_verb_pos][0,0]
        yn[main_verb_pos].remove(yn[main_verb_pos][0])
        question = temp.capitalize() + ' ' + " ".join(yn.leaves()).rstrip() + '?'
        questionList.append(question)

    # Generating other Questions
    for i in range(0, len(answerPhraseList)):
        # Generating Questions whose Answer Phrases are in subject.
        if t0.treepositions().index(answerPhraseList[i]) < t0.treepositions().index(main_verb_pos):
            yn = copy.deepcopy(t0)
            yn[answerPhraseList[i]].remove(yn[answerPhraseList[i]][0])
            temp2 = yn.leaves()
            # Some hardcoded corrections
            if questionPhraseList[i] == 'Who' and temp2[0] == 'have':
                temp2[0] = 'has'
            question = questionPhraseList[i] + ' ' + " ".join(temp2).rstrip() + '?'
            questionList.append(question)

        # Generating Questions whose Answer Phrases are not in subject.
        else:
            for item in vt_list:
                yn = copy.deepcopy(item)
                temp = yn[main_verb_pos][0,0]
                yn[main_verb_pos].remove(yn[main_verb_pos][0])
                temp2 = list(answerPhraseList[i])
                temp2 = temp2[:-1]
                if verb_decomposition_flag == 0:
                    temp2[len(main_verb_pos)] = temp2[len(main_verb_pos)]-1
                temp2 = tuple(temp2)
                temp3 = list(answerPhraseList[i])
                if verb_decomposition_flag == 0:
                    temp3[len(main_verb_pos)] = temp3[len(main_verb_pos)]-1
                temp3 = tuple(temp3)
                yn[temp2].remove(yn[temp3])
                # Some hardcoded corrections
                if questionPhraseList[i] == 'Who' and temp == 'have':
                    temp = 'has'
                question = questionPhraseList[i] + ' ' + temp + ' ' + " ".join(yn.leaves()).rstrip() + '?'
                questionList.append(question)

    for question in questionList:
        print(question)

if __name__ == "__main__":
    main()
