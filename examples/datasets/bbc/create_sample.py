import os, numpy
import json
from glob import glob
import hashlib


def read_random(directory, count):


    glob_pattern = os.path.join(directory, '*.txt')
    files = sorted(glob(glob_pattern), key=os.path.getctime)
    return numpy.random.choice(a=files,size=count).tolist()


# Variables

# Change these if you wan` another sample size
categories = ['business', 'entertainment', 'politics', 'sport','tech']
category_size = 12

##
## tool itself
inputPath = os.path.dirname(__file__) + '/data_raw'
outputPath = os.path.dirname(__file__) + '/data'




#delete the old files
for the_file in os.listdir(outputPath):
    file_path = os.path.join(outputPath, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)


# reading files
sample_set = []
for category in categories:
    full_path = inputPath + '/' + category + '/'
    sample_set = sample_set + read_random(full_path, category_size)


print(len(sample_set))
# write data
for path in sample_set:
    with open(path, encoding='utf-8') as data_file:
        title = data_file.readline().rstrip()
        text = data_file.read().rstrip()
        text = text[1:] # removes a trailing new line

        filename = os.path.basename(path)
        tmp, dir = os.path.split(os.path.split(path)[0])
        sID = 'bbc'+dir+filename
        dID = hashlib.sha224(sID.encode('utf-8')).hexdigest()

        output_object = {'dId':  dID, 'title': title, 'text': text, 'description':'','category': dir, 'filename': filename}
        with open( outputPath + '/' + output_object['dId'] + '.json', 'w',  encoding='utf-8') as outfile:
            json_dump = json.dumps(output_object, sort_keys=False, indent=2)
            outfile.write(json_dump)
            outfile.close()


