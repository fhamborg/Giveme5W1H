import re

from nltk.tree import ParentedTree

from .abs_extractor import AbsExtractor
from extractor.extractors.candidate import Candidate

class MethodExtractor(AbsExtractor):
    """
    The MethodExtractor tries to extract the methods.
    """

    # weights used in the candidate evaluation:
    # (position, frequency, named entity)
    # weights = (4, 3, 2)
    weights = [1,1,1]

    # relevant indicators
    preposition = ['with', 'in', 'by', 'after']
    conjunction = ['as', 'because', 'so', 'until', 'while']
    pattern= ['NN-VBD', 'NN-VBZ', 'VBN-VBN']

    # prepositional phrase PP, preposition

    def extract(self, document):
        """
        Parses the document for answers to the questions how.

        :param document: The Document object to parse
        :type document: Document

        :return: The parsed Document object
        """

        self._extract_candidates(document)
        self._evaluate_candidates(document)
        
        return document

    def _extract_candidates(self, document):

        candidates = []
        postrees = document.get_trees()

        # Preposition or subordinating conjunction -> detecting verbs
        for i, tree in enumerate(postrees):
            for candidate in self._evaluate_tree(tree):
                    candidates.append(candidate)
        candidates = self._filterAndConvertToObjectOrientedList(candidates)

        # All kind of adjectives
        candidates = candidates + self._filterAndConvertToObjectOrientedList(self._extract_ad_candidates(document))

        document.set_candidates('MethodExtractor', candidates)

    def _evaluate_tree(self, tree):


        # in: before
        # after: after
        candidates = []
        for subtree in tree.subtrees():
            label = subtree.label()

            # Preposition or subordinating conjunction -> detecting verbs
            # ...after it "came off the tracks"...
            if label == 'IN':

                # after can be followed by a candidate
                # TODO list all prepositions depending on where candidates can be found (before or after)
                if subtree[0] in ['after']:
                    # candidate is after the preposition

                    right_sibling_pos = subtree.right_sibling()
                    # be  sure there is more text on the right side of the tree
                    if right_sibling_pos:
                        right_sibling_pos = right_sibling_pos.pos()
                        candidate_parts = self._findString(right_sibling_pos)
                        if candidate_parts:
                            candidates.append([candidate_parts, tree.stanfordCoreNLPResult['index']])

                else:
                    # candidate is before the preposition
                    # ....derailed and overturned IN...

                    # match VBD CC VBD and VBD
                    relevantParts = subtree.parent().parent().parent().pos()
                    candidate_parts = self._findString(relevantParts)
                    if candidate_parts:
                        candidates.append([candidate_parts, tree.stanfordCoreNLPResult['index']])

        return candidates

    def _filterAndConvertToObjectOrientedList(self, list):
        whoList = []
        for answer in self._filter_duplicates(list):
            ca = Candidate()
            ca.setParts(answer[0])
            ca.setIndex(answer[1])
            whoList.append(ca)
        return whoList


    def _findString(self, relevantParts):
        recording = False
        candidateParts = []
        for relevantPart in relevantParts:
            if relevantPart[1].startswith('VB') or relevantPart[1] == 'CC':
                candidateParts.append(relevantPart)
                recording = True
            elif recording is True:
                break
        candidatePartsLen = len(candidateParts)

        # filter out short candidates
        if ((candidatePartsLen == 1 and candidateParts[0][0] not in ['and', 'is', 'has', 'have', 'went', 'was', 'been', 'were', 'am', 'get', 'said','are']) or candidatePartsLen > 1):
            return candidateParts
        return None


    def _extract_ad_candidates(self, document):
        """
        :param document: The Document to be analyzed.
        :type document: Document

        :return: A List of Tuples containing all agents, actions and their position in the document.
        """

        # retrieve results from preprocessing
        candidates = []

        tmp_candidates = []
        sentences = document.get_sentences()

        self._maxIndex = 0
        for sentence in sentences:
            for token in sentence['tokens']:
                if token['index'] > self._maxIndex:
                    self._maxIndex = token['index']
                if self._isRelevantPos(token['pos']) and token['ner'] not in ['TIME', 'DATE', 'ORGANIZATION', 'DURATION', 'ORDINAL']:
                    candidates.append( [[(token['pos'], token['originalText'], token['lemma'])], sentence['index']] )

        return candidates


    def _evaluate_candidates(self, document):
        """
        :param document: The parsed document
        :type document: Document
        :param candidates: Extracted candidates to evaluate.
        :type candidates:[([(String,String)], ([(String,String)])]
        :return: A list of evaluated and ranked candidates
        """
        #ranked_candidates = []
        document.set_answer('how', document.get_candidates('MethodExtractor'))
          
        groupe_per_lemma = {}
        maxCount = 0
        
        candidates = document.get_candidates('MethodExtractor')

        if candidates and len(candidates) == -1:
            # frequency per lemma
            for candidate in candidates:
                if candidate is not None and len(candidate['originalText']) > 0:
                    lema_count = groupe_per_lemma.get(candidate["lemma"], 0 )
                    lema_count += 1

                    if lema_count > maxCount:
                        maxCount = lema_count
                    groupe_per_lemma[candidate["lemma"]] = lema_count

            # transfer count per lemmaGroup to candidates
            for candidate in candidates:
                if candidate is not None and len(candidate['originalText']) > 0:

                    # save normalized frequency
                    candidate['frequency'] = groupe_per_lemma[candidate['lemma']]
                    if maxCount-1 > 0:
                        candidate['frequencyNorm'] = ( candidate['frequency'] - 1 ) / (maxCount-1)
                    else:
                        # there is just one candidate
                        candidate['frequencyNorm'] = 1
                    lema_count = groupe_per_lemma.get(candidate["lemma"], 0 )

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




            result = []
            for candidate in new_list:
                keyVal = ([( candidate['originalText'], candidate['pos'])], candidate['score'] )
                result.append( keyVal )





    def _isRelevantPos(self, pos):
       
        # Is adjectivs or adverb
        if pos.startswith('JJ') or pos.startswith('RB'):
            return True
        else:
            return False




