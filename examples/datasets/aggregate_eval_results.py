import csv

filepath = './evaluate_bbc.csv'

csv_reader = csv.reader(open(filepath, 'r'), delimiter=';', quoting=csv.QUOTE_MINIMAL)

index_step = 2
index_who = 1
index_what = index_who + index_step
index_when = index_what + index_step
index_where = index_when + index_step
index_why = index_where + index_step
index_how = index_why + index_step
index_dict = {
    'who': index_who,
    'what': index_what,
    'when': index_when,
    'where': index_where,
    'why': index_why,
    'how': index_how
}


def get_scores(row, question):
    """
    returns all two scores
    :param row:
    :param question:
    :return:
    """
    index = index_dict[question]
    score1 = row[index]
    score2 = row[index+1]
    if not score2:
        score2 = score1
    return [score1, score2]


def get_score_entry(row, row_next):
    category = row[0]
    who = get_scores(row_next, 'who')
    what = get_scores(row_next, 'what')
    when = get_scores(row_next, 'when')
    where = get_scores(row_next, 'where')
    why = get_scores(row_next, 'why')
    how = get_scores(row_next, 'how')

    return {
        'category': category,
        'who': who,
        'what': what,
        'when': when,
        'where': where,
        'why': why,
        'how': how
    }


rows = list(csv_reader)
i = 1 # starting with 1 skips the header row
while i < len(rows):
    score_entry = get_score_entry(rows[i], rows[i+1])
    i += 2
    print(score_entry)

