import enum
from enum import Enum

from extractor.document import Document
from extractor.candidate import Candidate
from extractor.extractors.abs_extractor import AbsExtractor


@enum.unique
class ExtensionStrategy(Enum):
    Range = 1
    Blacklist = 2
    Blacklist_Max_Range = 3


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
    # enhance by punctuation marks
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
                   'wouldn', ':', '.', '"', ';', ',', '\'']

    _stop_ner = ['TIME', 'DATE', 'ORGANIZATION', 'DURATION', 'ORDINAL']

    # end of sentence, quote, PERIOD, COLON, QUOTE
    _blacklist = ['.', '"', '\'', ';']

    def __init__(self, weights: (float, float, float, float) = [0.228, 0.139, 0.633, 0.266],
                 extension_strategy: ExtensionStrategy = ExtensionStrategy.Blacklist_Max_Range, phrase_range: int = 10, discard_threshold = 0.2):
        """
        weights used in the candidate evaluation:
        (position, frequency, conjunction, adjectives/adverbs)
        :param weights: 
        """
        self.weights = weights
        self._extension_strategy = extension_strategy
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

                    # if subtree[0] in self._copulative_conjunction
                    if subtree[0]['nlpToken']['lemma'] in self._copulative_conjunction:

                        # if the right sibling (potential candidate) is not an in _stop_ner (location, time..)
                        if right_sibling.leaves()[0]['nlpToken']['ner'] not in self._stop_ner:

                            tokens = right_sibling.root().stanfordCoreNLPResult['tokens']
                            _index = subtree[0]['nlpToken']['index'] + 1

                            if self._extension_strategy is ExtensionStrategy.Blacklist or self._extension_strategy is ExtensionStrategy.Blacklist_Max_Range:

                                candidate_parts = []
                                _range = 0
                                # walk over the sentence, starting after the indicator
                                for token in tokens[_index - 1:]:
                                    if token['lemma'] not in self._blacklist and token['ner'] not in self._stop_ner:

                                        if self._extension_strategy is ExtensionStrategy.Blacklist_Max_Range and self._phrase_range <= _range:
                                            break

                                        candidate_parts.append(token)
                                        _range = _range + 1
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

        #self._maxIndex = 0
        for sentence in sentences:
            for i,token in enumerate(sentence['tokens']):
                #if token['index'] > self._maxIndex:
                #    self._maxIndex = token['index']
                if self._is_relevant_pos(token['pos']) and \
                        token['ner'] not in self._stop_ner and\
                        token['lemma'] not in self._stop_words:

                    if i == 0:
                        start = i
                    else:
                        start = i-1


                    # expand finding
                    if self._extension_strategy is ExtensionStrategy.Range:
                            tokens = sentence['tokens'][start: self._phrase_range]
                    elif self._extension_strategy is ExtensionStrategy.Blacklist_Max_Range:
                        # test
                        # walk fixed range
                        tokens = []
                        for i in range(start, self._phrase_range  + start):

                            if i == start and (sentence['tokens'][i]['lemma'] in self._blacklist or sentence['tokens'][i]['lemma'] == ':'):
                                # ignore first word if a step back would hit a blacklist word # derailed: Several ....
                                continue
                            if len(sentence['tokens']) > i and (sentence['tokens'][i]['lemma'] not in  self._blacklist or sentence['tokens'][i]['ner'] not in self._stop_ner):
                                tokens.append(sentence['tokens'][i])
                            else:
                                break
                    else:
                        # no expansion
                        tokens = [token]

                    tokens_fixed = []
                    for token in tokens:
                        tokens_fixed.append(self._token_fix(token))

                    if len(tokens_fixed):
                        candidates.append([tokens_fixed, None, sentence['index'], 'adjectiv'])

        return candidates

    def _token_fix(self, token):
        """
        helper to craete a token based on a legacy structure. (mime leav)
        :param token:
        :return:
        """
        new_token = ({'nlpToken': token}, token['pos'], token)
        return new_token

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
        global_max_lemma = -1
        for candidate in candidates:

            # remove any prev. calculations
            candidate.reset_calculations()

            max_lemma = -1
            for part in candidate.get_parts():
                lemma = part[0]['nlpToken']['lemma']
                # ignore lemma count for stopwords, because they are very frequent
                if lemma not in self._stop_words:
                    # take also just the lemma of the indicator
                    if (candidate.get_type() == 'adjectiv' and self._is_relevant_pos(part[0]['nlpToken']['pos'])) or \
                            candidate.get_type() == 'prepos':
                        lemma_count = lemma_map[lemma]
                        max_lemma = max(max_lemma, lemma_count)
                        global_max_lemma = max(global_max_lemma, lemma_count)

            # assign the greatest lemma to the candidate
            candidate.set_calculations('lemma_count', max_lemma)

        # normalize frequency (per lemma)
        for candidate in candidates:
            count = candidate.get_calculations('lemma_count')
            candidate.set_calculations('lemma_count_norm', count / global_max_lemma)

        # normalize position - reserved order
        #sentences_count = document.get_len()
        #for candidate in candidates:
        #    freq = (sentences_count - candidate.get_sentence_index()) / sentences_count
        #    candidate.set_calculations('position_frequency_norm', freq)

        # calculate score
        score_max = 0
        # weights_sum = sum(self.weights)
        for candidate in candidates:

            type_weight = 1
            if candidate.get_type() == 'adjectiv':
                type_weight = self.weights[2]
            elif candidate.get_type() == 'prepos':
                type_weight = self.weights[3]

            score = ((document.get_len() - candidate.get_sentence_index() + 1) / document.get_len()) * self.weights[0]
            score += (candidate.get_calculations('lemma_count_norm') * self.weights[1])
            score += type_weight

            score /= sum(self.weights)

            candidate.set_score(score)
            if score > score_max:
                score_max = score

        # normalize score
        # for candidate in candidates:
        #    score = candidate.get_score()
        #    candidate.set_score(score / score_max)

        candidates.sort(key=lambda x: x.get_score(), reverse=True)

        # Format fix of parts
        candidates_fixed = self._fix_format(candidates)

        # Filter by text
        candidates_clean = self._filter_candidate_dublicates(candidates_fixed)

        document.set_answer('how', candidates_clean)

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

    def _is_relevant_pos(self, pos):
        # Is adjective or adverb
        if pos.startswith('JJ') or pos.startswith('RB'):
            return True
        else:
            return False
