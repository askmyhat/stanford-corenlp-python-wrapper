import pexpect
import os
import sys

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
        "corefopenie",
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

    def reset(self):
        if self.engine:
            self.engine.kill(1)
            print("Engine terminated.")
            sys.stdout.flush()
        self.annotators = []

    def add_annotators(self, annotators):
        if not isinstance(annotators, list):
            annotators = [annotators]
        annotators = [annotator.lower() for annotator in annotators]
        if self.restart_required(annotators):
            old_annotators = self.annotators
            self.reset()
            print("Initializing engine. This may take a while, please wait.")
            sys.stdout.flush()
            self.make_annotators_list(annotators + old_annotators)

            memory = "2"
            if 'coref' in self.annotators:
                memory = "5"

            cmd = 'java -cp "*" -Xmx' + memory + 'g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators ' + ','.join(self.annotators)

            if "corefopenie" in cmd:
                cmd = cmd.replace("corefopenie", "")[:-1]
                cmd += " -openie.resolve_coref"

            self.engine = pexpect.spawnu(cmd, cwd=self.cwd, timeout=1000)
            self.engine.expect(self.expectation)
            print("Engine initialized.")
            sys.stdout.flush()

    def restart_required(self, annotators):
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
        if annotator in ["tokenize", "ssplit"]:
            if "tokenize" not in self.annotators:
                self.annotators.append("tokenize")
            if "ssplit" not in self.annotators:
                self.annotators.append("ssplit")

        if annotator == "ssplit":
            self.resolve_dependency("tokenize")

        if annotator == "cleanxml":
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
            self.resolve_dependency("parse")
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

        if annotator == "corefopenie":
            self.resolve_dependency("coref")
            self.resolve_dependency("openie")

        if annotator == "quote":
            pass

        if annotator == "udfeats":
            self.resolve_dependency("tokenize")
            self.resolve_dependency("ssplit")
            self.resolve_dependency("pos")
            self.resolve_dependency("parse")

        if annotator not in self.annotators:
            self.annotators.append(annotator)

    def preprocess(self, annotator, line):
        if annotator not in self.annotators:
            self.add_annotators(annotator)
            self.process(line)
            return
        if line != self.last_input:
            self.process(line)

    def process(self, line):
        if len(self.annotators) == 0:
            raise Exception("No annotators specified")

        self.last_input = line

        # Removing newlines
        line = ' '.join(' '.join(line.splitlines()).split())

        self.engine.sendline(line)
        self.engine.expect(self.expectation)
        self.output["raw"] = self.engine.before
        self.output["sentences"] = [l[l.find("tokens):") + 10:] for l in self.output["raw"].split("Sentence #")[1:]]
        self.output["words"] = []
        for sent in self.output["sentences"]:
            self.output["words"].append([line for line in sent.splitlines() if line[:6] == "[Text="])
        return self.output["raw"]

    def Tokenize(self, line):
        self.preprocess("tokenize", line)
        self.output["tokenize"] = []
        for sent in self.output["words"]:
            self.output["tokenize"].append([word.split()[0][6:] for word in sent])
        return self.output["tokenize"]

    def SSplit(self, line):
        self.preprocess("ssplit", line)
        self.output["ssplit"] = [sent.splitlines()[0] for sent in self.output["sentences"]]
        return self.output["ssplit"]

    def NER(self, line):
        self.preprocess("ner", line)
        self.output["ner"] = {}
        last_key = ""
        for line in sum(self.output["words"], []):
            key = line.split()[5][15:-1]
            if key == "O":
                last_key = key
                continue
            if key == "DAT":
                key = "DATE"
            if key == "ORDINA":
                key = "ORDINAL"
            if key == "NUMBE":
                key = "NUMBER"
            if key == "PERSO":
                key = "PERSON"
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

    def OpenIE(self, line, resolve_coref=False):
        if resolve_coref:
            return CorefOpenIE(line)

        self.preprocess("openie", line)
        self.parse_openie(line)
        return self.output["openie"]

    def CorefOpenIE(self, line):
        self.preprocess("corefopenie", line)
        self.parse_openie(line)
        return self.output["openie"]

    def parse_openie(self, line):
        self.output["openie"] = []
        for processed_sent in self.output["sentences"]:
            c = processed_sent.find("Open IE")
            splitted = processed_sent[c + 16:].splitlines()
            splitted = [line for line in splitted if line[:3] == "1.0"]
            self.output["openie"].append([tuple(line.split("\t")[1:]) for line in splitted])

    def Coref(self, line):
        self.preprocess("coref", line)
        self.parse_coref()
        return self.output["coref"]

    def DCoref(self, line):
        self.preprocess("dcoref", line)
        self.parse_coref()
        return self.output["coref"]

    def parse_coref(self):
        raw_coref = "\n".join(self.output["raw"].split("Coreference set:")[1:])
        raw_coref = raw_coref.replace("\t(", "")
        raw_coref = raw_coref.replace("[", "")
        raw_coref = raw_coref.replace("]) -> (", ",")
        raw_coref = raw_coref.replace("])", "")
        raw_coref = raw_coref.splitlines()

        self.output["coref"] = []
        for sent in raw_coref:
            if len(sent) == 0:
                continue
            sp = sent.split(',')
            coref = (int(sp[0]) - 1, int(sp[2]) - 1, int(sp[3]) - 1, int(sp[4]) - 1, int(sp[6]) - 1, int(sp[7]) - 1)
            self.output["coref"].append(coref)

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
        return processor(line)

class Tokenize(AnnotatorWrapper):
    pass

class SSplit(AnnotatorWrapper):
    pass

class NER(AnnotatorWrapper):
    pass

class DCoref(AnnotatorWrapper):
    pass

class Coref(AnnotatorWrapper):
    pass

class OpenIE(AnnotatorWrapper):
    pass

class CorefOpenIE(AnnotatorWrapper):
    pass
