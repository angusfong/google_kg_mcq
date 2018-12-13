import nltk
from nltk.tag.stanford import StanfordPOSTagger

# generate a question that asks the property of entity
def q_generate(entity, property):
    tags = tag_property(property)

    # super naive but for now: if the last POS is noun
    if tags[-1][1] == 'NN':
        print("The " + property + " of " + entity + " is ___")
    else:
        print(entity + " is " + property + " ___")

    #https://www.nltk.org/book/ch07.html
    # grammar = "NP: {<DT>?<JJ>*<NN>}"
    #
    # cp = nltk.RegexpParser(grammar)
    # print(cp)
    #
    # result = cp.parse(tags)


# takes an English input sentence and tags each word by POS
# for now, need: Stanford POS tagger https://nlp.stanford.edu/software/tagger.shtml
def tag_property(sentence):
    postagger = StanfordPOSTagger("stanford-postagger/models/english-bidirectional-distsim.tagger", "stanford-postagger/stanford-postagger.jar")
    tags  = postagger.tag(sentence.split())
    return tags
