import logging
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from copy import deepcopy
from .abs_extractor import AbsExtractor


class CauseExtractor(AbsExtractor):
    """
    The CauseExtractor tries to detect a causative that could explain an event.
    """

    # weights used in the candidate evaluation:
    # (position, pattern type)
    weights = (1, 1)

    # list of indicators indicating a cause-effect relation
    # this list is inspired by TODO
    verb_indicators = ['allow', 'affect', 'alter', 'arouse', 'cause', 'change', 'create', 'criticize', 'convert',
                       'cut', 'develop', 'derive', 'encourage', 'extend', 'force', 'let', 'permit', 'make', 'wash',
                       'generate', 'result']
    adverbial_indicators = ['therefore', 'hence', 'thus', 'consequently', 'accordingly']  # 'so' has problems with JJ
    clausal_conjunctions = {'consequence': 'of', 'effect': 'of',  'result': 'of', 'upshot': 'of', 'outcome': 'of',
                            'because': '', 'due': 'to', 'stemmed': 'from'}

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

            # TODO Modal auxiliaries? (MD)?

            # skip to the first verb
            while sibling.label() == 'ADVP' and sibling.right_sibling() is not None:
                sibling = sibling.right_sibling()

            if sibling.label() == 'VP' and '(NP' in sibling.pformat():
                leaves = sibling.leaves()
                verb = leaves[0].lower()

                # TODO passive sentences?

                if verb in self.verb_indicators:
                    candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                elif self.lemmatizer.lemmatize(verb, 'v') in self.verb_indicators:
                    # if the first attempt failed, try to lemmatize the verb using WordNet
                    candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))

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
                    score += self.weights[1] * 0.5

                if score > 0:
                    score /= weights_sum

                ranked_candidates.append((candidate[0], score))

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates
