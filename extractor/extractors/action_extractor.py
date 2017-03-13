import re
from copy import deepcopy
from nltk.tree import ParentedTree
from .abs_extractor import AbsExtractor


class ActionExtractor(AbsExtractor):

    ner_threshold = 0
    # weights used in the candidate evaluation:
    # position, frequency, named entity
    weights = (4, 3, 2)

    def __init__(self, weights=None, ner_threshold=0):
        """
        :param weights: tuple of weights for candidate evaluation: (pos, frequency, ner)
        :param ner_threshold: Overlap threshold used to determine if a phrase contains an entity.
        """
        if weights is not None:
            self.weights = weights

        self.ner_threshold = ner_threshold

    def extract(self, document):
        """
        Parses the document for answers to the questions who and what.

        :param document: Document to be Parsed
        :return: Parsed document
        """

        candidates = self._extract_candidates(document)
        candidates = self._evaluate_candidates(document, candidates)

        who = [(c[0], c[2]) for c in candidates]
        what = [(c[1], c[2]) for c in candidates]

        document.set_answer('who', self._filter_duplicates(who))
        document.set_answer('what', self._filter_duplicates(what))

    def _extract_candidates(self, document, limit=None):
        """
        Extracts all possible agents/actions from a given document.

        :param document: The Document to be analyzed.
        :param limit: Number of sentences that should be analyzed.
        :return: A List of Tuples containing all agents, actions and their position in the document.
        """

        corefs = document.get_corefs()
        trees = document.get_trees()
        candidates = []

        for cluster in corefs:
            for mention in corefs[cluster]:
                # check if the mention is part of a NP-VP-NP pattern
                for pattern in self._evaluate_tree(trees[mention['sentNum']-1]):
                    np_string = ''.join([p[0] for p in pattern[0]])
                    if re.sub(r'\s+', '', mention['text']) in np_string:
                        candidates.append([pattern[0], pattern[1], cluster, mention['id']])

        return candidates


    def _evaluate_tree(self, tree):
        """
        Determines if the given tree contains a possible agent/action.

        :param subtree: A ParentedTree to be analyzed
        :return: A list of Tuples containing the agent and the action described in the sentence.
        """

        candidates = []

        for subtree in tree.subtrees():
                        # A subject of a sentence s can be defined as the NP that is a child of s and the sibling of VP
            if subtree.label() == 'NP' and subtree.parent().label() == 'S':

                # Skip NPs containing a VP
                if any(list(subtree.subtrees(filter=lambda t: t.label() == 'VP'))):
                    continue

                # skip phrases starting with certain pos-patterns
                pos = subtree.pos()

                # for label in pos:
                #     if label[1] in ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']:
                #         break

                # if label is None or label[1] not in ['NN', 'NNS', 'NNP', 'NNPS']:
                #     continue

                # check siblings for VP
                sibling = subtree.right_sibling()
                while sibling is not None:
                    if sibling.label() == 'VP':
                        first = sibling.leaves()[0].lower()
                        # if first.startswith('say') or first.startswith('said'):
                        #     break
                        candidates.append((pos, self.cut_what(sibling, 3).pos()))
                        break
                    sibling = sibling.right_sibling()

        return candidates

    def _cluster_candidates(self, np_list, ner_list):
        """
        Decides based on overlapping tokens or contained entities, if a phrase is considered similar.

        :param np_list: List of noun phrases
        :param ner_list: List of named entities
        :return: Returns clustered noun phrases
        """

        overlap_threshold = 0.6  # overlap necessary for clustering candidates w/o know entities
        clusters = {}
        candidate_strings = []
        candidate_tokens = []

        for np in np_list:
            tokens = [token[0] for token in np[0]]
            candidate_tokens.append(tokens)
            candidate_strings.append(' '.join(tokens).lower())

        for entity in ner_list:
            # each named entity gets a cluster
            clusters[entity[1]] = []

        # check NPs for named entities
        for i in range(len(np_list)):
            entity_found = False

            for entity in ner_list:
                for name in entity[0]:

                    entity_found = name.lower() in candidate_strings[i]
                    if entity_found:
                        np_list[i][3] = True
                        clusters[entity[1]].append(deepcopy(np_list[i]))
                        break

                if entity_found:
                    break

        # revisit NPs without known entities
        for i in range(len(np_list)):
            if not np_list[i][3]:
                clusters[candidate_strings[i]] = [deepcopy(np_list[i])]

                # iterate over following candidates and compare semantic overlap
                for j in range(len(np_list))[i+1:]:
                    if self.sem_overlap(np_list[i][0], np_list[j][0], 'n') > overlap_threshold:
                        clusters[candidate_strings[i]].append(deepcopy(np_list[j]))
                        np_list[j][3] = True  # mark as clustered

        return clusters

    def _evaluate_candidates(self, document, candidates):
        """
        Calculate a confidence score for extracted candidates.

        :param document: The parsed document
        :param clusters: The noun phrase clusters
        :return: A list of evaluated and ranked candidates
        """

        # TODO include VP for ranking?

        ranked_candidates = []
        d_len = document.get_len()
        ners = document.get_ner()
        pos = document.get_pos()
        corefs = document.get_corefs()
        max_len = len(max(corefs.values(), key=len))

        for candidate in candidates:
            verb = candidate[1][0][0].lower()
            if verb.startswith('say') or verb.startswith('said'):
                # skip actions starting with say etc
                continue

            cluster = corefs[candidate[2]]
            score = (len(cluster) / max_len) * self.weights[1]
            rep = None
            ner = False
            type = ''

            for mention in cluster:
                if mention['id'] == candidate[3]:
                    type = mention['type']
                    if mention['sentNum'] < d_len:
                        # position
                        score += ((d_len - mention['sentNum'] + 1) / d_len) * self.weights[0]
                if mention['isRepresentativeMention']:
                    # representing mention for agent without a proper name
                    rep = pos[mention['sentNum']-1][mention['headIndex']-1:mention['endIndex']-1]
                    if rep[-1][1] == 'POS':
                        rep = rep[:-1]

                if not ner:
                    for token in ners[mention['sentNum']-1][mention['headIndex']-1:mention['endIndex']-1]:
                        if token[1] in ['PERSON', 'ORGANIZATION', 'LOCATION']:
                            ner = True
                            score += self.weights[2]
                            break

            if score > 0:
                score /= sum(self.weights)

            if type == 'PRONOMINAL':
                # use representing mention if the agent is only a pronoun
                ranked_candidates.append((rep, candidate[1], score))
            else:
                ranked_candidates.append((candidate[0], candidate[1], score))

        ranked_candidates.sort(key=lambda x: x[2], reverse=True)
        return ranked_candidates

    def cut_what(self, tree, min=0, length=0):
        if type(tree[0]) is not ParentedTree:

            return ParentedTree(tree.label(), [tree[0]])
        else:
            children = []
            for sub in tree:
                child = self.cut_what(sub, min, length)
                length += len(child.leaves())
                children.append(child)
                if sub.label() == 'NP':
                    sibling = sub.right_sibling()
                    if length < min and sibling is not None and sibling.label() == 'PP':
                        children.append(ParentedTree.fromstring(str(sibling)))
                    break
            return ParentedTree(tree.label(), children)




