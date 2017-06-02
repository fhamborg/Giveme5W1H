import json
import hashlib

class Writer:
    def __init__(self, outputDirectory, rewriteFilename=True):
        """
        :param path: Absolute path to the output directory
        """
        self.outputDirectory = outputDirectory
        self.rewriteFilename = rewriteFilename
        
    def __enter__(self):
        return self
        
    def writeJson(self, outputObject):
        outfile = open(self.outputDirectory +'/'+ outputObject['filename'], 'w')
        outfile.write( json.dumps(outputObject, sort_keys=False, indent=2))
        outfile.close()
        
    def write(self, document, n=0.8, f=False):
        """

        :param document: The parsed Document
        :type document: Document

        :return: None
        """     
        # reuse the input json as template for the output json
        output = document.get_rawData()

        print(output)
        if self.rewriteFilename:
            output['filename'] = hashlib.sha256(output['url'].encode('utf-8')).hexdigest()
            
        # check if there isn`t already a fiveWoneH literal
        fiveWoneHLiteral =  output.setdefault('fiveWoneH',{})
        
        #Extract answer
        answers = document.get_answers()
        for index, question in enumerate(answers):
            # check if question literal is there
            questionLiteral =  fiveWoneHLiteral.setdefault(question,{ 'annotated': None, 'extracted': []})
            # check if extracted literal is there
            extractedLiteral = questionLiteral.setdefault(question,[])
            for index, key in enumerate(answers[question]):
                candidate = answers[question][index]
                candidateJson = {'score': candidate[1], 'words': []}
                if candidateJson.score <= n:
                    break
                if f:
                    candidateJson['words'] = { 'text':candidate[0], 'tag':candidate[1]}
                extractedLiteral.append(candidateJson)
        self.writeJson(output)
        
            
#print(questionLiteral)
        
        #output.metadata = Object();
        #output.metadata.pubdate = document.get_date()
        #output.metadata.source = document.get_source()
        
#         doc_annotation = document.get_annotations()
#         
#         #Answer 
#         answers = document.get_answers()   
#         output.fiveWoneH = Object()
#         for index, question in enumerate(answers):
#             questionAttribut = Object()
#             setattr(output.fiveWoneH, question, questionAttribut)
#             
#             # Add annotation for this question 
#             questionAttribut.annotations = []
#             questionAnnotation = doc_annotation.get(question,None)
#             if questionAnnotation is not None:
#                 for an in doc_annotation.get(question,None):
#                     questionAttribut.annotations.append(an[2])
#                 
#             # Add answers for this question
#             questionAttribut.extracted = []
#             for index, key in enumerate(answers[question]):
#                 candidate = answers[question][index]
#                 candidateJson = Object()
#                 candidateJson.score = candidate[1]
#                 
#                 if candidateJson.score <= n:
#                     break
#                 if f:
#                     candidateJson.words = candidate[0]
#                 else:    
#                     candidateJson.words = candidate[0]
#                 questionAttribut.extracted.append(candidateJson)
#                  
        #self.writeJson.write(output.toJSON());