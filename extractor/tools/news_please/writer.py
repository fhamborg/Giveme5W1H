import json
import hashlib

class Writer:
    def __init__(self, rewriteFilename=True):
        """
        :param path: Absolute path to the output directory
        """
        self.rewriteFilename = rewriteFilename
        
    def __enter__(self):
        return self
        
    def _writeJson(self, outputPath, outputObject):
        outfile = open(outputPath +'/'+ outputObject['filename'], 'w')
        outfile.write( json.dumps(outputObject, sort_keys=False, indent=2))
        outfile.close()
        
    def write(self, outputPath , document):
        """
        :param document: The parsed Document
        :type document: Document

        :return: None
        """     
        # reuse the input json as template for the output json
        output = document.get_rawData()

        #print(output)
        if self.rewriteFilename:
            output['filename'] = hashlib.sha224(output['url'].encode('utf-8')).hexdigest() + '.json'
         
        # check if there isn`t already a fiveWoneH literal
        fiveWoneHLiteral =  output.setdefault('fiveWoneH',{})
        
        #Extract answers
        answers = document.get_answers()
        for index, question in enumerate(answers):
            # check if question literal is there
            questionLiteral =  fiveWoneHLiteral.setdefault(question,{ 'annotated': None, 'extracted': []})
            # check if extracted literal is there 
            extractedLiteral = questionLiteral.setdefault('extracted',[])
            for index, key in enumerate(answers[question]):
                candidate = answers[question][index]
                candidateJson = {'score': candidate[1], 'words': []}
                #if candidateJson.score <= n:
                #    break
                candidateJson['words'] = { 'text':candidate[0], 'tag':candidate[1]}
                extractedLiteral.append(candidateJson)
        self._writeJson(outputPath, output)