import pexpect
import os

# TODO: compare "parse" and "depparse"
# TODO: Enum for annotators with desc

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]

class Engine(metaclass=Singleton):
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
        "coref",
        "mention",
        "relation",
        "natlog",
        "openie",
        "quote",
        "udfeats"
    ]

    annotators = []
    expectation = "NLP>"
    engine = None
    output = {}
    last_input = ""

    def __init__(self, path, annotators=None):
        if not os.path.exists(path):
            raise Exception("Incorrect path to StanfordCoreNLP directory")
        self.cwd = path
        if annotators:
            self.add_annotators(annotators)

    def __del__(self):
        self.reset()

    def add_annotators(self, annotators):
        print("Initializing engine. This may take a while, please wait.")
        if self.restart_required(annotators):
            self.reset()
            if not isinstance(annotators, list):
                annotators = [annotators]
            self.make_annotators_list(annotators)
            cmd = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators ' + ','.join(self.annotators)
            self.engine = pexpect.spawnu(cmd, cwd=self.cwd, timeout=100)
            self.engine.expect(self.expectation)

    def reset(self):
        if self.engine:
            self.engine.kill(1)
            print("Engine terminated.")
        self.annotators = []

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

    def preprocess(self, annotator):
        if annotator in self.annotators and line == self.last_input:
            return self.output[annotator]
        if annotator not in self.annotators:
            self.add_annotators(annotator)
        if line:
            self.process(line)
        return None

    def process(self, line):
        if len(self.annotators) == 0:
            raise Exception("No annotators specified")
        self.engine.sendline(line)
        self.engine.expect(self.expectation)
        self.output["raw"] = self.engine.before
        self.splitted_output = [l[l.find("tokens):") + 10:] for l in self.output["raw"].split("Sentence #")[1:]]
        return self.output["raw"]

    def OpenIE(self, line):
        preresult = self.preprocess("openie", line)
        if preresult is not None:
            return preresult

        self.output["openie"] = []
        for processed_sent in self.splitted_output:
            c = processed_sent.find("Open IE")
            splitted = processed_sent[c + 16:].splitlines()
            splitted = [line for line in splitted if line[:3] == "1.0"]
            self.output["openie"].append([tuple(line.split("\t")[1:]) for line in splitted])
        return self.output["openie"]

    def NER(self, line):
        preresult = self.preprocess("ner", line)
        if preresult is not None:
            return preresult

        self.output["ner"] = {}
        splitted = [line for line in self.output["raw"].splitlines() if line[:6] == "[Text="]
        last_key = ""
        for line in splitted:
            key = line.split()[5][15:-1]
            if key == "O":
                continue
            if key == "DAT":
                key = "DATE"
            value = line.split()[0][6:]
            if key in self.output["ner"]:
                if key == last_key:
                    self.output["ner"][key][-1] += " " + value
                else:
                    self.output["ner"][key].append(value)
            else:
                self.output["ner"][key] = [value]
            last_key = key
        for key in self.output["ner"]:
            self.output["ner"][key] = list(set(self.output["ner"][key]))
        return self.output["ner"]

    def DCoref(self, line):
        preresult = self.preprocess("dcoref", line)
        if preresult is not None:
            return preresult

        self.output["dcoref"] = self.output["raw"].split("Coreference set:")[1].replace("\t", "").splitlines()[1:]
        return self.output["dcoref"]

class AnnotatorWrapper:
    def __init__(self, path):
        self.annotator = self.__class__.__name__
        self.engine = Engine(path)
        if self.annotator.lower() not in self.engine.annotators:
            self.engine.add_annotators(self.annotator.lower())
        self.sample = self.engine.sample

    def process(self, line):
        if not line:
            raise Exception("Empty input.")
        processor = getattr(self.engine, self.annotator)
        self.engine.process(line)
        return processor(line)

class OpenIE(AnnotatorWrapper):
    pass

class NER(AnnotatorWrapper):
    pass

class DCoref(AnnotatorWrapper):
    pass

