from extractor.document import Document
from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.five_w_extractor import FiveWExtractor

def parse_file_to_articles(path):
    f = open(path, "r")
    json.load(file_content)


if __name__ == '__main__':
    list_articles = parse_file_to_articles("bbc_sampled_contents.json")

    doc = extractor.parse(Document(article["title"], article["lead"], article["text"]))
    _print_5w(article, doc)
