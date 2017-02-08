from copy import deepcopy

from .abs_extractor import AbsExtractor


class ActionExtractor(AbsExtractor):

    ner_threshold = 0
    weights = (1, 1, 1)

    def __init__(self, weights=None, overwrite=True, ner_threshold=0):
        """
        :param weights: tuple of weights for candidate evaluation: (pos, frequency, ner)
        :param overwrite: determines if existing answers should be overwritten.
        :param ner_threshold: Overlap threshold used to determine if a phrase contains an entity.
        """
        if weights is not None:
            self.weights = weights

        self.overwrite = overwrite
        self.ner_threshold = ner_threshold

    def extract(self, document):
        """
        Parses the document for answers to the questions who and what.

        :param document: Document to be Parsed
        :return: Parsed document
        """

        candidates = self._extract_candidates(document)
        candidates = self._cluster_candidates(candidates[0], candidates[1])
        candidates = self._evaluate_candidates(document, candidates)

        who = [(c[1], c[0]) for c in candidates]
        what = [(c[2], c[0]) for c in candidates]

        self.answer(document, 'who', who)
        self.answer(document, 'what', what)

    def _extract_candidates(self, document, limit=None):
        """
        Extracts all possible agents/actions from a given document.

        :param document: The Document to be analyzed.
        :param limit: Number of sentences that should be analyzed.
        :return: A List of Tuples containing all agents, actions and their position in the document.
        """

        entity_list = []
        np_list = []

        # look up all named entities
        for i in range(len(document.nerTags)):
            for candidate in self._extract_entities(document.nerTags[i], filter=['PERSON', 'ORGANIZATION'],
                                                    inverted=True):

                # check if a similar name was already mentioned
                similarity = 0
                for entity in entity_list:
                    for name in entity[0]:
                        similarity = max(similarity, self.overlap(candidate[0], name))

                    if 1 > similarity > self.ner_threshold:
                        entity[0].append(candidate[0])
                        break

                # no similar name could be found, this must be a new entity
                if similarity == 0:
                    entity_list.append([[candidate[0]], None, candidate[1]])

        # sort names of entities by ascending length and select longest as most accurate representation
        for entity in entity_list:

            name_strings = []

            for name in entity[0]:
                if isinstance(name, list):
                    name = ' '.join(name)
                name_strings.append(name)

            name_strings.sort(key=len)
            entity[0] = name_strings
            entity[1] = name_strings[len(name_strings)-1]

        # extract all suitable NPs
        for i in range(document.length):
            if limit is not None and limit == i:
                break
            np_list.extend([c[0], c[1], i, False] for c in self._evaluate_tree(document.posTrees[i]))

        return np_list, entity_list

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

                # skip phrases starting with certain pos-patterns
                pos = subtree.pos()

                for label in pos:
                    if label[1] in ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']:
                        break

                if label is None or label[1] not in ['NN', 'NNS', 'NNP', 'NNPS']:
                    continue

                # check siblings for VP
                sibling = subtree.right_sibling()
                while sibling is not None:
                    if sibling.label() == 'VP':
                        candidates.append((pos, sibling.pos()))
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

        overlap_threshold = 0.5  # overlap necessary for clustering candidates w/o know entities
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

                # iterate over following candidates
                for j in range(len(np_list))[i+1:]:
                    if self.overlap(candidate_tokens[i], candidate_tokens[j]) > overlap_threshold:
                        clusters[candidate_strings[i]].append(deepcopy(np_list[j]))
                        np_list[j][3] = True  # mark as clustered

        return clusters

    def _evaluate_candidates(self, document, clusters):
        """
        Calculate a confidence score for extracted candidates.

        :param document: The parsed document
        :param clusters: The noun phrase clusters
        :return: A list of evaluated and ranked candidates
        """

        # TODO include VP for ranking?

        ranked_candidates = []

        for cluster in clusters:
            frequency = len(clusters[cluster])
            for candidate in clusters[cluster]:

                scores = list(self.weights)
                # position
                scores[0] *= (document.length - candidate[2])
                # frequency
                scores[1] *= frequency
                # contains a named entity
                if candidate[3]:
                    scores[2] *= 1
                else:
                    scores[2] = 0
                ranked_candidates.append((sum(scores), candidate[0], candidate[1]))

        ranked_candidates.sort(key=lambda x: x[0], reverse=True)
        return ranked_candidates





