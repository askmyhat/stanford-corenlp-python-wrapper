import pexpect
import sys


class StanfordCoreNLP():
    expectation = "NLP>"
    avaliable_annotators = [
        "tokenize",
        "cleanxml",
        "ssplit",
        "pos",
        "lemma",
        "ner",
        "regexner",
        "entitymentions",
        "gender",
        "truecase",
        "parse",
        "dcoref",
        "coref",
        "mention",
        "relation",
        "dependencies",
        "natlog",
        "openie",
        "quote",
        "udfeats"
    ]
    runned_annotators = []
    new_annotators = []
    cwd = "~/stanford-corenlp.full-2015-12-09"
    engine = None

    def __init__(self, cwd=None, annotators=None):
        if cwd:
            self.cwd = cwd
        else:
            raise Exception("Please, specify path to Stanford CoreNLP sources.\nUsage: nlp = StanfordCoreNLP(cwd='/home/bob/stanford-corenlp-full-2015-12-09', annotators=['NER']).")

        if not annotators:
            self.print_annotators()
            raise Exception("Please, specify annotators.\nUsage: nlp = StanfordCoreNLP(cwd='/home/bob/stanford-corenlp-full-2015-12-09', annotators=['NER']).")

        self.init(annotators)

    def __del__(self):
        self.engine.kill(1)

    def init(self, annotators):
        print("Initializing engine. This may take a while, please wait.")

        if self.restart_required(annotators):
            if self.engine:
                self.engine.kill(1)
            cmd = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators ' + ','.join(self.new_annotators)

            self.engine = pexpect.spawnu(cmd, cwd=self.cwd, timeout=100)
            self.engine.expect(self.expectation)
            self.runned_annotators = self.new_annotators
            self.new_annotators = []

    def restart_required(self, annotators):
        if type(annotators) is list:
            for annotator in annotators:
                self.add_annotator(annotator.lower())
        else:
            self.add_annotator(annotators.lower())

        for n in self.new_annotators:
            if n not in self.runned_annotators:
                return True

        return False

    def add_annotator(self, annotator):
        if annotator not in self.avaliable_annotators:
            raise Exception("Not supported annotator.")

        if annotator == "tokenize":
            pass

        if annotator == "cleanxml":
            self.add_annotator("tokenize")

        if annotator == "ssplit":
            self.add_annotator("tokenize")

        if annotator == "pos":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")

        if annotator == "lemma":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")

        if annotator == "ner":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")

        if annotator == "regexner":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")

        if annotator == "gender":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")

        if annotator == "truecase":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")

        if annotator == "parse":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")

        if annotator == "dependencies":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")

        if annotator == "mention":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("ner")
            self.add_annotator("dependency")

        if annotator == "entitymentions":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")
            self.add_annotator("dependency")

        if annotator == "dcoref":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")
            self.add_annotator("ner")
            self.add_annotator("parse")

        if annotator == "coref":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")
            self.add_annotator("ner")
            self.add_annotator("dependency")
            self.add_annotator("mention")

        if annotator == "relation":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")
            self.add_annotator("ner")
            self.add_annotator("dependency")

        if annotator == "natlog":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")
            self.add_annotator("dependency")  # todo(gabor) can also use 'parse' annotator

        if annotator == "openie":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("dependency")  # todo(gabor) can also use 'parse' annotator
            self.add_annotator("natlog")

        if annotator == "quote":
            pass

        if annotator == "udfeats":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("dependency")

        if annotator not in self.new_annotators:
            self.new_annotators.append(annotator)

    @staticmethod
    def print_annotators():
        print("Avaliable annotators:")
        print("\n".join(StanfordCoreNLP.avaliable_annotators))

    sample = [
        "Spotify raises $1 billion in debt with devilish terms to fight Apple Music",
        "CockroachDB just raised $20 million from Benchmark, Index, and GV",
        "Slack is work chat’s runaway train, raises $200M at $3.8B",
        "Venture firm Accel Partners just raised $2B from its investors"
    ]

    def process(self, line):
        self.engine.sendline(input)
        self.engine.expect(self.expectation)
        output = self.engine.before
#        output = list(filter(None, self.c.before.splitlines()))
#        output = [tuple(filter(None, i.split('\t')[1:])) for i in output[1:]]
        return output

