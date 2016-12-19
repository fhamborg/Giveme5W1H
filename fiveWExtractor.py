from extractors import whoExtractor, whereExtractor, whyExtractor, actionExtractor
from document import Document


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
            ]

    def parse(self, title, desc=None):
        doc = Document(title, desc)
        self.preprocessor.preprocess(doc)

        for extractor in self.extractors:
            extractor.extract(doc)

        return doc


if __name__ == "__main__":
    ex = FiveWExtractor('/home/soeren/Downloads/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
                               '/home/soeren/Downloads/stanford-ner-2015-12-09/stanford-ner.jar')
    data = "Harold T. Martin III kept his security clearance despite a record that included drinking problems, unpaid tax bills and an episode in which he posed as a police officer. Also another sentece for you."
    ex.parse(data)

