from .abs_processor import AbsProcessor


class LearnWeights(AbsProcessor):
    def __init__(self, outputPath):
        self._outputPath = outputPath
        
        
    def process(self, document):
        #TODO get/set weights, (re)evaluate, (save) result
        print(document.get_title())
    
    
    def _writeToJson(self):
        print('writeResultPerRun')
        # TODO: not sure how this should looks like
        
        # generate result files
        
#         files = {
#             'action': open(os.path.expanduser('~') + '/confusion/who-matrix_' + prefix + '.csv', 'w+'),
#             'when': open(os.path.expanduser('~') + '/confusion/when-matrix_' + prefix + '.csv', 'w+'),
#             'why': open(os.path.expanduser('~') + '/confusion/why-matrix_' + prefix + '.csv', 'w+')
#         }
# 
#         # write caption
#         files['action'].write('position,frequency,named entity,score who,score what\n')
#         files['when'].write('position,date,frequency,score\n')
#         files['why'].write('position,conjunction,adverb,verb,score\n')