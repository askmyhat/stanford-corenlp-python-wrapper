import pexpect
import sys

sents = [
    "Spotify raises $1 billion in debt with devilish terms to fight Apple Music",
    "CockroachDB just raised $20 million from Benchmark, Index, and GV",
    "Slack is work chat’s runaway train, raises $200M at $3.8B",
    "Venture firm Accel Partners just raised $2B from its investors"
]

class StanfordCoreNLP(object):
    expectation = "NLP>"

    def __init__(self, cwd):
        print("Starting processor. This may take a while, please wait.")
        self.c = pexpect.spawnu(self.cmd, cwd=cwd, timeout=100)
        self.c.expect(self.expectation)

    def __del__(self):
        self.c.kill(1)

class Core(StanfordCoreNLP):
    cmd = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref'

class OpenIE(StanfordCoreNLP):
    cmd = 'java -mx1g -cp stanford-corenlp-3.6.0.jar:stanford-corenlp-3.6.0-models.jar:CoreNLP-to-HTML.xsl:slf4j-api.jar:slf4j-simple.jar edu.stanford.nlp.naturalli.OpenIE'

    def process(self, input):
        self.c.sendline(input)
        self.c.expect(self.expectation)
        output = list(filter(None, self.c.before.splitlines()))
        output = [tuple(filter(None, i.split('\t')[1:])) for i in output[1:]]
        return output

