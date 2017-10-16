import csv
import os

# evaluates results with ICR and GP


filename = 'evaluation_data_how.csv'

# change csv column index, if necessary here
category_index = 2
coder_a_index = 5
coder_b_index = 6
coder_c_index = 7


# measure_agreement function to keep code more readable
def measure_agreement(a, b):
    if a == b:
        return 1
    else:
        return 0


# convert ICR rating from 0 to 2 to GP scala 0 - 1
# (done on purpose in easy to read way, aka without normalization )
def to_precision_generalized(a):
    if a == 0:
        # not relevant:
        return 0
    elif a == 1:
        # partial relevant
        return 0.5
    else:
        # relevant
        return 1


with open(os.path.dirname(__file__) + '/' + filename, 'r') as csvfile:
    reader = csv.reader(csvfile)

    is_header = True
    ICR = 0
    ICR_cat = {}
    generalized_precision = 0
    generalized_precision_cat = {}

    aggrement = []
    for line in reader:
        if is_header:
            is_header = False
        else:
            category = line[category_index]
            coder_a = int(line[coder_a_index])
            coder_b = int(line[coder_b_index])
            coder_c = int(line[coder_c_index])

            # measure pairwise agreement AB, AC, CB
            ab = measure_agreement(coder_a, coder_b)
            ac = measure_agreement(coder_a, coder_c)
            cb = measure_agreement(coder_c, coder_b)

            # measure agreement of the pairs
            # inter-rater reliability is based on agreement between pairs of raters.
            line_agreement = (ab + ac + cb) / 3

            # irc global
            ICR = ICR + line_agreement

            # irc per category
            ICR_cat[category] = ICR_cat.get(category, 0) + line_agreement

            # gp global
            tmp_gp = to_precision_generalized(coder_a) + to_precision_generalized(coder_b) + to_precision_generalized(
                coder_c)

            generalized_precision = generalized_precision + tmp_gp

            # gp per category
            generalized_precision_cat[category] = generalized_precision_cat.get(category, 0) + tmp_gp

            # saved, for possible output
            aggrement.append((category, ab, ac, cb, line_agreement, tmp_gp))

    line_count = len(aggrement)
    cat_count = len(ICR_cat)
    line_count_cat = line_count / cat_count

    # for GP: summarize all ratings dividing by the number of all ratings
    rating_count = line_count * 3  # each doc was rated by 3 coder
    rating_count_cat = rating_count / cat_count

    # output
    print('Global ICR: ' + str(ICR / line_count))
    print('Global GP: ' + str(generalized_precision / rating_count))

    for cat in ICR_cat:
        val = ICR_cat[cat]
        print(cat + ' ICR: ' + str(val / line_count_cat))

        val = generalized_precision_cat[cat]
        print(cat + ' GP: ' + str(val / rating_count_cat))
