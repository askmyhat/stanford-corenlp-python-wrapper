from StanfordCoreNLP import StanfordCoreNLP as nlp

path = "/home/as/stanford-corenlp-full-2015-12-09/"

for annotator in nlp.avaliable_annotators:
    print("\n\n\n +========================+ ")
    print("Testing", annotator)
    a = nlp(path, annotator)
    print("Annotators:", a.annotators)
    print(a.process(nlp.sample[0]))
