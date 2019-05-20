"""
This is a simple example how to use the extractor in combination with news-please, a news crawler and scraper (https://github.com/fhamborg/news-please).

- Nothing is cached

"""

# don`t forget to start up core_nlp_host
# giveme5w1h-corenlp

from newsplease import NewsPlease

from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor

extractor = MasterExtractor()


def main():
    article = NewsPlease.from_url(
        'https://www.foxnews.com/politics/house-democrat-subpoenas-mnuchin-irs-for-trumps-tax-returns')
    doc = Document.from_newsplease(article)
    doc = extractor.parse(doc)
    answers = doc.get_top_answer('who').get_parts_as_text()


if __name__ == '__main__':
    main()
