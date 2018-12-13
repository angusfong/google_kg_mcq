import nltk
from nltk.tag.stanford import StanfordPOSTagger

# generate a question that asks the property of entity
def q_generate(entity, property):
    tags = tag_property(property)

    # if last tag is not preposition or subordinating conjunction
    if tags[-1][1] != 'IN':
        print("The " + property + " of " + entity + " is ___")
    else:
        print(entity + " is " + property + " ___")

# takes an English input sentence and tags each word by POS
# for now, need: Stanford POS tagger https://nlp.stanford.edu/software/tagger.shtml
def tag_property(sentence):
    postagger = StanfordPOSTagger("stanford-postagger/models/english-bidirectional-distsim.tagger", "stanford-postagger/stanford-postagger.jar")
    tags  = postagger.tag(sentence.split())
    return tags
