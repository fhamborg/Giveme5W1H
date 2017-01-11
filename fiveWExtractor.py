from extractors import actionExtractor, environmentExtractor, causeExtractor


class FiveWExtractor:

    preprocessor = None
    extractors = []

    def __init__(self, prep, extractorlist=None):
        self.preprocessor = prep

        if extractorlist is not None and len(extractorlist) > 0:
            self.extractors = extractorlist
        else:
            self.extractors = [
                actionExtractor.ActionExtractor(),
                environmentExtractor.EnvironmentExtractor(),
                causeExtractor.CauseExtractor()
            ]

    def parse(self, doc):
        self.preprocessor.preprocess(doc)
        for extractor in self.extractors:
            extractor.extract(doc)

        return doc


if __name__ == "__main__":
    ex = FiveWExtractor('/home/soeren/Downloads/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
                               '/home/soeren/Downloads/stanford-ner-2015-12-09/stanford-ner.jar')


