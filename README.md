# Generating Multiple-Choice Questions Using Google Knowledge Graph and Wikidata
## Downloading the Stanford POS Tagger
If you do not already have access, it can be downloaded here: https://nlp.stanford.edu/software/tagger.shtml

Define tagger path with `export TAGGER=$PATH/TO/TAGGER`

## Running query.py

Usage: `python query.py [topic_of_initerest] -type ["Thing"/"Person"/"Place" or other schemas found at schemas.org]`
Optional: `-specific` to return most relevant entity only
