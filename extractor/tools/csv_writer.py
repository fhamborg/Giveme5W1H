import csv


class CSVWriter:
    def __init__(self, path):
        """
        A simple csv writer

        :param path: Path to the file
        """
        self.csv_file = open(path, 'w')
        self.writer = csv.writer(self.csv_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer = None
        self.csv_file.close()

    def save_document(self, document, n=3):
        """
        Saves the first n 5Ws answers to the csv document.

        :param document: The parsed Document
        :param n: Number of candidates to save.
        :return: None
        """

        self.writer.writerow([document.raw_title])

        # write to csv file
        for question in document.questions.keys():
            topn_annotations = document.annotations[question][:n]
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
                    if question in ['where', 'when']:
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
