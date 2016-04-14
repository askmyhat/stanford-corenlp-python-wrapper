import pexpect
import sys

# TODO: Move logging from stdout
# TODO: compare "parse" and "depparse"

class StanfordCoreNLP():
    sample = [
        "Stanford University is located in California. It is a great university, founded in 1891.",
        "Spotify raises $1 billion in debt with devilish terms to fight Apple Music",
        "CockroachDB just raised $20 million from Benchmark, Index, and GV",
        "Slack is work chat’s runaway train, raises $200M at $3.8B",
        "Venture firm Accel Partners just raised $2B from its investors"
    ]

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
#        "truecase", # TODO: resolve requirements
        "parse",
        "dcoref",
#        "coref", # High memory usage
        "mention",
        "relation",
        "natlog",
        "openie",
        "quote",
        "udfeats"
    ]

    annotators = []
    cwd = "~/stanford-corenlp.full-2015-12-09"
    expectation = "NLP>"
    engine = None
    raw_output = ''

    def __init__(self, cwd, annotators=None):
        self.cwd = cwd

        if annotators:
            self.init(annotators)

    def __del__(self):
        self.engine.kill(1)
        print("Engine terminated.")

    def init(self, annotators):
        print("Initializing engine. This may take a while, please wait.")

        if self.restart_required(annotators):
            if self.engine:
                self.engine.kill(1)

            cmd = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators ' + ','.join(self.annotators)

            self.engine = pexpect.spawnu(cmd, cwd=self.cwd, timeout=100)
            self.engine.expect(self.expectation)

    def restart_required(self, annotators):
        if not isinstance(annotators, list):
            annotators = [annotators]

        annotators_set = set(annotators)

        if not annotators_set.issubset(self.avaliable_annotators):
            raise Exception("Not supported annotators.")

        if annotators_set.issubset(self.annotators):
            return False

        self.annotators = []

        for annotator in annotators:
            self.add_annotator(annotator)

        return True

    def add_annotator(self, annotator):
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

        if annotator == "mention":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("ner")
            self.add_annotator("parse")

        if annotator == "entitymentions":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")
            self.add_annotator("ner")

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
            self.add_annotator("parse")

        if annotator == "natlog":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("lemma")
            self.add_annotator("parse")

        if annotator == "openie":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("natlog")

        if annotator == "quote":
            pass

        if annotator == "udfeats":
            self.add_annotator("tokenize")
            self.add_annotator("ssplit")
            self.add_annotator("pos")
            self.add_annotator("parse")

        if annotator not in self.annotators:
            self.annotators.append(annotator)


    @staticmethod
    def print_annotators():
        print("Avaliable annotators:")
        print("\n".join(StanfordCoreNLP.avaliable_annotators))

    def process(self, line):
        self.engine.sendline(line)
        self.engine.expect(self.expectation)
        result = self.engine.before
        raw_output = result
        return result

# Developing
#    def OpenIE(line=None):
#        if 'openie' not in self.annotators:

#        output = list(filter(None, self.c.before.splitlines()))
#        output = [tuple(filter(None, i.split('\t')[1:])) for i in output[1:]]
