import sys
import os
from os.path import join
import nltk
from nltk.tag.stanford import StanfordPOSTagger

# generate a question that asks the property of entity
def q_generate(entity, property):
    try:
       tagger = os.environ.get("TAGGER")
    except KeyError:
       print ("Please set export TAGGER=$PATH/TO/TAGGER")
       sys.exit(1)
        
    tags = tag_property(property, tagger)

    # if last tag is not preposition or subordinating conjunction
    if tags[-1][1] != 'IN':
        print("The " + property + " of " + entity + " is ___")
    else:
        print(entity + " is " + property + " ___")

# takes an English input sentence and tags each word by POS
# for now, need: Stanford POS tagger https://nlp.stanford.edu/software/tagger.shtml
def tag_property(sentence, tagger):
    postagger = StanfordPOSTagger(join(tagger, "stanford-postagger/models/english-bidirectional-distsim.tagger"), join(tagger, "stanford-postagger/stanford-postagger.jar"))
    tags  = postagger.tag(sentence.split())
    return tags
