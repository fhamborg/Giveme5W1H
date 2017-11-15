import csv
import json
import os


# converter to the get a more reliable annotation.json, see also readme

def to_int(input):
    if input != '':
        return int(input)
    return 0


result = {}
# parsing the excel
with open(os.path.dirname(__file__) + '/IRC-annotations.csv', 'r') as excel_dunp_file:
    reader = csv.reader(excel_dunp_file)

    line_counter = 0
    file_name = None  # this is the filename
    question = None
    for line in reader:
        # File-Header line
        if line_counter == 0:
            file_name = line[1]
            result[file_name] = {}
        # Placeholder
        elif line_counter == 18:
            print('')
        elif line_counter == 19:
            # end of one annotations: write
            line_counter = -1
            # questions tiself
        else:
            if line_counter == 1 or line_counter == 4 or line_counter == 7 or line_counter == 10 or line_counter == 13 or line_counter == 16:
                # header itself per annotation
                question = line[0]
                result[file_name][question] = []
            # coder 1,2, 3
            count = to_int(line[3]) + to_int(line[4]) + to_int(line[5])
            annotated_text = line[1]
            if annotated_text and len(annotated_text) > 0:
                result[file_name][question].append((annotated_text, count))
        line_counter = line_counter + 1

# write it to the disc
outfile = open(os.path.dirname(__file__) + '/annotation_new.json', 'w', encoding='utf8')

outfile.write(json.dumps(result, indent=2, sort_keys=True))
outfile.close()
