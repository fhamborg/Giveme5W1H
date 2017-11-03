import logging
import os
import sys
import json
import glob
import xml.etree.ElementTree as ET
import copy
import html
import re


from twisted.python.util import println

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
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2, ensure_ascii=False)
    
    
# get topic file
println("Starting converting")


topics = {}
fileTopics = open('input/index.txt', 'r')

for topic in fileTopics.read().split('#'):
    parts = topic.split('\n')
    topicCandidate  = parts.pop(0);
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
    
    #Output Object
    news = Object()
    news.metadata = Object()
   
    news.fiveWoneH = Object()
    for features in root.iter('Feature'):
        if(features[0].text == 'MimeType'):
            news.metadata.mimeType = features[1].text
        if(features[0].text == 'source'):
            news.metadata.source = features[1].text  
        if(features[0].text == 'pubdate'):
            news.metadata.pubdate = features[1].text
        if(features[0].text == 'parsingError'):
            news.metadata.parsingError = features[1].text  
        
    for features in root.iter('Annotation'):
        if(features[0][1].text == 'title'):
            news.title = extract_markup(text_node, features.get('StartNode', 0), features.get('EndNode', 0), 'utf-8')
        if(features[0][1].text == 'description'):
            news.description = extract_markup(text_node, features.get('StartNode', 0), features.get('EndNode', 0), 'utf-8')    
        if(features[0][1].text == 'text'):
            news.text = extract_markup(text_node, features.get('StartNode', 0), features.get('EndNode', 0), 'utf-8')    
            news.text = news.text.replace("\n", " ")
            
    # get a nice to readable publisher from the url         
    if('www' in news.metadata.source):
        firstDot = news.metadata.source.index('.')+1
    else:
        firstDot = news.metadata.source.index('//')+2
    news.metadata.publisher = news.metadata.source[firstDot:]
    #print(news.metadata.publisher) 
    news.metadata.publisher = news.metadata.publisher[:news.metadata.publisher.index('.')]
    
    # get text
   
    #news.text = html.unescape(ET.tostring(text_node, method='text').decode('UTF-8')).replace("\n", " ")
    
    # add topics if any
    filenameWithExtention = filename + '.xml'
    if filenameWithExtention in topics:
        news.metadata.topics = topics[filename + '.xml']
    
    # add annotations
    if filenameWithExtention in annotation:
        news.fiveWoneH = Object()
        for question in annotation[filenameWithExtention]:
            #print(question)
            questionAttribut = Object()
            setattr(news.fiveWoneH, question, questionAttribut)
            questionAttribut.annotated = []
            for tmpAnnotannoWithScore in annotation[filenameWithExtention][question]:
                questionAttribut.annotated.append(tmpAnnotannoWithScore[0])
                
            #news.fiveWoneH = annotation[filenameWithExtention]
        
    news.metadata.filename  = news.metadata.pubdate.replace(' ','T').replace(':','') +'_'+ news.metadata.publisher + '_' + re.sub('[^a-zA-Z0-9]', '', news.title.replace(' ',''))[0:15] 
    print(news.toJSON())
    #write it out
    outfile = open('output/'+ news.metadata.filename   + '.json', 'w', encoding='utf8')
    outfile.write(news.toJSON())
    outfile.close()
    #print(filename)

println("Done")
