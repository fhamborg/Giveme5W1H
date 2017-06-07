import re
from nltk.tree import ParentedTree
from .abs_extractor import AbsExtractor


class MethodExtractor(AbsExtractor):
    """
    The MethodExtractor tries to extract the methods.
    """

    # weights used in the candidate evaluation:
    # (position, frequency, named entity)
    # weights = (4, 3, 2)

    def extract(self, document):
        """
        Parses the document for answers to the questions how.

        :param document: The Document object to parse
        :type document: Document

        :return: The parsed Document object
        """
        self.weights = [1,1,1]
        self._candidates = []
        candidates = self._extract_candidates(document)
        #print(candidates)
        candidates = self._evaluate_candidates(document, candidates)
        document.set_answer('how', [])



    def _extract_candidates(self, document):
        """
    

        :param document: The Document to be analyzed.
        :type document: Document

        :return: A List of Tuples containing all agents, actions and their position in the document.
        """

        # retrieve results from preprocessing
        corefs = document.get_corefs()
        trees = document.get_trees()
        candidates = []
        
        tmp_candidates = []
        sentences = document.get_sentences()
        
        # is used for normalisation
        self._maxIndex = 0
        for sentence in sentences:
            for token in sentence['tokens']:
                if token['index'] > self._maxIndex:
                    self._maxIndex = token['index']
                if self._isRelevantPos(token['pos']):
                    # TODO some further checks based on relations
                    print(token['pos'])
                    
                    # TODO exclude if ner tags is time, location...
                    
                    
                    # save all relevant information for _evaluate_candidates
                    # position, lema, word itslef,  
                    candidates.append({ 'position': token['index'], 'lemma': token['lemma'], 'originalText':token['originalText']  })
                
        return candidates


    

    def _evaluate_candidates(self, document, candidates):
        """
        :param document: The parsed document
        :type document: Document
        :param candidates: Extracted candidates to evaluate.
        :type candidates:[([(String,String)], ([(String,String)])]
        :return: A list of evaluated and ranked candidates
        """
        #ranked_candidates = []
        
        
        # 1. position in text
        # score = self.weights[0] * (document_lenght-candidate['position']) / document_lenght
        

        
        groupePerLemma = {}
        maxCount = 0
        # group per lemma
        for candidate in candidates:
            if candidate is not None and len(candidate['originalText']) > 0:
                lemaCount = groupePerLemma.get(candidate["lemma"], 0 )
                lemaCount += 1
                
                if lemaCount > maxCount:
                    maxCount = lemaCount
                groupePerLemma[candidate["lemma"]] = lemaCount
                
        # transfer count per lemma group to candidates
        for candidate in candidates:
            if candidate is not None and len(candidate['originalText']) > 0:
                
                # save normalized frequency
                candidate['frequencyNorm'] = ( groupePerLemma[candidate['lemma']] - 1 ) / (maxCount-1)
                lemaCount = groupePerLemma.get(candidate["lemma"], 0 )
                
                #  normalized position
                candidate['positionNorm'] = (self._maxIndex -  candidate['position']) / self._maxIndex

    
        # scoring
        for candidate in candidates:
            candidate['score'] =  candidate['frequencyNorm'] * self.weights[1] +  candidate['positionNorm'] * self.weights[0] 
        
       
        # sort candidates accoring to the scoring
        #candidate.sort(key=lambda x: x.score, reverse=True)
        #sorted(candidate.keys(), key=lambda candidate: candidate.score)
        candidates.sort(key = lambda x: x['score'])
        print(candidates)
        return candidate

    def _isRelevantPos(self, pos):
       
        # Is adjectivs or adverb
        if pos.startswith('JJ') or pos.startswith('RB'):
            return True
        else:
            return False




