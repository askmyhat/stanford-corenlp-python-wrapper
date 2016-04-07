import pexpect
import sys

sents = [
    "Spotify raises $1 billion in debt with devilish terms to fight Apple Music",
    "CockroachDB just raised $20 million from Benchmark, Index, and GV",
    "Slack is work chat’s runaway train, raises $200M at $3.8B",
    "Venture firm Accel Partners just raised $2B from its investors"
]

def run_shell(cmd, cwd, expectation, init_expectation=None, input=None):
    if not init_expectation:
        init_expectation = expectation

    result = []

    c = pexpect.spawnu(cmd, timeout=100, cwd=cwd)

    c.expect(init_expectation)
    c.sendline(input[0])

    for line in input[1:]:
        c.expect(expectation)
        output = list(filter(None, c.before.splitlines()))
        output = (output[0], [tuple(filter(None, i.split('\t'))) for i in output[1:]])
        result.append(output)
        c.sendline(line)

    c.expect(expectation)
    output = list(filter(None, c.before.splitlines()))
    output = (output[0], [tuple(filter(None, i.split('\t'))) for i in output[1:]])
    result.append(output)

    c.kill(1)
    return result

def run_core(input=None):
    cwd = '/home/as/stanford-corenlp-full-2015-12-09'
    cmd = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref'
    expectation = "NLP>"
    return run_shell(cmd, cwd, expectation, input)

def run_openie(input=None):
    cwd = '/home/as/stanford-corenlp-full-2015-12-09'
    cmd = 'java -mx1g -cp stanford-corenlp-3.6.0.jar:stanford-corenlp-3.6.0-models.jar:CoreNLP-to-HTML.xsl:slf4j-api.jar:slf4j-simple.jar edu.stanford.nlp.naturalli.OpenIE'
    expectation = "OpenIE> "
    init_expectation = "Processing from stdin. Enter one sentence per line."
    return run_shell(cmd, cwd, expectation, init_expectation, input)

r = run_openie(sents)
print(r)
