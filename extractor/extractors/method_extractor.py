from candidate import Candidate
from .abs_extractor import AbsExtractor


class MethodExtractor(AbsExtractor):
    """
    The MethodExtractor tries to extract the methods.
    """

    # weights used in the candidate evaluation:
    # (position, frequency)
    # weights = (4, 3)
    weights = [1.0, 1]

    # relevant indicators
    preposition = ['with', 'in', 'by', 'after']
    conjunction = ['as', 'because', 'so', 'until', 'while']
    pattern = ['NN-VBD', 'NN-VBZ', 'VBN-VBN']

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
            for candidate in self._extract_tree_for_prepos_conjunctions(tree):
                candidates.append(candidate)
        candidates = self._convert_to_object_oriented_list(candidates)

        # All kind of adjectives
        candidatesAd = self._convert_to_object_oriented_list(self._extract_ad_candidates(document))


        # join the candidates
        candidates = candidates + candidatesAd

        # save them to the document
        document.set_candidates('MethodExtractor', candidates)

    def _extract_tree_for_prepos_conjunctions(self, tree):

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

                    right_sibling = subtree.right_sibling()
                    # be  sure there is more text on the right side of the tree
                    if right_sibling:

                        right_sibling_pos = self._pos_linked_to_corenlp_tokens(right_sibling)

                        candidate_parts = self._find_VB_CC_VB_Parts(right_sibling_pos)

                        if candidate_parts:

                            # get the CoreNLP tokens for each part e.g lemmas etc.

                            # convert list objects back to tuples for backward compatibility

                            candidates.append([candidate_parts, tree.stanfordCoreNLPResult['index'], 'prepos'])

                else:
                    # candidate is before the preposition
                    # ....derailed and overturned IN...

                    # matches VBD CC VBD and VBD
                    atree = subtree.parent().parent().parent()

                    relevantParts = self._pos_linked_to_corenlp_tokens(atree)
                    candidate_parts = self._find_VB_CC_VB_Parts(relevantParts)
                    if candidate_parts:
                        candidates.append([candidate_parts, tree.stanfordCoreNLPResult['index'], 'prepos'])

        return candidates

    def _pos_linked_to_corenlp_tokens(self, tree):
        root = tree.root()
        pos = tree.pos()
        candidate_parts_as_list = []
        startIndex = self._findIndexFromRoot(tree.root(), list(tree.treeposition())) -1
        for x in range(0, len(pos)):
            # convert part tuple to list, get token
            token = root.stanfordCoreNLPResult['tokens'][x + startIndex]
            partsAsList = list(pos[x])
            partsAsList.append(token)
            # save list
            candidate_parts_as_list.append(partsAsList)
        return [tuple(x) for x in candidate_parts_as_list]


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
                if self._isRelevantPos(token['pos']) and token['ner'] not in ['TIME', 'DATE', 'ORGANIZATION',
                                                                              'DURATION', 'ORDINAL']:


                    candidates.append([[(token['pos'], token['originalText'], token)], sentence['index'], 'adjectiv'])

        return candidates

    def _evaluate_candidates(self, document):
        """
        :param document: The parsed document
        :type document: Document
        :param candidates: Extracted candidates to evaluate.
        :type candidates:[([(String,String)], ([(String,String)])]
        :return: A list of evaluated and ranked candidates
        """
        # ranked_candidates = []
        candidates = document.get_candidates('MethodExtractor')
        lemma_map = document.get_lemma_map()

        # find lemma count per candidate, consider only the the greatest count per candidate
        # (each candidate is/can be a phrase and therefore, has multiple words)
        global_max_lemma = 0
        for candidate in candidates:

            # remove any prev. calculations
            candidate.reset_calculations()

            maxLemma = 0
            for part in candidate.getParts():
                lemma = part[2]['lemma']
                lemma_count = 0
                if lemma not in ['be', 'i', 'is', 'and', 'have', 'the', 'a', ',', '.', '']:
                    lemma_count = lemma_map[lemma]
                if lemma_count > maxLemma:
                    maxLemma = lemma_count
                if lemma_count > global_max_lemma:
                    global_max_lemma = lemma_count
            # assigme the greatest lemma to the candidate
            candidate.set_calculations('lemma_count', maxLemma)
            #candidate.set_lemma_count(maxLemma)

        # normalize frequency (per lemma)
        for candidate in candidates:
            count = candidate.get_calculations('lemma_count')
            candidate.set_calculations('lemma_count_norm', count /global_max_lemma)
            #print(candidate.get_calculations('lemma_count_norm'))

        # normalize position - reserved order
        sentences_count = len(document.get_sentences())
        for candidate in candidates:
            freq = (sentences_count - candidate.get_sentence_Index()) / sentences_count
            candidate.set_calculations('position_frequency_norm', freq )
            #print(candidate.get_calculations('position_frequency_norm'))
            #print(candidate.get_sentence_Index())
            #print('')

        # callculate score
        score_max = 0
        weights_sum = sum(self.weights)
        for candidate in candidates:
            score = ((candidate.get_calculations('lemma_count_norm') * self.weights[1] +
                      candidate.get_calculations('position_frequency_norm') * self.weights[0]
                        )/ weights_sum)
            candidate.setScore(score)
            if score > score_max:
                score_max = score

        #normalize score
        for candidate in candidates:
            score = candidate.getScore()
            candidate.setScore(score/score_max)
            #print(candidate.getScore())

        candidates.sort(key=lambda x: x.getScore(), reverse=True)
        document.set_answer('how', candidates)


    # removed filter because of frequency
    def _convert_to_object_oriented_list(self, list):
        whoList = []
        #for answer in list:
        for answer in self._filter_duplicates(list):
            ca = Candidate()
            ca.setParts(answer[0])
            ca.set_sentence_Index(answer[1])
            ca.setType(answer[2])
            whoList.append(ca)
        return whoList

    def _find_VB_CC_VB_Parts(self, relevantParts):
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
        if ((candidatePartsLen == 1 and candidateParts[0][0] not in ['and', 'is', 'has', 'have', 'went', 'was', 'been',
                                                                     'were', 'am', 'get', 'said',
                                                                     'are']) or candidatePartsLen > 1):
            return candidateParts
        return None




    def _findIndexFromRoot(self, root, path):

       if(len(path) > 1):
            position = path.pop(0)
            leftChildCount = 0
            for x in range(0, position):
                 leftChildCount = leftChildCount + self._countElements(root[x])
            return leftChildCount + self._findIndexFromRoot(root[position], path)
       elif (len(path) is 1):
            return path.pop(0)+1
       else:
            return 0

    def _countElements(self, root):
        count = 0
        if isinstance(root, list):
            for element in root:
                if isinstance(element, list):
                    count += self._countElements(element)
                else:
                    count += 1
        else:
            count += 1
        return count


    def _isRelevantPos(self, pos):

        # Is adjectivs or adverb
        if pos.startswith('JJ') or pos.startswith('RB'):
            return True
        else:
            return False
