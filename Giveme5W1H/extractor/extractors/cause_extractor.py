import logging
from copy import deepcopy

import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

from Giveme5W1H.extractor.candidate import Candidate
from Giveme5W1H.extractor.extractors.abs_extractor import AbsExtractor


class CauseExtractor(AbsExtractor):
    """
    The CauseExtractor tries to detect a causative that could explain an event.
    """

    adverbial_indicators = ['therefore', 'hence', 'thus', 'consequently', 'accordingly']  # 'so' has problems with JJ
    causal_conjunctions = {'consequence': 'of', 'effect': 'of', 'result': 'of', 'upshot': 'of', 'outcome': 'of',
                           'because': '', 'due': 'to', 'stemmed': 'from'}

    causal_conjunctions_inclusive = ['because', 'hence', 'thus', 'stemmed', 'due']

    # list of verbs for the detection of cause-effect relations within NP-VP-NP patterns
    # this list and the TODO
    causal_verbs = ['activate', 'actuate', 'arouse', 'associate', 'begin', 'bring', 'call', 'cause', 'commence',
                    'conduce', 'contribute', 'create', 'derive', 'develop', 'educe', 'effect', 'effectuate', 'elicit',
                    'entail', 'evoke', 'fire', 'generate', 'give', 'implicate', 'induce', 'kick', 'kindle', 'launch',
                    'lead', 'link', 'make', 'originate', 'produce', 'provoke', 'put', 'relate', 'result', 'rise', 'set',
                    'spark', 'start', 'stem', 'stimulate', 'stir', 'trigger', 'unleash']

    # list of verbs that require additional tokens
    causal_verb_phrases = {'call': ['down', 'forth'], 'fire': ['up'], 'give': ['birth'], 'kick': ['up'],
                           'put': ['forward'], 'set': ['in motion', 'off', 'up'], 'stir': ['up']}

    # verbs involved in NP-VP-NP constraints
    constraints_verbs = {'cause': None, 'associate': None, 'relate': None, 'lead': None, 'induce': None}

    # hyponym classes involved in NP-VP-NP constraints
    constraints_hyponyms = {'entity': None, 'phenomenon': None, 'abstraction': None, 'group': None, 'possession': None,
                            'event': None, 'act': None, 'state': None}

    def __init__(self, weights: (float, float, float, float) = (.56, .44, .27, .026)):
        """
        Load WordNet corpus.

        :param weights: (position, clausal conjunction, adverbial indicator, NP-VP-NP)
        :type weights: (Float, Float, Float, Float)
        """
        self.log = logging.getLogger('GiveMe5W')

        # fetch WordNet corpus
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            self.log.warning('Could not find corpus for WordNet, will now try to download the corpus.')
            nltk.download('wordnet')

        self.weights = weights

        # translate causal verbs into synsets
        synsets = []
        for verb in self.causal_verbs:
            synsets += wordnet.synsets(verb, 'v')
        self.causal_verbs = set(synsets)

        for verb in self.constraints_verbs:
            self.constraints_verbs[verb] = set(wordnet.synsets(verb, 'v'))

        # initialize synsets that are used as constraints in NP-VP-VP patterns
        for noun in self.constraints_hyponyms:
            hyponyms = set()
            for synset in wordnet.synsets(noun, 'n'):
                hyponyms |= self.get_hyponyms(synset)
            self.constraints_hyponyms[noun] = hyponyms

        self.lemmatizer = WordNetLemmatizer()

    def _extract_candidates(self, document):
        """
        Extracts possible agents/actions pairs from a given document.
        Candidates are chosen if they belong to an coref-chain and is part of a NP-VP-NP pattern

        :param document: The Document to be analyzed.
        :type document: Document

        :return: A List of Tuples containing all agents, actions and their position in the document.
        """
        candidates = []
        postrees = document.get_trees()

        for i, tree in enumerate(postrees):
            for candidate in self._evaluate_tree(tree):
                candidateObject = Candidate()
                # used by the extractor
                candidateObject.set_raw(candidate[0])  # candidate[0] contains the cause, candidate[1] the effect
                candidateObject.set_type(candidate[2])
                candidateObject.set_sentence_index(i)

                candidates.append(candidateObject)

        document.set_candidates(self.get_id(), candidates)

    def _evaluate_tree(self, tree):
        """
        Determines if the given sub tree contains a cause/effect relation.

        The indicators used in this function are inspired by:
        "Automatic Extraction of Cause-Effect Information from Newspaper Text Without Knowledge-based Inferencing"
        by Khoo et. al. (adverbs + conjunctions)
        "Automatic Detection of Causal Relations for Question Answering" by Roxana Girj (verbs)

        :param tree: A tree to analyze
        :type tree: ParentedTree

        :return: A Tuple containing the cause/effect phrases and the pattern used to find it.
        """
        self._candidatesObjects = []
        candidates = []
        pos = tree.pos()
        tokens = [t[0] for t in pos]

        # Searching for cause-effect relations that involve a verb/action we look for NP-VP-NP
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP' and t.right_sibling() is not None):
            sibling = subtree.right_sibling()

            # skip to the first verb
            while sibling.label() == 'ADVP' and sibling.right_sibling() is not None:
                sibling = sibling.right_sibling()

            # NP-VP-NP pattern found .unicode_repr()
            if sibling.label() == 'VP' and "('NP'" in sibling.unicode_repr():
                verbs = [t[0] for t in sibling.pos() if t[1][0] == 'V'][:3]
                verb_synset = set()

                # depending on the used tense, we may have to look at the second/third verb e.g. 'have been ...'
                for verb in verbs:
                    normalized = verb['nlpToken']['originalText'].lower()

                    # check if word meaning is relevant
                    verb_synset = set(wordnet.synsets(normalized, 'v'))
                    if verb_synset.isdisjoint(self.causal_verbs):
                        continue

                    # if necessary look at the  following phrase
                    lemma = self.lemmatizer.lemmatize(normalized)
                    if lemma in self.causal_verb_phrases:
                        # fetch following two tokens
                        rest = ''
                        for i, token in enumerate(verbs):
                            if verb['nlpToken']['word'] == token['nlpToken']['word']:
                                rest = ' '.join([t['nlpToken']['word'] for t in verbs[i + 1:i + 3]]).lower()
                                break
                        if rest != self.causal_verb_phrases[lemma]:
                            continue

                # According to Girju, if the found verb is 'cause' or a synonym, the following NP is 100% the cause
                # so we can directly put it in the list of candidates
                if not verb_synset.isdisjoint(self.constraints_verbs['cause']):
                    candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                else:
                    # pattern contains a valid verb (that is not 'cause'), so check the 7 subpatterns
                    pre = [t[0]['nlpToken']['originalText'].lower() for t in subtree.pos() if
                           t[1][0] == 'N' and t[0]['nlpToken']['originalText'].isalpha()]
                    post = [t[0]['nlpToken']['originalText'].lower() for t in sibling.pos() if
                            t[1][0] == 'N' and t[0]['nlpToken']['originalText'].isalpha()]
                    pre_con = {'entity': False, 'abstraction': False}
                    post_con = {'entity': False, 'phenomenon': False, 'abstraction': False, 'group': False,
                                'possession': False, 'event': False, 'act': False, 'state': False}
                    verb_con = {'associate': False, 'relate': False, 'lead': False, 'induce': False}

                    # check nouns in after verb
                    for noun in post:
                        noun_synset = set(wordnet.synsets(noun, 'n'))
                        for con in post_con:
                            post_con[con] = post_con[con] or not noun_synset.isdisjoint(self.constraints_hyponyms[con])
                            if post_con['phenomenon']:
                                break

                        if post_con['phenomenon']:
                            break

                    # check nouns in before verb
                    for noun in pre:
                        noun_synset = set(wordnet.synsets(noun, 'n'))
                        for con in pre_con:
                            pre_con[con] = pre_con[con] or not noun_synset.isdisjoint(self.constraints_hyponyms[con])

                    # check if verb is relevant for a subpattern
                    for con in verb_con:
                        verb_con[con] = not verb_synset.isdisjoint(self.constraints_verbs[con])
                        if verb_con[con]:
                            break

                    # apply subpatterns
                    if (
                            post_con['phenomenon']
                    ) or (
                            not pre_con['entity'] and (verb_con['associate'] or verb_con['relate']) and (
                            post_con['abstraction'] and post_con['group'] and post_con['possession'])
                    ) or (
                            not pre_con['entity'] and post_con['event']
                    ) or (
                            not pre_con['abstraction'] and (post_con['event'] or post_con['act'])
                    ) or (
                            verb_con['lead'] and (not post_con['entity'] and not post_con['group'])
                    ):
                        candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))

        # search for adverbs or clausal conjunctions
        for i in range(len(tokens)):
            token = tokens[i]['nlpToken']['originalText'].lower()

            if pos[i][1] == 'RB' and token in self.adverbial_indicators:
                # If we come along an adverb (RB) check the adverbials that indicate causation
                candidates.append(deepcopy([pos[:i], pos[i - 1:], 'RB']))

            elif token in self.causal_conjunctions and ' '.join([x['nlpToken']['originalText'] for x in tokens[i:]]).lower().startswith(
                self.causal_conjunctions[token]):
                # Check if token is a clausal conjunction indicating causation
                start = i
                if token not in self.causal_conjunctions_inclusive:
                    # exclude clausal conjunction besides special cases
                    start += 1
                candidates.append(deepcopy([pos[start:], pos[:i], 'biclausal']))

        # drop candidates containing other candidates
        unique_candidates = []
        candidate_strings = []
        for candidate in candidates:
            # Bugfix, at some very rare occasions, the candidate holds an empty list
            if len(candidate[0]) > 0:
                another_string = [x[0]['nlpToken']['originalText'] for x in candidate[1]]
                a_string = candidate[0][0][0]['nlpToken']['originalText'] + ' ' + ' '.join(another_string)
                candidate_strings.append(a_string)

        for i, candidate in enumerate(candidates):
            unique = True
            for j, substring in enumerate(candidate_strings):
                if i != j and candidate[2] == candidates[j][2] and substring in candidate_strings[i]:
                    unique = False
                    break
            if unique:
                unique_candidates.append(candidate)

        return unique_candidates

    def _evaluate_candidates(self, document):
        """
        Calculate a confidence score for extracted candidates.

        :param document: The parsed document.
        :param candidates: The extracted candidates: [cause, effect, pattern]
        :param weights: Optional weighting used for the evaluation: [position, pattern]

        :return: A list of evaluated and ranked candidates
        """
        # ranked_candidates = []
        candidates = document.get_candidates(self.get_id())

        # normalization sum is only first and second weight, because the second to fourth weights
        # are only virtual weights but actually scores
        weights_norm_sum = self.weights[0] + self.weights[1]

        for candidateObject in candidates:

            parts = candidateObject.get_raw();
            if parts is not None and len(parts) > 0:
                # following the concept of the inverted pyramid use the position for scoring
                score = self.weights[0] * (
                        document.get_len() - candidateObject.get_sentence_index()) / document.get_len()

                # we also consider the pattern typ used to detect the candidate
                if candidateObject.get_type() == 'biclausal':
                    # the most obvious candidates have biclausal indicators and get the most boost
                    score += self.weights[1]
                elif candidateObject.get_type() == 'RB':
                    # while not as significant as biclausal indicators, adverbials are mor significant as the verbs
                    score += self.weights[2]
                else: # NP-VP-NP
                    score += self.weights[3]

                if score > 0:
                    score /= weights_norm_sum

                # NEW
                candidateObject.set_score(score)

        # TODO: remove leftover from refactoring
        for candidate in candidates:
            candidate.set_parts(candidate.get_raw())

        candidates.sort(key=lambda x: x.get_score(), reverse=True)

        candidates_clean = self._filter_candidate_dublicates(candidates)
        document.set_answer('why', candidates_clean)

    def get_hyponyms(self, synsets):
        """
        Fetches all hyponyms in a recursive manner creating a word class.

        :param synsets: The list of synsets to process
        :type synsets: [synset]

        :return: A set of synsets
        """

        result = set()
        for hyponym in synsets.hyponyms():
            result |= self.get_hyponyms(hyponym)
        return result | set(synsets.hyponyms())
