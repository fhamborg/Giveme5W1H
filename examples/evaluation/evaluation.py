import os
import csv
from extractor.tools.file.handler import Handler

# evaluates results with ICR and GP

# measure_agreement function to keep code more readable
def measure_agreement(a,b):
    if a == b:
        return 1
    else:
        return 0

# convert ICR rating from 0 to 2 to GP scala 0 - 1
# (done on purpose in easy to read way, aka without normalization )
def to_precision_generalized (a):
    if a == 0:
        # not relevant:
        return 0
    elif a == 1:
        # partial relevant
        return 0.5
    else:
        # relevant
        return 1

# AB AC	CB
with open(os.path.dirname(__file__) + '/evaluation_data_how.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)

    header = True
    ICR = 0
    ICR_cat = {}
    generalized_precision = 0
    generalized_precision_cat = {}

    aggrement = []
    for line in reader:
        if header:
            header = False
        else:
            category = line[2]
            coder_a = int(line[5])
            coder_b = int(line[6])
            coder_c = int(line[7])

            # measure pairwise agreement AB, AC, CB
            ab = measure_agreement(coder_a, coder_b)
            ac = measure_agreement(coder_a, coder_c)
            cb = measure_agreement(coder_c, coder_b)

            # measure agreement of the pairs
            # inter-rater reliability is based on agreement between pairs of raters.
            line_agrement = (ab + ac + cb) / 3

            # irc global
            ICR = ICR + line_agrement

            # irc per category
            ICR_cat[category] = ICR_cat.get(category, 0) + line_agrement

            # gp global
            tmp_gp = to_precision_generalized(coder_a) + to_precision_generalized(coder_b) + to_precision_generalized(coder_c)
            generalized_precision = generalized_precision + tmp_gp

            # gp per category
            generalized_precision_cat[category] = generalized_precision_cat.get(category, 0) + tmp_gp

            # saved, for possible output
            aggrement.append((category, ab, ac, cb, line_agrement, tmp_gp))

    line_count = len(aggrement)
    cat_count = len(ICR_cat)
    line_count_cat = line_count/cat_count

    # for GP:  die ganzen ratings zusammenaddieren und durch anzahl der ratings teilen
    rating_count = line_count * 3  # each doc was rated by 3 coder
    rating_count_cat = rating_count / cat_count

    # output
    print('Global ICR: ' + str(ICR / line_count))
    print('Global GP: ' + str(generalized_precision / rating_count))

    for cat in ICR_cat:
        val = ICR_cat[cat]
        print( cat + ' ICR: ' + str(val/line_count_cat))

        val = generalized_precision_cat[cat]
        print(cat + ' GP: ' + str(val / rating_count_cat))

