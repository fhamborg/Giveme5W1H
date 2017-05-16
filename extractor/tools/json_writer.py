import  json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
       
        
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
        output.metadata = Object();
        output.metadata.title = document.get_title()   
        output.metadata.pubdate = document.get_date()
        
        # Annotations
        output.annotations = Object();
        doc_annotation = document.get_annotations()
        
        for question in doc_annotation:
            annotations = []
            for an in doc_annotation[question]:
                annotations.append(an[2])
            setattr(output.annotations, question, annotations)
        # Answer 
        output.answers = Object()
        answers = document.get_answers()
        for index, question in enumerate(answers):
            candidates = [];
            for candidate in answers[question]:
                candidateJson = Object()
                candidateJson.score = candidate[1]
                # one object to hold all findings 
                candidateJson.found = Object()
                for index, key in enumerate(candidate[0]):
                    # index as prefix to keep track of the order
                    jsonkey = str(index).zfill(3) + '_' + key[1]
                    setattr(candidateJson.found, jsonkey, key[0])
                    if index >= n:
                        break
                candidateJson.found = candidateJson.found
                candidates.append(candidateJson)
            setattr(output.answers, question, candidates)
        self.outfile.write(output.toJSON());