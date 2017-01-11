import logging
import os
import copy
import re
import html
import xml.etree.cElementTree as ElementTree

from document import Document


def parse_dir(path):

    documents = []

    if not os.path.exists(path):
        logging.warning('The given path does not exist: %s' % path)
    else:
        for root, directory, files in os.walk(path):
            for file in files:
                doc = parse_file(os.path.join(root, file))
                if doc is not None:
                    documents.append(doc)

    return documents


def parse_file(path):

    if not os.path.isfile(path):
        return None

    with open(path) as raw_data:
        try:
            # read encoding from xml head
            encoding = re.search('''(?<=encoding=["'])[^'"]*''', raw_data.readline())
            if encoding:
                encoding = encoding.group()
            else:
                encoding = 'utf-8'

            root = ElementTree.fromstring(raw_data.read())
            text_node = copy.deepcopy(root.find('TextWithNodes'))

            title = html.unescape(ElementTree.tostring(text_node, method='text').decode(encoding))
            description = None
            text = None

            # read the Annotation
            annotations = []
            for annotation in root.find('AnnotationSet'):
                attrib = annotation.attrib

                if attrib['Type'] == 'TextSection':
                    # divide text up in sections if marked
                    marked_text = extract_markup(text_node, attrib['StartNode'], attrib['EndNode'], encoding)
                    for feature in annotation:
                        if feature[1].text == 'title':
                            title = marked_text
                        elif feature[1].text == 'description':
                            description = marked_text
                        elif feature[1].text == 'text':
                            text = marked_text
                        else:
                            logging.warning("Wrong feature in 'TextSection' found.")
                else:
                    features = [(f[0].text, f[1].text) for f in annotation]
                    marked_text = extract_markup(text_node, attrib['StartNode'], attrib['EndNode'], encoding)
                    annotations.append((attrib['Type'], features, marked_text))

            document = Document(title, description, text)
            document.annotations = annotations

            return document

        except ElementTree.ParseError as e:
            logging.warning('The given file contains invalid xml: %s - %s', e, path)

            return None


def extract_markup(root, start, end, encoding):
    text = ''

    for node in root:
        if node.attrib['id'] == end:
            break
        elif node.attrib['id'] == start or len(text) > 0:
            text += html.unescape(ElementTree.tostring(node, method='text').decode(encoding))

    return text


if __name__ == "__main__":
    docs = parse_dir('./data/articles/')
    logging.info(' %i documents parsed' % len(docs))
