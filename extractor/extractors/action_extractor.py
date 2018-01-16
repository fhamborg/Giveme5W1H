import re

from nltk.tree import ParentedTree

from extractor.candidate import Candidate
from extractor.extractors.abs_extractor import AbsExtractor


class ActionExtractor(AbsExtractor):
    """
    The ActionExtractor tries to extract the main actor and his action.

    """

    def __init__(self, weights: (float, float, float) = (0.9, 0.095, 0.005), minimal_length_of_tokens: int = 3):
        self._minimal_length_of_tokens = minimal_length_of_tokens

        # weights used in the candidate evaluation:
        # (position, frequency, named entity)
        self.weights = weights

    def _extract_candidates(self, document):
        """
        Extracts possible agents/actions pairs from a given document.
        Candidates are chosen if they belong to an coref-chain and is part of a NP-VP-NP pattern

        :param document: The Document to be analyzed.
        :type document: Document

        :return: A List of Tuples containing all agents, actions and their position in the document.
        """

        # retrieve results from preprocessing
        corefs = document.get_corefs()
        trees = document.get_trees()
        candidates = []

        for cluster in corefs:
            for mention in corefs[cluster]:
                # Check if mention is the subject of the sentence by matching the NP-VP-NP pattern.
                #
                # "One common way of defining the subject of a sentence S in English is as the noun phrase that is the
                # child of S and the sibling of VP" (http://www.nltk.org/book/ch08.html)

                for pattern in self._evaluate_tree(trees[mention['sentNum'] - 1]):
                    np_string = ''.join([p[0]['nlpToken']['originalText'] for p in pattern[0]])
                    if re.sub(r'\s+', '', mention['text']) in np_string:
                        candidate_object = Candidate()
                        candidate_object.set_sentence_index(pattern[2])
                        candidate_object.set_raw([pattern[0], pattern[1], cluster, mention['id']])

                        candidates.append(candidate_object)

        document.set_candidates(self.get_id(), candidates)

    def _evaluate_tree(self, sentence_root):
        """
        Examines the passed syntactic tree to determine if it matches a NP-VP-NP pattern
        This is executed per sentence

        :param sentence_root: A tree to be analyzed
        :type sentence_root: ParentedTree

        :return: A list of Tuples containing the agent and the action described in the sentence.
        """

        candidates = []
        for subtree in sentence_root.subtrees():
            if subtree.label() == 'NP' and subtree.parent().label() == 'S':

                # Skip NPs containing a VP
                if any(list(subtree.subtrees(filter=lambda t: t.label() == 'VP'))):
                    continue

                # check siblings for VP
                sibling = subtree.right_sibling()
                while sibling is not None:
                    if sibling.label() == 'VP':
                        # this gives a tuple to find the way from sentence to leaf
                        # tree_position = subtree.leaf_treeposition(0)
                        entry = [subtree.pos(), self.cut_what(sibling, self._minimal_length_of_tokens).pos(),
                                 sentence_root.stanfordCoreNLPResult['index']]
                        candidates.append(entry)
                        break
                    sibling = sibling.right_sibling()
        return candidates

    def _evaluate_candidates(self, document):
            """
            Calculate a confidence score based on number of mentions, position in text and entailment of named entities
            for extracted candidates.

            :param document: The parsed document
            :type document: Document
            :param candidates: Extracted candidates to evaluate.
            :type candidates:[([(String,String)], ([(String,String)])]
            :return: A list of evaluated and ranked candidates
            """
            ranked_candidates = []
            doc_len = document.get_len()
            doc_ner = document.get_ner()
            doc_coref = document.get_corefs()

            if any(doc_coref.values()):
                # get length of longest coref chain for normalization
                max_len = len(max(doc_coref.values(), key=len))
            else:
                max_len = 1

            for candidate in document.get_candidates(self.get_id()):
                candidateParts = candidate.get_raw()
                verb = candidateParts[1][0][0]['nlpToken']['originalText'].lower()

                # VP beginning with say/said often contain no relevant action and are therefor skipped.
                if verb.startswith('say') or verb.startswith('said'):
                    continue

                coref_chain = doc_coref[candidateParts[2]]

                # first parameter used for ranking is the number of mentions, we use the length of the coref chain
                score = (len(coref_chain) / max_len) * self.weights[1]

                representative = None
                contains_ne = False
                mention_type = ''

                for mention in coref_chain:
                    if mention['id'] == candidateParts[3]:
                        mention_type = mention['type']
                        if mention['sentNum'] < doc_len:
                            # The position (sentence number) is another important parameter for scoring.
                            # This is inspired by the inverted pyramid.
                            score += ((doc_len - mention['sentNum'] + 1) / doc_len) * self.weights[0]
                    if mention['isRepresentativeMention']:
                        # The representative name for this chain has been found.
                        tmp = document._sentences[mention['sentNum'] - 1]['tokens'][mention['headIndex'] - 1]
                        representative = ((tmp['originalText'], tmp), tmp['pos'])


                        try:
                            # these dose`t work, if some special characters are present
                            if representative[-1][1] == 'POS':
                                representative = representative[:-1]
                        except IndexError:
                            pass

                    if not contains_ne:
                        # If the current mention doesn't contain a named entity, check the other members of the chain
                        for token in doc_ner[mention['sentNum'] - 1][mention['headIndex'] - 1:mention['endIndex'] - 1]:
                            if token[1] in ['PERSON', 'ORGANIZATION', 'LOCATION']:
                                contains_ne = True
                                break

                if contains_ne:
                    # the last important parameter is the entailment of a named entity
                    score += self.weights[2]

                if score > 0:
                    # normalize the scoring
                    score /= sum(self.weights)

                if mention_type == 'PRONOMINAL':
                    # use representing mention if the agent is only a pronoun
                    rp_format_fix = [(({'nlpToken': representative[0][1]}, representative[0][1]['pos']))]
                    ranked_candidates.append((rp_format_fix, candidateParts[1], score, candidate.get_sentence_index()))
                else:
                    ranked_candidates.append((candidateParts[0], candidateParts[1], score, candidate.get_sentence_index()))

            # split results
            who = [(c[0], c[2], c[3]) for c in ranked_candidates]
            what = [(c[1], c[2], c[3]) for c in ranked_candidates]

            # Transform who to object oriented list
            o_who = self._filterAndConvertToObjectOrientedList(who)
            # Filter by text
            o_who_clean = self._filter_candidate_dublicates(o_who)
            document.set_answer('who', o_who_clean)

            # Transform who to object oriented list
            o_what = self._filterAndConvertToObjectOrientedList(what)
            # Filter by text
            o_what_clean = self._filter_candidate_dublicates(o_what)
            document.set_answer('what', o_what_clean)

    def _filterAndConvertToObjectOrientedList(self, list):
        max = 0
        candidates = self._filter_duplicates(list)
        for candidate in candidates:
            if candidate.get_score() > max:
                max = candidate.get_score()

        # normalize
        for candidate in candidates:
            score = candidate.get_score()
            candidate.set_score(score / max)

        # sort
        candidates.sort(key=lambda x: x.get_score(), reverse=True)

        return candidates

    def cut_what(self, tree, min_length=0, length=0):
        """
        This function is used to shorten verbphrases, it recursively traverses the parse tree depth first.

        :param tree: Tree to cut
        :type tree: ParentedTree
        :param min_length: Desired minimal length of tokens
        :type min_length: Integer
        :param length: Number of tokens already included by the upper level function
        :type length: Integer

        :return: A subtree
        """
        if type(tree[0]) is not ParentedTree:
            # we found a leaf
            return ParentedTree(tree.label(), [tree[0]])
        else:
            children = []
            for sub in tree:
                child = self.cut_what(sub, min_length, length)
                length += len(child.leaves())
                children.append(child)
                if sub.label() == 'NP':
                    sibling = sub.right_sibling()
                    if length < min_length and sibling is not None and sibling.label() == 'PP':
                        children.append(sibling.copy(deep=True))
                    break
            return ParentedTree(tree.label(), children)
