from examples.startup.util import StartupHelper


def start():
    h = StartupHelper()
    h.do_command('CoreNLP',
                 'java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -props edu/stanford/nlp/coref/properties/neural-english.properties',
                 'stanford-corenlp-full-2016-10-31')
    h.forever()


start()

#
