# nlp-factoid-questions-generator
Generating Factoid Questions from a given paragraph or article.

Done as part of NLP course - Monsoon 2018, IIIT Hyderabad.

[Link](https://docs.google.com/document/d/1GSFHxmLH9VXH5g0yR-dPrzgSuAMRdOC25foZHiI6rcs/edit?usp=sharing) to the primary details about this project.

**Update**: Completed Question Generation Part of this project.

Instructions:
- Download and install StanfordCoreNLP.
- Install wordnet with ```nltk.download('wordnet')``` in your python shell.
- Also download and install spacy along with its English language model.

```
(from corenlp folder)
java -Xmx2g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

(from this repo)
bash main.sh "---sentence---"
```

Example:
```
bash main.sh "I saw an eagle"

OUTPUT:
Did I saw an eagle?
Did I see an eagle?
Who saw an eagle?
What did I saw?
What did I see?

bash main.sh "Peter is studying in NY"

OUTPUT:
Is Peter studying in NY?
Who is studying in NY?
Where is Peter studying?

bash main.sh "I have made a huge mistake"

OUTPUT:
Have I made a huge mistake?
Who has made a huge mistake?
What have I made?
```

Note that in the first example, questions 1 and 4 have 'saw' as verb because they consider 'saw' in the sentence to be the act of 'sawing' and not past form of 'see'.
