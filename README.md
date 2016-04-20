# Python wrapper for Stanford CoreNLP

1. Download [Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) and unpack it.
2. Download stanford-corenlp-python-wrapper:

    `git clone https://github.com/askmyhat/stanford-corenlp-python-wrapper`

3. Put StanfordCoreNLP.py from this repository in your project directory

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

print(nlp.avaliable_annotators)

# Initialize engine with specified annotators and it's dependencies
p = nlp(path, "openie")

# Process data and get raw output as string
r = p.process(nlp.sample[0])

# Initialize engine if required and process data into python structures
r = p.OpenIE(nlp.sample[0])

# Terminate engine
p.reset()
```

### Avaliable raw output into python structures processors
* Tokenize
* NER
* OpenIE
* Coref/DCoref

### Note
Coref annotator requires more than 4GB RAM. You can use DCoref instead.
Each coreference is represented by tuple consisting of two triplets for each corresponding token (sentence, start_word_position, end_word_position)
