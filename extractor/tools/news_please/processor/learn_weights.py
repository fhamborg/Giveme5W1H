from .abs_processor import AbsProcessor


class LearnWeights(AbsProcessor):
    def process(self, document):
        #TODO get/set weights, (re)evaluate, (save) result
        print(document.get_title())