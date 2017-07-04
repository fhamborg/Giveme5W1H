import copy
import glob
import hashlib
import html
import json
import xml.etree.ElementTree as ET


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
            text += html.unescape(ET.tostring(node, method='text').decode(encoding))

    return text


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2, ensure_ascii=False)


# get topic files
print("Starting converting")

topics = {}
fileTopics = open('input/index.txt', 'r')

for topic in fileTopics.read().split('#'):
    parts = topic.split('\n')
    topicCandidate = parts.pop(0);
    parts = [part for part in parts if '' is not part]
    if topicCandidate is not '':
        if topicCandidate is not '' and topicCandidate in topics:
            topics[topicCandidate] += parts
        else:
            topics[topicCandidate] = parts
# create a structure filename->topic
tmp_topics = topics
topics = {}
for topic in tmp_topics:
    for filename in tmp_topics[topic]:
        topics[filename] = topic

# get the annotation file
with open('input/annotation.json', 'r', encoding='utf-8-sig') as dataAnnotation:
    annotation = json.load(dataAnnotation)

for filepath in glob.glob('input/*.xml'):
    filename = filepath[6:-4]
    news = ET.parse(filepath)
    root = news.getroot()

    text_node = copy.deepcopy(root.find('TextWithNodes'))

    # Output Object
    news = Object()

    news.fiveWoneH = Object()
    for features in root.iter('Feature'):
        if (features[0].text == 'MimeType'):
            news.mimeType = features[1].text
        if (features[0].text == 'source'):
            news.url = features[1].text
        if (features[0].text == 'pubdate'):
            news.publish_date = features[1].text
        if (features[0].text == 'parsingError'):
            news.parsingError = features[1].text

    for features in root.iter('Annotation'):
        if (features[0][1].text == 'title'):
            news.title = extract_markup(text_node, features.get('StartNode', 0), features.get('EndNode', 0), 'utf-8')
        if (features[0][1].text == 'description'):
            news.description = extract_markup(text_node, features.get('StartNode', 0), features.get('EndNode', 0),
                                              'utf-8')
        if (features[0][1].text == 'text'):
            news.text = extract_markup(text_node, features.get('StartNode', 0), features.get('EndNode', 0), 'utf-8')
            news.text = news.text.replace("\n", " ")

    # add topics if any
    filenameWithExtention = filename + '.xml'
    if filenameWithExtention in topics:
        news.topics = topics[filename + '.xml']

    # add annotations
    if filenameWithExtention in annotation:
        news.fiveWoneH = Object()
        for question in annotation[filenameWithExtention]:
            # print(question)
            questionAttribut = Object()
            setattr(news.fiveWoneH, question, questionAttribut)
            questionAttribut.annotated = []
            for tmpAnnotannoWithScore in annotation[filenameWithExtention][question]:
                tmp = Object()
                tmp.text = tmpAnnotannoWithScore[0]
                questionAttribut.annotated.append(tmp)

    news.origin = 'gate'
    news.filename = hashlib.sha224(news.url.encode('utf-8')).hexdigest() + '.json'

    outfile = open('output/' + news.filename, 'w', encoding='utf8')
    outfile.write(news.toJSON())
    outfile.close()

print("Done")
