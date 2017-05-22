import  json
import ntpath


def path_leaf(path):
        """
        helper to get the filename from a path
        """
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)
    
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
        
class JSONWriter:
    
   

    def __init__(self, path):
        """
        A simple json writer for saving results.  

        :param path: Absolute path to the file
        """
        self.path = path
        self.outfile = open(self.path, 'w')
        self.outfile.write('[')
        self.isEmpty = True
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer = None
        self.path = None
        self.outfile.write(']');
        self.outfile.close()
        

    def save_document(self, document, n=3):
        """
        Saves the first n 5Ws answers to a json file.

        :param document: The parsed Document
        :type document: Document
        :param n: Number of candidates to save
        :type n: Integer

        :return: None
        """
        if self.isEmpty: 
            self.isEmpty = False
        else: 
            self.outfile.write(',');
            
        output = Object();
        output.title = document.get_title()
        output.filename = path_leaf(document.get_path())
        output.metadata = Object();
        output.metadata.pubdate = document.get_date()
        output.metadata.source = document.get_source()
        
        
        doc_annotation = document.get_annotations()
        
        #Answer 
        answers = document.get_answers()   
        output.fiveWoneH = Object()
        for index, question in enumerate(answers):
            questionAttribut = Object()
            setattr(output.fiveWoneH, question, questionAttribut)
            
            # Add annotation for this question 
            questionAttribut.annotations = []
            questionAnnotation = doc_annotation.get(question,None)
            if questionAnnotation is not None:
                for an in doc_annotation.get(question,None):
                    questionAttribut.annotations.append(an[2])
                
            # Add answers for this question
            questionAttribut.extracted = []
            for index, key in enumerate(answers[question]):
                candidate = answers[question][index]
                if index >= n:
                    break
                candidateJson = Object()
                candidateJson.score = candidate[1]
                candidateJson.words = candidate[0]
                questionAttribut.extracted.append(candidateJson)
                 
        self.outfile.write(output.toJSON());