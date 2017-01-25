import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from copy import deepcopy
from .abs_extractor import AbsExtractor


class CauseExtractor(AbsExtractor):
    verb_indicators = ['allow', 'affect', 'alter', 'arouse', 'cause', 'change', 'create', 'criticize', 'convert',
                       'cut', 'develop', 'derive', 'encourage', 'extend', 'force', 'let', 'permit', 'make', 'wash',
                       'generate', 'result']
    adverbial_indicators = ['therefore', 'hence', 'thus', 'consequently', 'accordingly']  # TODO 'so' problems with JJ
    clausal_conjunctions = {'consequence': 'of', 'effect': 'of',  'result': 'of', 'upshot': 'of', 'outcome': 'of',
                            'because': '', 'due': 'to', 'stemmed': 'from'}

    def __init__(self, overwrite=None):
        """
        :param overwrite: determines if existing answers should be overwritten.
        """
        try:
            nltk.data.find('wordnet.zip')
        except:
            nltk.download('wordnet')

        if overwrite is not None:
            self.overwrite = overwrite
        self.lemmatizer = WordNetLemmatizer()

    def extract(self, document):
        """
        Parses the document for answers to the question why.

        :param document: Document to be Parsed
        :return: Parsed document
        """
        candidate_list = []

        for i in range(document.length):
            for candidate in self._evaluate_tree(document.posTrees[i]):
                candidate_list.append([candidate[0], candidate[1], i])

        candidate_list = self._evaluate_candidates(document, candidate_list)
        self.answer(document, 'why', candidate_list)

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

    def _evaluate_candidates(self, document, candidates, weights=None):
        """
        Calculate a confidence score for extracted candidates.

        :param document: The parsed document.
        :param candidates: The extracted candidates: [cause, effect, pattern]
        :param weights: Optional weighting used for the evaluation: [position, pattern]
        :return: A list of evaluated and ranked candidates
        """

        if weights is None:
            weights = [1, 1]

        ranked_candidates = []
        for candidate in candidates:
            if candidate is not None and len(candidate[0]) > 0:
                scores = deepcopy(weights)
                # position
                scores[0] *= candidate[2]/document.length
                # pattern
                if candidate[1] == 'biclausal':
                    scores[1] *= 1
                elif candidate[1] == 'RB':
                    scores[1] *= 0.6
                else:
                    scores[1] *= 0.3

                ranked_candidates.append((candidate[0], sum(scores)))

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates
