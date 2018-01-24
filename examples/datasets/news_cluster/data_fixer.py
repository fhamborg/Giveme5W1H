import glob

"""
    this script is fixing errors found in the data, after processing
"""

# final fixes for known errors
for filepath in glob.glob('output/*.json'):
    # Read in the file
    with open(filepath, 'r') as file:
        filedata = file.read()

    # AIDA has a wrong URL for the Dallas Airport
    wrong = 'http://en.wikipedia.org/wiki/Dallas/Dallas%2FFort%20Worth%20International%20Airport'
    correct = 'http://en.wikipedia.org/wiki/Dallas%2FFort%20Worth%20International%20Airport'
    # Replace the target string
    filedata = filedata.replace(wrong, correct)

    # Write the file out again
    with open(filepath, 'w') as file:
        file.write(filedata)