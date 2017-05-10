import logging
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from copy import deepcopy
from .abs_extractor import AbsExtractor


class CauseExtractor(AbsExtractor):
    """
    The CauseExtractor tries to detect a causative that could explain an event.
    """

    # weights used in the candidate evaluation:
    # (position, clausal conjunction, adverbial indicator, NP-VP-NP)
    weights = (.35, 0.3, .7, .4)

    adverbial_indicators = ['therefore', 'hence', 'thus', 'consequently', 'accordingly']  # 'so' has problems with JJ
    clausal_conjunctions = {'consequence': 'of', 'effect': 'of',  'result': 'of', 'upshot': 'of', 'outcome': 'of',
                            'because': '', 'due': 'to', 'stemmed': 'from'}

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

    def __init__(self, weights=None):
        """
        Load WordNet corpus

        :param weights: tuple of weights for candidate evaluation
        :type weights: (Float, Float)
        """
        self.log = logging.getLogger('GiveMe5W')

        # fetch WordNet corpus
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            self.log.info('Could not find corpus for WordNet, will now try to download the corpus.')
            nltk.download('wordnet')

        if weights is not None:
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

    def extract(self, document):
        """
        Parses the document for answers to the question why.

        :param document: Document to be Parsed
        :return: Parsed document
        """

        candidate_list = self._extract_candidates(document)
        candidate_list = self._evaluate_candidates(document, candidate_list)
        document.set_answer('why', candidate_list)

        return document

    def _extract_candidates(self, document):
        """
        Extracts possible agents/actions pairs from a given document.
        Candidates are chosen if they belong to an coref-chain and is part of a NP-VP-NP pattern

        :param document: The Document to be analyzed.
        :type document: Document

        :return: A List of Tuples containing all agents, actions and their position in the document.
        """
        candidate_list = []
        postrees = document.get_trees()

        for i, tree in enumerate(postrees):
            for candidate in self._evaluate_tree(tree):
                candidate_list.append([candidate[1], candidate[2], i])

        return candidate_list

    def _evaluate_tree(self, tree):
        """
        Determines if the given sub tree contains a cause/effect relation.

        The indicators used in this function are inspired by TODO

        :param tree: A tree to analyze
        :type tree: ParentedTree

        :return: A Tuple containing the cause/effect phrases and the pattern used to find it.
        """

        candidates = []
        pos = tree.pos()
        tokens = [t[0] for t in pos]

        # Searching for cause-effect relations that involve a verb/action we look for NP-VP-NP
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP' and t.right_sibling() is not None):
            sibling = subtree.right_sibling()

            # skip to the first verb
            # TODO skip Modal auxiliaries? (MD)?
            while sibling.label() == 'ADVP' and sibling.right_sibling() is not None:
                sibling = sibling.right_sibling()

            # NP-VP-NP pattern found
            if sibling.label() == 'VP' and '(NP' in sibling.pformat():
                verbs = [t[0] for t in sibling.pos() if t[1][0] == 'V'][:3]
                verb_synset = set()

                # depending on the used tense, we may have to look at the second/third verb e.g. 'have been ...'
                for verb in verbs:
                    normalized = verb.lower()

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
                            if verb == token[0]:
                                rest = ' '.join([t[0] for t in verbs[i+1:i+3]]).lower()
                                break
                        if rest != self.causal_verb_phrases[lemma]:
                            continue

                # pattern contains a valid verb, so check the 8 subpatterns
                if not verb_synset.isdisjoint(self.constraints_verbs['cause']):
                    candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                else:
                    pre = [t[0].lower() for t in subtree.pos() if t[1][0] == 'N' and t[0].isalpha()]
                    post = [t[0].lower() for t in sibling.pos() if t[1][0] == 'N' and t[0].isalpha()]
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
                    if post_con['phenomenon']:
                        candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                    elif not pre_con['entity'] and (verb_con['associate'] or verb_con['relate']) and (
                                    post_con['abstraction'] and post_con['group'] and post_con['possession']):
                        candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                    elif not pre_con['entity'] and post_con['event']:
                        candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                    elif not pre_con['abstraction'] and (post_con['event'] or post_con['act']):
                        candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                    elif verb_con['lead'] and (not post_con['entity'] and not post_con['group']):
                        candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))

        # search for adverbs or clausal conjunctions
        for i in range(len(tokens)):
            token = tokens[i].lower()

            # TODO negation check?
            if pos[i][1] == 'RB' and token in self.adverbial_indicators:
                # If we come along an adverb (RB) check the adverbials that indicate causation
                candidates.append(deepcopy([pos[:i], pos[i - 1:], 'RB']))

            elif token in self.clausal_conjunctions and \
                    ' '.join(tokens[i:]).lower().startswith(self.clausal_conjunctions[token]):
                # Check if token is au clausal conjunction indicating causation
                candidates.append(deepcopy([pos[i - 1:], pos[:i], 'biclausal']))
        return candidates

    def _evaluate_candidates(self, document, candidates):
        """
        Calculate a confidence score for extracted candidates.

        :param document: The parsed document.
        :param candidates: The extracted candidates: [cause, effect, pattern]
        :param weights: Optional weighting used for the evaluation: [position, pattern]

        :return: A list of evaluated and ranked candidates
        """

        ranked_candidates = []
        weights_sum = sum(self.weights)

        for candidate in candidates:
            if candidate is not None and len(candidate[0]) > 0:
                # following the concept of the inverted pyramid use the position for scoring
                score = self.weights[0] * (document.get_len()-candidate[2]) / document.get_len()

                # we also consider the pattern typ used to detect the candidate
                if candidate[1] == 'biclausal':
                    # the most obvious candidates have biclausal indicators and get the most boost
                    score += self.weights[1]
                elif candidate[1] == 'RB':
                    # while not as significant as biclausal indicators, adverbials are mor significant as the verbs
                    score += self.weights[2]
                else:
                    # NP-VP-NP
                    score += self.weights[3]

                if score > 0:
                    score /= weights_sum

                ranked_candidates.append((candidate[0], score))

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates

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
