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
        
        candidates = self._extract_candidates(document)
        candidates = self._evaluate_candidates(document, candidates)
        
        
        #convert candidates into correct format
        #print(candidates)
        result = []
        for candidate in candidates:
            keyVal = ([( candidate['originalText'], candidate['pos'])], candidate['score'] )
            result.append( keyVal )
        document.set_answer('how', result )
        print(result)

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
                    # print(token['pos'])
                    
                    # TODO exclude if ner tags is time, location...
                    
                    # TODO extend candidates to phrases
                    
                    # save all relevant information for _evaluate_candidates  
                    candidates.append({ 'position': token['index'], 'lemma': token['lemma'], 'originalText':token['originalText'], 'pos' : token['pos']   })
                
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
        
          
        groupePerLemma = {}
        maxCount = 0
        
        # frequency per lemma
        for candidate in candidates:
            if candidate is not None and len(candidate['originalText']) > 0:
                lemaCount = groupePerLemma.get(candidate["lemma"], 0 )
                lemaCount += 1
                
                if lemaCount > maxCount:
                    maxCount = lemaCount
                groupePerLemma[candidate["lemma"]] = lemaCount
                
        # transfer count per lemmaGroup to candidates 
        for candidate in candidates:
            if candidate is not None and len(candidate['originalText']) > 0:
                
                # save normalized frequency
                candidate['frequency'] = groupePerLemma[candidate['lemma']]
                candidate['frequencyNorm'] = ( candidate['frequency'] - 1 ) / (maxCount-1)
                lemaCount = groupePerLemma.get(candidate["lemma"], 0 )
                
                # normalized position
                candidate['positionNorm'] = (self._maxIndex -  candidate['position']) / self._maxIndex

    
        # scoring
        scoreMax = 0 
        for candidate in candidates:
            candidate['score'] =  candidate['positionNorm'] * self.weights[0] + candidate['frequencyNorm'] * self.weights[1]
            if candidate['score'] > scoreMax:
                    scoreMax = candidate['score']
                    
        # normalizing scores
        for candidate in candidates:
            candidate['score'] = candidate['score']/scoreMax
        # Sort candidates
        candidates.sort(key = lambda x: x['score'], reverse=True)
        
        # delete duplicates
        # - frequency already used used for scoring, so only best scored candidate must be returned
        alreadySaveLemma = {}
        new_list = []
        for candidate in candidates:
            if candidate['lemma'] not in alreadySaveLemma:
                alreadySaveLemma[candidate['lemma']] = True
                new_list.append(candidate)
        
        return new_list

    def _isRelevantPos(self, pos):
       
        # Is adjectivs or adverb
        if pos.startswith('JJ') or pos.startswith('RB'):
            return True
        else:
            return False




