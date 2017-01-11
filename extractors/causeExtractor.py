from extractors.absExtractor import AbsExtractor
import nltk
from nltk.stem.wordnet import WordNetLemmatizer


class CauseExtractor(AbsExtractor):
    verb_indicators = ['allow', 'affect', 'alter', 'arouse', 'cause', 'change', 'create', 'criticize', 'convert',
                       'cut', 'develop', 'derive', 'encourage', 'extend', 'force', 'let', 'permit', 'make', 'wash',
                       'generate', 'result']
    adverbial_indicators = ['therefore', 'hence', 'thus', 'consequently', 'accordingly']  # TODO 'so' problems with JJ
    clausal_conjunctions = {'consequence': 'of', 'effect': 'of',  'result': 'of', 'upshot': 'of', 'outcome': 'of',
                            'because': '', 'due': 'to', 'stemmed': 'from'}

    def __init__(self, overwrite=None):

        try:
            nltk.data.find('wordnet.zip')
        except:
            nltk.download('wordnet')

        if overwrite is not None:
            self.overwrite = overwrite
        self.lemmatizer = WordNetLemmatizer()

    def extract(self, document):
        candidates = []

        for i in range(document.length):
            candidates.extend([c.append(i) for c in self._evaluate_tree(document.posTrees[i])])

        candidates = self._evaluate_candidates(document, candidates)
        self.answer(document, 'why', candidates)

    def _evaluate_tree(self, tree):
        """
        Determines if the given sub tree contains a possible reason.

        :param tree: A ParentedTree to be analyzed
        :return: A Tuple containing the cause/effect phrases and the methode used to find it.
        """

        candidates = []
        pos = tree.pos()
        tokens = [tupel[0] for tupel in pos]

        # search for NP-VP-NP patterns representing a cause-effect-relation
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP' and t.right_sibling() is not None):
            sibling = subtree.right_sibling()

            # TODO Modal auxiliaries? (MD)

            while sibling.label() == 'ADVP' and sibling.right_sibling() is not None:
                sibling = sibling.right_sibling()

            if sibling.label() == 'VP' and '(NP' in sibling.pformat():
                leaves = sibling.leaves()
                verb = leaves[0].lower()

                # TODO passive sentences

                if verb in self.verb_indicators:
                    candidates.append([subtree.pos(), sibling.pos(), 'NP-VP-NP'])
                elif self.lemmatizer.lemmatize(verb, 'v') in self.verb_indicators:
                    candidates.append([subtree.pos(), sibling.pos(), 'NP-VP-NP'])

        for i in range(len(tokens)):
            token = tokens[i].lower()

            # TODO negation check

            # search for adverbs indicating a causal relation
            if pos[i][1] == 'RB' and token in self.adverbial_indicators:
                candidates.append([pos[i - 1:], pos[:i], 'RB'])
            # search for causal links
            elif token in self.clausal_conjunctions and \
                            ' '.join(tokens[i:]).lower() == self.clausal_conjunctions[token]:
                candidates.append([pos[i - 1:], pos[:i], 'biclausal'])

        return candidates

    def _evaluate_candidates(self, document, candidates, weights=None):

        if weights is None:
            weights = [1, 1]

        ranked_candidates = []
        for candidate in candidates:
            if candidate is not None and len(candidate[0]) > 0:
                scores = weights
                scores[0] *= candidate[3]/document.length
                if candidate[2] == 'biclausal':
                     scores[1] *= 1
                elif candidate[2] == 'RB':
                    scores[1] *= 0.6
                else:
                    scores[1] *= 0.3

                ranked_candidates.append((candidate[0], sum(scores)))

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates
