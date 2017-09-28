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

    _copulative_conjunction = ['and', 'as', 'both', 'because', 'even', 'for', 'if ', 'that', 'then', 'since', 'seeing', 'so']
    _prepositions_before = ['in', 'with', 'until', 'as', 'during']
    _stop_words = ['and', 'is', 'has', 'have', 'went', 'was', 'been','were', 'am', 'get', 'said', 'are']

    #_tmp_statistic = {}

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

                if subtree[0] in  self._copulative_conjunction or subtree[0] not in self._prepositions_before:
                    # candidate is after the preposition

                    right_sibling = subtree.right_sibling()
                    # be  sure there is more text on the right side of the tree
                    if right_sibling:

                        right_sibling_pos = self._pos_linked_to_corenlp_tokens(right_sibling)
                        candidate_parts = self._find_vb_cc_vb_parts(right_sibling_pos)

                        if candidate_parts:
                            # get the CoreNLP tokens for each part e.g lemmas etc.
                            # convert list objects back to tuples for backward compatibility
                            candidates.append([candidate_parts, None, tree.stanfordCoreNLPResult['index'], 'prepos'])

                else:
                    # candidate is before the preposition
                    # ....derailed and overturned IN...

                    # matches VBD CC VBD and VBD
                    atree = subtree.parent().parent().parent()
                    if atree:
                        relevantParts = self._pos_linked_to_corenlp_tokens(atree)
                        candidate_parts = self._find_vb_cc_vb_parts(relevantParts)
                        if candidate_parts:
                            candidates.append([candidate_parts,None,tree.stanfordCoreNLPResult['index'], 'prepos'])

        return candidates



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
                if self._is_relevant_pos(token['pos']) and token['ner'] not in ['TIME', 'DATE', 'ORGANIZATION', 'DURATION', 'ORDINAL']:
                    candidates.append([[(token['originalText'],token['pos'], token)], None ,sentence['index'], 'adjectiv'])
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
            for part in candidate.get_parts():
                lemma = part[2]['lemma']
                lemma_count = 0
                if lemma not in ['so','due', 'well', 'very', 'on', 'too', 'be', 'i', 'is', 'and', 'have', 'the', 'a', ',', '.', '', 'not', "n't", 'am', 'as', 'even', 'however', 'other', 'just', 'over', 'more']:
                    lemma_count = lemma_map[lemma]
                if lemma_count > maxLemma:
                    maxLemma = lemma_count
                if lemma_count > global_max_lemma:
                    global_max_lemma = lemma_count
            # assigme the greatest lemma to the candidate
            candidate.set_calculations('lemma_count', maxLemma)

        # normalize frequency (per lemma)
        for candidate in candidates:
            count = candidate.get_calculations('lemma_count')
            candidate.set_calculations('lemma_count_norm', count / global_max_lemma)

        # normalize position - reserved order
        sentences_count = len(document.get_sentences())
        for candidate in candidates:
            freq = (sentences_count - candidate.get_sentence_index()) / sentences_count
            candidate.set_calculations('position_frequency_norm', freq)

        # callculate score
        score_max = 0
        weights_sum = sum(self.weights)
        for candidate in candidates:
            score = ((candidate.get_calculations('lemma_count_norm') * self.weights[1] +
                      candidate.get_calculations('position_frequency_norm') * self.weights[0]
                      ) / weights_sum)
            candidate.set_score(score)
            if score > score_max:
                score_max = score

        # normalize score
        for candidate in candidates:
            score = candidate.get_score()
            candidate.set_score(score / score_max)

        candidates.sort(key=lambda x: x.get_score(), reverse=True)
        document.set_answer('how', candidates)

    def _convert_to_object_oriented_list(self, list):

        list = self._filter_duplicates(list)
        return list
        #whoList = []
        # for answer in list:
        #for answer in self._filter_duplicates(list):
        #    ca = Candidate()
        #    ca.set_parts(answer[0])
        #    ca.set_sentence_index(answer[1])
        #    ca.set_type(answer[2])
        #    whoList.append(ca)
        #return whoList

    def _find_vb_cc_vb_parts(self, relevantParts):
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
        if ((candidatePartsLen == 1 and candidateParts[0][0] not in self._stop_words) or candidatePartsLen > 1):
            return candidateParts
        return None

    def _count_elements(self, root):
        count = 0
        if isinstance(root, list):
            for element in root:
                if isinstance(element, list):
                    count += self._count_elements(element)
                else:
                    count += 1
        else:
            count += 1
        return count

    def _is_relevant_pos(self, pos):

        # Is adjectivs or adverb
        if pos.startswith('JJ') or pos.startswith('RB'):
            return True
        else:
            return False

""""
1	  of	1761
2	  in	1667
3	  on	890
4	  for	716
5	  with	622
6	  at	538
7	  as	497
8	  that	414
9	  after	374
10	  from	330
11	  by	316
12	  into	181
13	  about	137
14	  before	123
15	  than	114
16	  during	111
17	  over	110
18	  while	99
19	  like	96
20	  since	84
21	  if	82
22	  around	80
23	  between	79
24	  because	61
25	  against	61
26	  near	56
27	  out	55
28	  outside	42
29	  through	35
30	  whether	34
31	  across	34
32	  behind	31
33	  among	31
34	  until	24
35	  without	23
36	  under	22
37	  despite	22
38	  onto	21
39	  inside	19
40	  off	18
41	  down	17
42	  though	16
43	  alongside	15
44	  so	14
45	  within	13
46	  up	11
47	  although	11
48	  throughout	10
49	  along	10
50	  towards	8
51	  above	8
52	  ago	7
53	  per	6
54	  via	5
55	  beyond	5
56	  toward	4
57	  upon	4
58	  whilst	3
59	  next	3
60	  underneath	3
61	  beside	3
62	  unlike	3
63	  !!	2
64	  amid	2
65	  save	2
66	  past	2
67	  amongst	1
68	  except	1
69	  below	1
70	  unless	1
71	  en	1
72	  aboard	1
73	  once	1
74	  atop	1

"""