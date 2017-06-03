from .abs_processor import AbsProcessor


class SimpleLogger(AbsProcessor):
    def process(self, document):
        #TODO get/set weights, (re)evaluate, (save) result
        print('Processed: ',document.get_title())