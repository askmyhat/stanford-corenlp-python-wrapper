# Python wrapper for Stanford CoreNLP

1. Download [Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) and unpack it.
2. Download stanford-corenlp-python-wrapper:

```bash
git clone https://github.com/askmyhat/stanford-corenlp-python-wrapper
cd stanford-corenlp-python-wrapper
```

3. Install it:

```bash
python setup.py install
```

## Usage example

### Single annotator

```python
from StanfordCoreNLP import NER
path = "/home/as/stanford-corenlp-full-2015-12-09/"
p = ner(path)
r = p.process(p.sample[0])
```

### Multiple annotators

```python
import stanford_corenlp_python_wrapper as nlp
path = "/home/as/stanford-corenlp-full-2015-12-09/"

# Initialize engine
# without annotators
p = nlp.Engine(path)
# with one
p = nlp.Engine(path, "openie")
# or more
p = nlp.Engine(path, ["openie", "dcoref"])
# Also nitializing all dependencies

# Show all avaliable annotators
print(nlp.Engine.avaliable_annotators)

# Add one
p.add_annotators("openie")
# or more annotators
p.add_annotators(["openie", "ner"])

# Process data into raw output for all initialized annotators
r = p.process(nlp.sample[0])
# or process data into python structures (and initialize annotator if requred)
r = p.OpenIE(nlp.sample[0])

# Terminate engine
p.reset()
```

### Notes
* Use `reset()` if you have limited memory and no need in initialized annotators.
* Reinitializing engine without `reset()` keeps initialized annotators added before.
* Coref annotator requires more than 4GB RAM. You can use DCoref instead bit it's less accurate.
* Each coreference is represented by tuple consisting of two triplets for each corresponding token (sentence, start_word_position, end_word_position)

### Avaliable annotators with python structures output
* tokenize
* ssplit
* ner
* coref/dcoref
* openie
* openie_with_coref (OpenIE with coreference resolving)

## Similar projects
* [https://github.com/dasmith/stanford-corenlp-python](https://github.com/dasmith/stanford-corenlp-python)
* [https://github.com/brendano/stanford_corenlp_pywrapper](https://github.com/brendano/stanford_corenlp_pywrapper)
* [https://bitbucket.org/torotoki/corenlp-python](https://bitbucket.org/torotoki/corenlp-python)
