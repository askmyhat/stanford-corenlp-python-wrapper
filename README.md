# Python wrapper for Stanford CoreNLP

1. Download [Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) and unpack it.
2. Download stanford-corenlp-python-wrapper:

    `git clone https://github.com/askmyhat/stanford-corenlp-python-wrapper`

3. Install it:

    `python setup.py install`

## Usage example

### Specific annotator

```python
from StanfordCoreNLP import NER
path = "/home/as/stanford-corenlp-full-2015-12-09/"
p = NER(path)
r = p.process(p.sample[0])
```

### All annotators

```python
from StanfordCoreNLP import Engine as nlp
path = "/home/as/stanford-corenlp-full-2015-12-09/"

# Initialize engine without annotators
p = nlp(path, "openie")

# Show all avaliable annotators
print(nlp.avaliable_annotators)

# Initialize engine with specified annotators and it's dependencies
p = nlp(path, "openie")

# Process data into raw string output
r = p.process(nlp.sample[0])

# or process data into python structures (initializing annotator if requred)
r = p.OpenIE(nlp.sample[0])

# Terminate engine (if you have very limited RAM and no more need in already added annotators)
p.reset()

# Continue processing with another annotator
r = p.NER(mlp.sample[0])
```

### Avaliable annotators with python structures output
* Tokenize
* SSplit
* NER
* Coref/DCoref
* OpenIE (CorefOpenIE() extract IE with coreference resolving)

### Note
Coref annotator requires more than 4GB RAM. You can use DCoref instead.
Each coreference is represented by tuple consisting of two triplets for each corresponding token (sentence, start_word_position, end_word_position)
