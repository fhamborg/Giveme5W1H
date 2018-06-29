import csv

filepath = './evaluate_bbcfix.csv'

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
    return [score1, score2, score2]


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
        'who0': who[0],
        'who1': who[1],
        'who2': who[2],
        'what0': what[0],
        'what1': what[1],
        'what2': what[2],
        'when0': when[0],
        'when1': when[1],
        'when2': when[2],
        'where0': where[0],
        'where1': where[1],
        'where2': where[2],
        'why0': why[0],
        'why1': why[1],
        'why2': why[2],
        'how0': how[0],
        'how1': how[1],
        'how2': how[2]
    }


# get rows from read file
rows = list(csv_reader)
i = 1 # starting with 1 skips the header row

# init csv writer
with open('scores_bbc-fix.csv', 'w') as file_out:
    while i < len(rows):
        score_entry = get_score_entry(rows[i], rows[i+1])
        print(score_entry)

        if i == 1:
            csv_writer = csv.DictWriter(file_out, score_entry.keys())
            csv_writer.writeheader()

        csv_writer.writerow(score_entry)

        i += 2
