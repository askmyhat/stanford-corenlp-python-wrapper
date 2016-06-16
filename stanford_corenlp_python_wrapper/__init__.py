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
        "openie_with_coref",
        "quote",
        "udfeats"
    ]

    avaliable_parsers = [
        "tokenize",
        "ssplit",
        "ner",
        "dcoref",
        "coref",
        "openie",
        "openie_with_coref"
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

            if "openie_with_coref" in cmd:
                cmd = cmd.replace("openie_with_coref", "")[:-1]
                cmd += " -openie.resolve_coref"

            self.engine = pexpect.spawnu(cmd, cwd=self.cwd, timeout=5000)
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

        if annotator == "openie_with_coref":
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

        if line == self.last_input:
            return self.output

        self.last_input = line

        # Removing newlines
        line = ' '.join(' '.join(line.splitlines()).split())

        self.engine.sendline(line)
        self.engine.expect(self.expectation)

        self.output["raw"] = self.engine.before
        self.output["raw_sentences"] = [l[l.find("tokens):") + 10:] for l in self.output["raw"].split("Sentence #")[1:]]
        self.output["raw_words"] = []
        for sent in self.output["raw_sentences"]:
            self.output["raw_words"].append([line for line in sent.splitlines() if line[:6] == "[Text="])

        for annotator in self.annotators:
            if annotator == "openie_with_coref":
                annotator = "openie"
            if annotator == "dcoref":
                annotator = "coref"
            if annotator not in self.avaliable_parsers:
                continue

            parser = getattr(self, "parse_" + annotator)
            parser()

        output = self.output.copy()
        output.pop("raw", None)
        output.pop("raw_words", None)
        output.pop("raw_sentences", None)

        return output

    def tokenize(self, line):
        self.preprocess("tokenize", line)
        return self.output["tokenize"]

    def ssplit(self, line):
        self.preprocess("ssplit", line)
        return self.output["ssplit"]

    def ner(self, line):
        self.preprocess("ner", line)
        return self.output["ner"]

    def replace_ner(self, line):
        self.preprocess("ner", line)
        output = []

        words = self.output["tokenize"]
        ners = self.output["ner"]
        last_word = ""
        last_ner = ""
       
        for i in range(len(words)):
            sent = ""
            for j in range(len(words[i])):
                if ners[i][j] == last_ner and last_ner != "O":
                    continue
                if last_word + " " + words[i][j] in self.output["sentences"][i]:
                    sent += " "
                if ners[i][j] == "O":
                    sent += words[i][j]
                else:
                    sent += ners[i][j]
                last_ner = ners[i][j]
            output.append(sent)

        output = ' '.join(output)
        return output

    def openie(self, line, resolve_coref=False):
        if resolve_coref:
            return openie_with_coref(line)
        self.preprocess("openie", line)
        return self.output["openie"]

    def openie_with_coref(self, line):
        self.preprocess("openie_with_coref", line)
        return self.output["openie"]

    def coref(self, line):
        self.preprocess("coref", line)
        return self.output["coref"]

    def dcoref(self, line):
        self.preprocess("dcoref", line)
        return self.output["coref"]

    def parse_tokenize(self):
        self.output["tokenize"] = []
        for sent in self.output["raw_words"]:
            self.output["tokenize"].append([word.split()[0][6:] for word in sent])
        self.output["words"] = self.output["tokenize"]

    def parse_ssplit(self):
        self.output["ssplit"] = [sent.splitlines()[0] for sent in self.output["raw_sentences"]]
        self.output["sentences"] = self.output["ssplit"]

    def parse_ner(self):
        self.output["ner"] = []
        for sent in self.output["raw_words"]:
            self.output["ner"].append([word[word.find(" NamedEntityTag=")+16:].split()[0].split("]")[0] for word in sent])

    def parse_openie(self):
        self.output["openie"] = []
        for processed_sent in self.output["raw_sentences"]:
            c = processed_sent.find("Open IE")
            splitted = processed_sent[c + 16:].splitlines()
            splitted = [line for line in splitted if line[:3] == "1.0"]
            self.output["openie"].append([tuple(line.split("\t")[1:]) for line in splitted])

    def parse_coref(self):
        raw_coref = "\n".join(self.output["raw"].split("coreference set:")[1:])
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

class tokenize(AnnotatorWrapper):
    pass

class ssplit(AnnotatorWrapper):
    pass

class ner(AnnotatorWrapper):
    pass

class replace_ner(AnnotatorWrapper):
    pass

class dcoref(AnnotatorWrapper):
    pass

class coref(AnnotatorWrapper):
    pass

class openie(AnnotatorWrapper):
    pass

class openie_with_coref(AnnotatorWrapper):
    pass
