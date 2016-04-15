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
            self.add_annotators(annotators)

    def __del__(self):
        self.reset()

    def add_annotators(self, annotators):
        print("Initializing engine. This may take a while, please wait.")
        if self.restart_required(annotators):
            if not isinstance(annotators, list):
                annotators = [annotators]
            self.make_annotators_list(annotators)
            if self.engine:
                self.engine.kill(1)
            cmd = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators ' + ','.join(self.annotators)
            self.engine = pexpect.spawnu(cmd, cwd=self.cwd, timeout=100)
            self.engine.expect(self.expectation)

    def reset(self):
        self.engine.kill(1)
        self.annotators = []
        print("Engine terminated.")

    def restart_required(self, annotators):
        if not isinstance(annotators, list):
            annotators = [annotators]
        annotators_set = set(annotators)
        if not annotators_set.issubset(self.avaliable_annotators):
            raise Exception("Not supported annotators.")
        if annotators_set.issubset(self.annotators):
            return False
        return True

    def make_annotators_list(self, annotators):
        for annotator in annotators:
            self.resolve_dependency(annotator)

    def resolve_dependency(self, annotator):
        if annotator == "tokenize":
            pass

        if annotator == "cleanxml":
            self.resolve_dependency("tokenize")

        if annotator == "ssplit":
            self.resolve_dependency("tokenize")

        if annotator == "pos":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")

        if annotator == "lemma":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")

        if annotator == "ner":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("lemma")

        if annotator == "regexner":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")

        if annotator == "gender":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")

        if annotator == "truecase":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("lemma")

        if annotator == "parse":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")

        if annotator == "mention":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("ner")
            self.resolve_dependency("parse")

        if annotator == "entitymentions":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("lemma")
            self.resolve_dependency("ner")

        if annotator == "dcoref":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("lemma")
            self.resolve_dependency("ner")
            self.resolve_dependency("parse")

        if annotator == "coref":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("lemma")
            self.resolve_dependency("ner")
            self.resolve_dependency("dependency")
            self.resolve_dependency("mention")

        if annotator == "relation":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("lemma")
            self.resolve_dependency("ner")
            self.resolve_dependency("parse")

        if annotator == "natlog":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("lemma")
            self.resolve_dependency("parse")

        if annotator == "openie":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("natlog")

        if annotator == "quote":
            pass

        if annotator == "udfeats":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("parse")

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
        self.raw_output = result
        return result

# Developing
    def OpenIE(self, line=None):
        if "openie" not in self.annotators:
            self.add_annotators("openie")
        if line:
            self.process(line)
        if not line and "openie" not in self.annotators:
            raise Exception("Empty input.")

        output = self.raw_output
        openie_output = []
        while True:
            c = output.find("Open IE")
            if c == -1:
                break
            output = output[c + 16:]
            openie_output.append(output[:output.find("Sentence #")])

        result = []
        for processed_sentence in openie_output:
            output = list(filter(None, processed_sentence.splitlines()))
            output = [tuple(filter(None, i.split('\t')[1:])) for i in output]
            result.append(output)

        return result

