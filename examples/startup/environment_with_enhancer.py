from examples.startup.util import StartupHelper


def start():
    h = StartupHelper()
    h.do_command('CoreNLP',
                 'java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000',
                 'stanford-corenlp-full-2016-10-31')

    h.do_command('AIDA', 'export MAVEN_OPTS="-Xmx16G" && mvn jetty:run', 'aida-3.0.4')

    h.forever()


if __name__ == '__main__':
    start()
