import csv


class CSVWriter:
    def __init__(self, path):
        self.csv_file = open(path, 'w')
        self.writer = csv.writer(self.csv_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer = None
        self.csv_file.close()

    def save_document(self, document, n=3):
        # writes results and annotation to a csv file

        self.writer.writerow([document.raw_title])

        questions = {'what': [], 'who': [], 'why': [], 'where': [], 'when': []}

        # read gate annotations
        for annotation in [a for a in document.annotations if a[0] == 'FiveW']:
            features = {'question': '-', 'id': '1', 'accuracy': '1'}

            for feature in annotation[1]:
                features[feature[0]] = feature[1]

            if features['question'] in questions.keys():
                questions[features['question']].append((features['id'], features['accuracy'], annotation[2]))

        # write to csv file
        for question in questions.keys():
            topn_annotations = sorted(questions[question], key=lambda q: q[1])[:n]
            topn_results = document.questions[question][:n]

            self.writer.writerow([question, 'annotation', '(id | accuracy)', 'result', 'score'])
            if max(len(topn_annotations), len(topn_results)) == 0:
                self.writer.writerow([])

            for i in range(n):
                row = ['', '', '', '', '']
                data = False

                if len(topn_annotations) > i:
                    row[1] = topn_annotations[i][2]
                    row[2] = ('(%s| %s)' % (topn_annotations[i][0], topn_annotations[i][1]))
                    data = True

                if len(topn_results) > i:
                    if question in ['where', 'why']:
                        answer = ' '.join(topn_results[i][0])
                    else:
                        answer = ' '.join([token[0] for token in topn_results[i][0]])  # filter pos
                    row[3] = answer
                    row[4] = topn_results[i][1]
                    data = True

                if data:
                    self.writer.writerow(row)

        self.writer.writerow([])
        self.writer.writerow([])
