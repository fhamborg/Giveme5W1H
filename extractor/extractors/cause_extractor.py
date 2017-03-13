import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from copy import deepcopy
from .abs_extractor import AbsExtractor


class CauseExtractor(AbsExtractor):
    weights = (1, 1)
    verb_indicators = ['allow', 'affect', 'alter', 'arouse', 'cause', 'change', 'create', 'criticize', 'convert',
                       'cut', 'develop', 'derive', 'encourage', 'extend', 'force', 'let', 'permit', 'make', 'wash',
                       'generate', 'result']
    adverbial_indicators = ['therefore', 'hence', 'thus', 'consequently', 'accordingly']  # TODO 'so' problems with JJ
    clausal_conjunctions = {'consequence': 'of', 'effect': 'of',  'result': 'of', 'upshot': 'of', 'outcome': 'of',
                            'because': '', 'due': 'to', 'stemmed': 'from'}

    def __init__(self, weights=None, overwrite=True):
        """
        :param weights: tuple of weights for candidate evaluation: (pos, pattern)
        :param overwrite: determines if existing answers should be overwritten.
        """
        try:
            nltk.data.find('wordnet.zip')
        except:
            nltk.download('wordnet')

        if weights is not None:
            self.weights = weights

        self.overwrite = overwrite
        self.lemmatizer = WordNetLemmatizer()

    def extract(self, document):
        """
        Parses the document for answers to the question why.

        :param document: Document to be Parsed
        :return: Parsed document
        """
        candidate_list = []
        posTrees = document.get_trees()

        for i in range(len(posTrees)):
            for candidate in self._evaluate_tree(posTrees[i]):
                if candidate[1] == 'RB':
                    candidate_list.append([candidate[0], candidate[2], i])
                else:
                    candidate_list.append([candidate[1], candidate[2], i])

        candidate_list = self._evaluate_candidates(document, candidate_list)
        document.set_answer('why', candidate_list)

        return document

    def _evaluate_tree(self, tree):
        """
        Determines if the given sub tree contains a cause/effect relation.

        :param tree: A ParentedTree to be analyzed
        :return: A Tuple containing the cause/effect phrases and the pattern used to find it.
        """

        candidates = []
        pos = tree.pos()
        tokens = [tupel[0] for tupel in pos]

        # search for NP-VP-NP patterns representing a cause-effect-relation
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP' and t.right_sibling() is not None):
            sibling = subtree.right_sibling()

            # TODO Modal auxiliaries? (MD)?

            while sibling.label() == 'ADVP' and sibling.right_sibling() is not None:
                sibling = sibling.right_sibling()

            if sibling.label() == 'VP' and '(NP' in sibling.pformat():
                leaves = sibling.leaves()
                verb = leaves[0].lower()

                # TODO passive sentences?

                if verb in self.verb_indicators:
                    candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))
                elif self.lemmatizer.lemmatize(verb, 'v') in self.verb_indicators:
                    candidates.append(deepcopy([subtree.pos(), sibling.pos(), 'NP-VP-NP']))

        for i in range(len(tokens)):
            token = tokens[i].lower()

            # TODO negation check?

            # search for adverbs indicating a causal relation
            if pos[i][1] == 'RB' and token in self.adverbial_indicators:
                candidates.append(deepcopy([pos[i - 1:], pos[:i], 'RB']))
            # search for causal links
            elif token in self.clausal_conjunctions and \
                    ' '.join(tokens[i:]).lower().startswith(self.clausal_conjunctions[token]):
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
                # position
                score = self.weights[0] * (document.get_len()-candidate[2]) / document.get_len()
                # pattern
                if candidate[1] == 'biclausal':
                    score += self.weights[1]
                elif candidate[1] == 'RB':
                    score += self.weights[1] * 0.5

                if score > 0:
                    score /= weights_sum

                ranked_candidates.append((candidate[0], score))

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates
