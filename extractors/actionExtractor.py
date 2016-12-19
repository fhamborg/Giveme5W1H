from .absExtractor import AbsExtractor


class ActionExtractor(AbsExtractor):

    def extract(self, document):
        candidates = self._extract_candidates(document)
        candidates = self._cluster_candidates(candidates[0], candidates[1])
        candidates = self._evaluate_candidates(document, candidates)
        self.answer(document, 'who', candidates)

    def _extract_candidates(self, document, limit=None):
        """
        Extracts all possible agents/actions from a given document.

        :param document: The Document to be analyzed.
        :param limit: Number of sentences that should be analyzed.
        :return: A List of Tuples containing all agents, actions and their position in the document.
        """

        entity_list = []
        # look up all named entities
        for i in range(len(document.nerTags)):
            for candidate in self._extract_entities(document.nerTags[i],
                                                    filter=['PERSON', 'ORGANIZATION'],
                                                    inverted=True):
                # check if a similar name was already mentioned
                max_overlap = 0
                for entity in entity_list:
                    for name in entity[0]:
                        max_overlap = max(max_overlap, self.overlap(candidate[0], name))

                    if 1 > max_overlap > 0:
                        entity[0].append(candidate[0])
                        break

                # no similar name could be found, this must be a new entity
                if max_overlap == 0:
                    entity_list.append([[candidate[0]], None, candidate[1]])

        # sort names of entities by ascending length and pic longest as most accurate representation
        for entity in entity_list:
            entity[0].sort(key=len)
            entity[1] = ' '.join(entity[0][len(entity[0])-1])

        np_list = []
        # extract all suitable NPs
        for i in range(len(document.posTrees)):
            if limit is not None and limit == i:
                break

            for subtree in document.posTrees[i].subtrees():
                candidate = self._evaluate_subtree(subtree)
                if candidate is not None:
                    np_list.append([candidate[0], candidate[1], i, False])

        return np_list, entity_list

    def _evaluate_subtree(self, subtree):
        """
        Determines if the given sub tree contains a possible agent/action.

        :param subtree: A ParentedTree to be analyzed
        :return: A Tuple containing the agent and the action described in the sentence.
        """

        # A subject of a sentence s can be defined as the NP that is a child of s and the sibling of VP
        if subtree.label() == 'NP' and subtree.parent().label() == 'S':
            # check siblings
            sibling = subtree.right_sibling()
            while sibling is not None:
                if sibling.label() == 'VP':
                    return subtree, sibling
                sibling = sibling.right_sibling()

        return None

    def _cluster_candidates(self, np_list, ner_list):

        clusters = {}
        for entity in ner_list:
            clusters[entity[1]] = []

        for candidate in np_list:
            candidate_phrase = ' '.join(candidate[0].leaves()).lower()

            # check NPs for named entities
            for entity in ner_list:
                for name in entity[0]:
                    if ' '.join(name).lower() in candidate_phrase:
                        clusters[entity[1]].append((candidate[0], candidate[1], candidate[2], True))
                        candidate[3] = True
                        break

            if not candidate[3]:
                if 'PRP' in [token[1] for token in candidate[0].pos()]:
                    # drop pronouns
                    np_list.remove(candidate)

        np_list = [np for np in np_list if not np[3]]
        for candidate in np_list:
            candidate_tokens = candidate[0].leaves()
            candidate_phrase = ' '.join(candidate_tokens)

            for noun_phrase in np_list:
                if not noun_phrase[3] and self.overlap(candidate_tokens, noun_phrase[0].leaves()) > 0.5:
                    if candidate_phrase not in clusters.keys():
                        clusters[candidate_phrase] = []
                    clusters[candidate_phrase].append((noun_phrase[0], noun_phrase[1], noun_phrase[2], False))
                    noun_phrase[3] = True

        return clusters

    def _evaluate_candidates(self, document, clusters, weights=None):

        sentences = len(document.sentences)
        ranked_candidates = []

        if weights is None:
            scores = [1, 1, 1]
        else:
            scores = weights

        for cluster in clusters:
            for phrase in clusters[cluster]:
                # frequency
                scores[0] *= len(phrase[0])/sentences
                # position
                scores[1] *= (sentences - phrase[3])/sentences
                # contains a named entity
                if phrase[3]:
                    scores[2] *= 1
                else:
                    scores[2] = 0
                ranked_candidates.append((sum(scores), phrase[0], phrase[1]))

        ranked_candidates.sort(key=lambda x: x[0], reverse=True)
        return ranked_candidates





