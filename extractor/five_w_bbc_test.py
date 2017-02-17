from extractor.document import Document
from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.five_w_extractor import FiveWExtractor
import json


def _print_1w(_doc, question):
    one_w = _doc.questions[question]
    if len(one_w) == 0:
        print(question + ": NONE")
        return
    print(question + ": " + str(one_w[0]))
    # _print_list(one_w[0][0])


def _print_5w(_article, _doc):
    print(_article["title"])
    print(_article["path"])
    _print_1w(_doc, "who")
    _print_1w(_doc, "what")
    _print_1w(_doc, "when")
    _print_1w(_doc, "where")
    _print_1w(_doc, "why")
    print("")
    print("")


path = "../data/bbc_sampled_contents.json"


if __name__ == '__main__':
    with open(path, "r") as data_file:
        list_articles = json.load(data_file)
    print("parsed {} articles".format(len(list_articles)))

    # initialize required extractors
    extractor_list = [
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor()
    ]
    extractor = FiveWExtractor(extractor_list)

    for article in list_articles:
        doc = extractor.parse(Document(article["title"], article["lead"], article["text"]))
        _print_5w(article, doc)



