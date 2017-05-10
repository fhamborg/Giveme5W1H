import copy
import html
import logging
import os
import re
import xml.etree.cElementTree as ElementTree
from extractor.document import DocumentFactory


def parse_dir(path):
    """
    Reads all gate documents in a given directory.

    :param path: Absolute path to the directory
    :type path: String

    :return: A list of Document objects
    """

    log = logging.getLogger('GiveMe5W')

    factory = DocumentFactory()
    documents = []

    if not os.path.exists(path):
        log.warning('The given path does not exist: %s' % path)
    else:
        for root, directory, files in os.walk(path):
            for file in files:
                doc = parse_file(os.path.join(root, file), factory)
                if doc is not None:
                    documents.append(doc)

    return documents


def parse_file(path, factory):
    """
    Creates a Document object from a gate file.

    :param path: Absolute path to the file
    :type path: String
    :param factory: DocumentFactory used to instantiate the document
    :type factory: DocumentFactory

    :return: The Document object
    """

    log = logging.getLogger('GiveMe5W')

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
            pubdate = None
            source = None

            # search for publication date in document features
            for feature in root.find('GateDocumentFeatures'):
                if feature[0].text == 'pubdate':
                    pubdate = feature[1].text
                elif feature[0].text == 'source':
                    source = feature[1].text

            # read the annotation
            annotations = {'what': [], 'who': [], 'why': [], 'where': [], 'when': []}
            for annotation in root.find('AnnotationSet'):
                attrib = annotation.attrib

                # read marked text sections
                if attrib['Type'] == 'TextSection':
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

                elif attrib['Type'] == 'FiveW':
                    marked_text = extract_markup(text_node, attrib['StartNode'], attrib['EndNode'], encoding)
                    question = None
                    features = [None, None, None]  # id , accuracy, text

                    for feature in [(f[0].text, f[1].text) for f in annotation]:
                        if feature[0] == 'accuracy':
                            features[1] = feature[1]
                        elif feature[0] == 'id':
                            features[1] = feature[0]
                        elif feature[0] == 'question':
                            question = feature[1]

                    if question is not None:
                        features[2] = marked_text
                        annotations[question].append(features)

            # backup for gate documents without marked text sections
            if len(title) == 0 and len(description) == 0 and len(text) == 0:
                title = html.unescape(ElementTree.tostring(text_node, method='text').decode(encoding))

            for answers in annotations.items():
                #sort annotations based on id and accuracy
                answers[1].sort(key=lambda x: x[0] or 'None')
                answers[1].sort(key=lambda x: x[1] or 'None')

            document = factory.spawn_doc(title, description, text, path.split('/')[-1], source)
            document.set_annotations(annotations)
            document.set_date(pubdate)

            return document

        except ElementTree.ParseError as e:
            log.warning('The given file contains invalid xml: %s - %s', e, path)

            return None


def extract_markup(root, start, end, encoding):
    """
    Extracts marked text from text body

    :param root: xml root of the text body
    :param start: Id of the start Node
    :param end: Id of the end Node
    :param encoding: Document encoding.
    :return: Marked text.
    """
    text = ''

    for node in root:
        if node.attrib['id'] == end:
            break
        elif node.attrib['id'] == start or len(text) > 0:
            text += html.unescape(ElementTree.tostring(node, method='text').decode(encoding))

    return text