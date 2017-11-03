import logging
import os
import sys
import json
import glob
import xml.etree.ElementTree as ET
import copy
import html
import re
import csv


from twisted.python.util import println

# converter to the get a more reliable annotation.json, see also readme

result = {}
# parsing the excel
with open(os.path.dirname(__file__) + '/IRC-annotations.csv', 'r') as excel_dunp_file:
    reader = csv.reader(excel_dunp_file)

    line_counter = 0
    file_name = None # this is the filename
    question = None
    for line in reader:
        # File-Header line
        if line_counter == 0:
            file_name = line[1]
            result[file_name] = {}
        # Placeholder
        elif line_counter == 15  or  line_counter == 16:
            print('')
        elif line_counter == 17:
            # end of one annotations: write
            line_counter = 0
            # questions tiself
        else:
            if line_counter % 4:
                # header itself per annotation
                question = line[0]
                result[file_name][question] = []
                # coder 1,2, 3
                count = line[5] + line[6] + line[7]
                annotated_text = line[0]

            result[file_name][question].append((annotated_text, count))
        line_counter = line_counter + 1

# write it to the disc
outfile = open(os.path.dirname(__file__) + '/annotation_new.json', 'w', encoding='utf8')

outfile.write(str(result))
outfile.close()

