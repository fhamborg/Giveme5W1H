import glob
import json

import io

links = {}
for filepath in glob.glob('output/*.json'):
    with io.open(filepath, 'r', encoding='utf-8-sig') as data_file:
        data = json.load(data_file)
        cat = data.get('category')
        if cat:
            if links.get(cat) is None:
                links[cat] = []
            links[cat].append(data['url'])
print(json.dumps(links, indent=4, sort_keys=True))