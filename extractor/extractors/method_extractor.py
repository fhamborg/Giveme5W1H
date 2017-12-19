import enum
from enum import Enum

from document import Document
from extractor.candidate import Candidate
from extractor.extractors.abs_extractor import AbsExtractor


@enum.unique
class ExtensionStrategy(Enum):
    Range = 1
    Blacklist = 2


class MethodExtractor(AbsExtractor):
    """
    The MethodExtractor extracts the methods.
    """

    # CONJUNCTIONS IN ENGLISH: MEANING, TYPES AND USES, ISSN 2348-3164
    # http://grammarist.com/grammar/conjunctions/
    _copulative_conjunction = ['and', 'as', 'both', 'because', 'even', 'for', 'if ', 'that', 'then', 'since', 'seeing',
                               'so', 'after']

    # https://github.com/igorbrigadir/stopwords
    # https://github.com/igorbrigadir/stopwords/blob/master/en/nltk.txt
    _stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                   'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                   'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                   'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                   'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                   'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                   'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                   'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                   'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                   'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should',
                   'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn',
                   'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won',
                   'wouldn']

    _stop_ner = ['TIME', 'DATE', 'ORGANIZATION', 'DURATION', 'ORDINAL']

    # end of sentence, quote, PERIOD, COLON, QUOTE
    _blacklist = ['.', '"', '\'', ';']

    def __init__(self, weights: (float, float) = [1.0, 1.0, 1.0, 1.0],
                 extension_strategy: ExtensionStrategy = ExtensionStrategy.Blacklist, phrase_range: int = 3):
        """
        weights used in the candidate evaluation:
        (position, frequency, conjunction, adjectives/adverbs)
        :param weights: 
        """
        self.weights = weights
        self._extension_strategy = extension_strategy
        if extension_strategy is ExtensionStrategy.Range:
            self._phrase_range = phrase_range

    def _extract_candidates(self, document: Document):
        candidates = []
        postrees = document.get_trees()

        # Preposition or subordinating conjunction -> detecting verbs
        for i, tree in enumerate(postrees):
            for candidate in self._extract_tree_for_prepos_conjunctions(tree):
                candidates.append(candidate)
        candidates = self._filter_duplicates(candidates, exact=False)

        # candidate detection
        # All kind of adjectives
        candidates_ad = self._filter_duplicates(self._extract_ad_candidates(document), exact=False)

        # join the candidates
        candidates = candidates + candidates_ad

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
                right_sibling = subtree.right_sibling()

                # be sure there is more text on the right side of the tree
                if right_sibling:
                    # check if IN candidate is copulative(also known as addition)

                    # if subtree[0] in self._copulative_conjunction or subtree[0] not in self._prepositions_before:
                    if subtree[0]['nlpToken']['lemma'] in self._copulative_conjunction:
                        # candidate is after the preposition and

                        # if the right sibling (potential candidate) is an location or time
                        # the left sibling is taken as candidate
                        if right_sibling.leaves()[0]['nlpToken']['ner'] not in self._stop_ner:

                            tokens = right_sibling.root().stanfordCoreNLPResult['tokens']
                            _index = subtree[0]['nlpToken']['index'] + 1

                            if self._extension_strategy is ExtensionStrategy.Blacklist:

                                candidate_parts = []
                                for token in tokens[_index - 1:]:
                                    if token['lemma'] not in self._blacklist and token['ner'] not in self._stop_ner:
                                        candidate_parts.append(token)
                                    else:
                                        break

                            elif self._extension_strategy is ExtensionStrategy.Range:
                                candidate_parts = tokens[_index - 1:_index + self._phrase_range]

                            if candidate_parts:
                                # format fix
                                candidate_parts_fixed = []
                                for candidate_part in candidate_parts:
                                    candidate_parts_fixed.append(
                                        ({'nlpToken': candidate_part}, candidate_part['pos'], candidate_part))

                                # get the CoreNLP tokens for each part e.g lemmas etc.
                                # convert list objects back to tuples for backward compatibility
                                candidates.append([candidate_parts_fixed, None, _index, 'prepos'])

        return candidates

    def _extract_ad_candidates(self, document: Document):
        """
        :param document: The Document to be analyzed.
        :type document: Document

        :return: A List of Tuples containing all agents, actions and their position in the document.
        """

        # retrieve results from pre-processing
        candidates = []

        sentences = document.get_sentences()

        self._maxIndex = 0
        for sentence in sentences:
            for token in sentence['tokens']:
                if token['index'] > self._maxIndex:
                    self._maxIndex = token['index']
                if self._is_relevant_pos(token['pos']) and token['ner'] not in self._stop_ner:
                    candidates.append(
                        [[({'nlpToken': token}, token['pos'], token)], None, sentence['index'], 'adjectiv'])
        return candidates

    def _evaluate_candidates(self, document: Document):
        """
        :param document: The parsed document
        :type document: Document
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

            max_lemma = 0
            for part in candidate.get_parts():
                lemma = part[0]['nlpToken']['lemma']
                lemma_count = 0
                # ignore lemma count for stopwords, because they are very frequent
                if lemma not in self._stop_words:
                    lemma_count = lemma_map[lemma]
                if lemma_count > max_lemma:
                    max_lemma = lemma_count
                if lemma_count > global_max_lemma:
                    global_max_lemma = lemma_count
            # assign the greatest lemma to the candidate
            candidate.set_calculations('lemma_count', max_lemma)

        # normalize frequency (per lemma)
        for candidate in candidates:
            count = candidate.get_calculations('lemma_count')
            candidate.set_calculations('lemma_count_norm', count / global_max_lemma)

        # normalize position - reserved order
        sentences_count = len(document.get_sentences())
        for candidate in candidates:
            freq = (sentences_count - candidate.get_sentence_index()) / sentences_count
            candidate.set_calculations('position_frequency_norm', freq)

        # calculate score
        score_max = 0
        # weights_sum = sum(self.weights)
        for candidate in candidates:

            type_weight = 1
            if candidate.get_type() == 'adjectiv':
                type_weight = self.weights[2]
            elif candidate.get_type() == 'prepos':
                type_weight = self.weights[3]

            score = ((candidate.get_calculations('lemma_count_norm') * self.weights[1] +
                      candidate.get_calculations('position_frequency_norm') * self.weights[0]
                      ) + (1 * type_weight))
            candidate.set_score(score)
            if score > score_max:
                score_max = score

        # normalize score
        for candidate in candidates:
            score = candidate.get_score()
            candidate.set_score(score / score_max)

        candidates.sort(key=lambda x: x.get_score(), reverse=True)
        document.set_answer('how', self._fix_format(candidates))

    def _fix_format(self, candidates):
        '''
        helper to convert parts to the new format
        :param candidates:
        :return:
        '''
        result = []
        for candidate in candidates:
            ca = Candidate()
            parts = candidate.get_parts()
            parts_new = []
            for part in parts:
                parts_new.append((part[0], part[1]))
            ca.set_parts(parts_new)
            ca.set_sentence_index(candidate.get_sentence_index())
            ca.set_score(candidate.get_score())
            result.append(ca)
        return result

    def _find_vb_cc_vb_parts(self, relevant_parts):
        """
         walks though the given subtree and returns all parts which are a part of
         JJ VB [CC] JJ VB  chain, starting from the first word.

        :param relevant_parts:
        :return:
        """
        recording = False
        candidate_parts = []
        for relevant_part in relevant_parts:
            if relevant_part[1].startswith('VB') or relevant_part[1].startswith('JJ') or relevant_part[1].startswith(
                    'LS') or relevant_part[1] == 'CC':
                candidate_parts.append(relevant_part)
                recording = True
            elif recording is True:
                break
        candidate_parts_len = len(candidate_parts)

        # filter out short candidates
        if ((candidate_parts_len == 1 and candidate_parts[0][0]['nlpToken'][
            'lemma'] not in self._stop_words) or candidate_parts_len > 1):
            return candidate_parts
        return None

    def _is_relevant_pos(self, pos):
        # Is adjective or adverb
        if pos.startswith('JJ') or pos.startswith('RB'):
            return True
        else:
            return False
