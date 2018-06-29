# Giveme5W1H

<img align="right" height="128px" src="https://raw.githubusercontent.com/fhamborg/Giveme5W1H/master/misc/logo/logo-256.png" /> 

[![PyPI version](https://badge.fury.io/py/giveme5w1h.svg)](https://badge.fury.io/py/giveme5w1h)

Giveme5W1H is an open source, state of the art system that extracts phrases answering the journalistic 5W1H questions describing a news article's main event, i.e., who did what, when, where, why, and how? You can access the system through a simple RESTful API from any programming language or use it as a Python 3 library.

The figure below shows an excerpt of a news article with highlighted 5W1H phrases.
<img src="https://raw.githubusercontent.com/fhamborg/Giveme5W1H/master/misc/example5w1h.png" /> 

## Getting started
Giveme5W1H requires Python 3.6 or later. 

### Installation
We are currently working to create a PyPI package so that you can install Giveme5W1H easily using PIP. Until then, simply follow the installation instructions below (tested on Linux and MacOS).

#### Get Giveme5W1H
```
git clone https://github.com/fhamborg/Giveme5W1H.git # or if you've setup SSH: git clone git@github.com:fhamborg/Giveme5W1H.git
cd Giveme5W1H
```
And install its dependencies:
```
pip3 install -r requirements.txt
```

#### Stanford CoreNLP Server
Giveme5W1H requires the Stanford Core Server to perform text preprocessing. Giveme5W1H has been tested with the 2017-06-09 build. Other builds may work as well, but no support will be given.

Get the Stanford Core Server
```
mkdir runtime-resources && cd runtime-resources
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip && unzip stanford-corenlp-full-2017-06-09.zip && rm stanford-corenlp-full-2017-06-09.zip
wget http://nlp.stanford.edu/software/stanford-english-corenlp-2017-06-09-models.jar && mv stanford-english-corenlp-2017-06-09-models.jar stanford-corenlp-full-2017-06-09/
cd ..
```

Test if the Stanford Core Server setup was successful
```
python3 -m examples.startup.environment
```
This should print after a couple of seconds `[main] INFO CoreNLP - StanfordCoreNLPServer listening at /0:0:0:0:0:0:0:0:9000`. If it does not, press `Ctrl+C` to abort the execution of the script, and have a look at the stacktrace shown.

### Extract 5W1H Phrases
You can access Giveme5W1H's functionality via a RESTful API, or as a module from within your own Python 3.6+ code. 

#### RESTful API

```

```

Environment is now running. Start parsing news_please files
```python
python3 -m examples.extracting.parse_documents
```
or start the rest api.
```python
python3 -m examples.extracting.server
```

> Its recommended to use a proper IDE(e.g. PyCharm) if you want to use Enhancer,
  otherwise you have to add the projects to your environment
### PIP
There is a pip package just run
```batch
pip install giveme5w1h
```

you can start afterwards the server with giveme5w1h.
> expects a CoreNLP server running under: http://localhost:9090/

> webserver is also bound to your external IP http://localhost:9099/!

## Configuration
Configurations are optional.

### CoreNLP Host

You can use not local installed  CoreNLP-Server. Simply parse the the preprocessor another url in case you run it on another machine:

```python
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
preprocessor = Preprocessor('192.168.178.10:9000')
FiveWExtractor(preprocessor=preprocessor)
```



### Output

- For file based data - every input is transferred to the output
    -  For instance, annotated is already a part of the provided example files
- Each Question has their extracted candidates under extracted,
- Each Candidate, has parts, score and text property and their sentence index.
- Each parts is structured as (payload, Postoken)
- Each payload has at least nlpToken which is the "basic" information.
- Each enhancer is saving his information under their own name in the payload

See the example below for details:
```json
 "who": {
      "annotated": [
        {
          "text": "Several people"
        },
        {
          "text": "dozens injured"
        }
      ],
      "label": "who",
      "extracted": [
        {
          "parts": [
            [
              {
                "nlpToken": {
                  "index": 8,
                  "word": "Croydon",
                  "originalText": "Croydon",
                  "lemma": "Croydon",
                  "characterOffsetBegin": 3148,
                  "characterOffsetEnd": 3155,
                  "pos": "NNP",
                  "ner": "LOCATION",
                  "speaker": "PER0",
                  "before": " ",
                  "after": " "
                },
                "aida": [
                  {
                    "mention": {
                      "allEntities": [
                        {
                          "kbIdentifier": "YAGO:Croydon",
                          "disambiguationScore": "0.23577"
                        }
                      ],
                      "offset": 3148,
                      "name": "Croydon",
                      "length": 7,
                      "bestEntity": {
                        "kbIdentifier": "YAGO:Croydon",
                        "disambiguationScore": "0.23577"
                      }
                    },
                    "bestEntityMetadata": {
                      "knowledgebase": "YAGO",
                      "depictionurl": "http://upload.wikimedia.org/wikipedia/commons/0/08/Croydon_Town_Hall_-_geograph.org.uk_-_432983.jpg",
                      "depictionthumbnailurl": "http://upload.wikimedia.org/wikipedia/commons/thumbCroydon_Town_Hall_-_geograph.org.uk_-_432983.jpg/200px-Croydon_Town_Hall_-_geograph.org.uk_-_432983.jpg",
                      "importance": 0.0007512499244432548,
                      "entityId": "Croydon",
                      "type": [
                        "YAGO_wordnet_district_108552138",
                        "YAGO_yagoPermanentlyLocatedEntity",
                        "YAGO_yagoLegalActorGeo",
                        "YAGO_wordnet_medium_106254669",
                        "YAGO_wordnet_urban_area_108675967",
                        "YAGO_wikicategory_Market_towns_in_Surrey",
                        "YAGO_wordnet_municipality_108626283",
                        "YAGO_wordnet_instrumentality_103575240",
                        "YAGO_wordnet_market_town_108672073",
                        "YAGO_wikicategory_locations",
                        "YAGO_wikicategory_Districts_of_London_listed_in_the_Domesday_Book",
                        "YAGO_wordnet_region_108630985",
                        "YAGO_yagoGeoEntity",
                        "YAGO_wordnet_physical_entity_100001930",
                        "YAGO_wikicategory_Districts_of_Croydon",
                        "YAGO_wikicategory_Post_towns_in_the_CR_postcode_area",
                        "YAGO_wordnet_entity_100001740",
                        "YAGO_wordnet_object_100002684",
                        "YAGO_wordnet_area_108497294",
                        "YAGO_wordnet_geographical_area_108574314",
                        "YAGO_wikicategory_Areas_of_London",
                        "YAGO_wikicategory_Market_towns_in_London",
                        "YAGO_wordnet_location_100027167",
                        "YAGO_wordnet_whole_100003553",
                        "YAGO_wikicategory_Media_and_communications_in_Croydon",
                        "YAGO_wordnet_artifact_100021939",
                        "YAGO_wordnet_administrative_district_108491826",
                        "YAGO_wordnet_town_108665504"
                      ],
                      "readableRepr": "Croydon",
                      "url": "http://en.wikipedia.org/wiki/Croydon"
                    }
                  }
                ]
              },
              "NNP"
            ]..
          "score": 1.0,
          "text": "Croydon MPS ( @MPSCroydon ) November 9 , 201 \" There",
          "nlpIndexSentence": 21:

```
>


> see configuration.py for all settings and description


Use the configuration Singleton to make adjustments
```python
from extractor.configuration import Configuration as Config
Config.get()['candidate']['nlpIndexSentence'] = False
```


## Processing-Files
Giveme5W can read and write only in a json format [example](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json).
[You find ready to used examples here](/examples/extracting)

> dID is used for matching input and output, not the filename!

There is a easy to use handler to work with files, these are all options::
``` python
 documents = (
        # initiate the file handler with the input directory
        Handler(inputPath)
            # add giveme5w extractor  (it would only copying files without...)
            .set_extractor(extractor)

            # Optional: set a output directory
            .set_output_path(outputPath)

            # Optional: set a path to cache and load preprocessed documents (CoreNLP & Enhancer results)
            .set_preprocessed_path(preprocessedPath)

            # Optional: limit the documents read from the input directory (handy for development)
            .set_limit(1)

            # Optional: resume ability, skip input file if its already in output
            .skip_documents_with_output()

            # load and saves all document runtime objects for further programming
            .preload_and_cache_documents()

            ## setup is done: executing it
            .process()

            # get the processed documents, this can only be done because preload_and_cache_documents was called
            .get_documents()
    )
```
Check the examples under parse_documents_simple.py and parse_documents.py for more details


### CACHE
CoreNLP and Enhancer have a long execution time, therefore it is possible to cache the result at the filesystem to speed up multiple executions.
Delete all files in "/cache", if you want to precess them again, see examples in 'examples/extracting' for more details.

> if you add or remove enhancer, you must delete all files in the cache directory (if cache is enabled (set_preprocessed_path))

## REST-Service
Its also possible to use giveme5W as rest service, there is also a very simple html ui.

```
$ python extractor/examples/extracting/server.py
```
> Check the code for more details, it is well documented

* GET AND POST requests are supported
    * Keep in mind that GET has a limited request length and special character encoding can be tricky
* Input Field
    * title (mandatory)
    * description
    * text
    * date (must be readable by [parsedatetime](https://pypi.python.org/pypi/parsedatetime/))
* Output
    * [news-please format](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json)


## Learn_Weights
/examples/misc/Learn_Weights.py is running the extractor with different weights from 0-10.
The best candidate is compared with the best annotation to get a score.
The calculated score, document id and the used weights are saved per question under ./results.

> Because of the combined_scorer, each document is evaluated in each step. This can lead to entries with the same weights, but with different scores.


# Startup - Scripts -> Giveme5W-runtime-resources
Giveme5W can start up everything for you. Check examples/startup scripts.
This is optional, especially without enhancer
All libraries must be located in the same directory 'runtime-resources' located inside Giveme5W .

- Folder Structure
    - Giveme5W                      (Master)
        - runtime-resources
            - aida-3.0.4
            - heideltime-standalone
            - stanford-corenlp-full-2016-10-31
            - treeTagger
    - Giveme5W_NewsCluster_enhancer (Master)


You can change this directory with:
```shell
Config.get()['Giveme5W-runtime-resources'] = './runtime-resources'
```

> Unfortunately there is a bug in PyCharm at the time of writing: if you are viewing multiple project at once, you have to add an additional /../ to the path


## How to cite
If you are using Giveme5W1H, please cite our [paper](http://www.gipp.com/wp-content/papercite-data/pdf/hamborg2018a.pdf) ([ResearchGate](https://www.researchgate.net/publication/325176943_Extraction_of_Main_Event_Descriptors_from_News_Articles_by_Answering_the_Journalistic_Five_W_and_One_H_Questions)):
```
@InProceedings{Hamborg2018a,
author    = {Hamborg, Felix and Breitinger, Corinna and Schubotz, Moritz and Lachnit, Soeren and Gipp, Bela},
title     = {Extraction of Main Event Descriptors from News Articles by Answering the Journalistic Five W and One H Questions},
booktitle = {Proceedings of the ACM/IEEE-CS Joint Conference on Digital Libraries (JCDL)},
year      = {2018},
month     = {Jun.},
location  = {Fort Worth, USA},
url       = {https://doi.org/10.1145/3197026.3203899},
doi       = {10.1145/3197026.3203899}
}
```

Giveme5W1H is based on the 5W extraction system [Giveme5W](https://www.gipp.com/wp-content/papercite-data/pdf/hamborg2018.pdf) ([ResearchGate](https://www.researchgate.net/publication/323582278_Giveme5W_Main_Event_Retrieval_from_News_Articles_by_Extraction_of_the_Five_Journalistic_W_Questions), [Mendeley](https://www.mendeley.com/research-papers/giveme5w-main-event-retrieval-news-articles-extraction-five-journalistic-w-questions/?utm_source=desktop&utm_medium=1.17.13&utm_campaign=open_catalog&userDocumentId=%7B6945b48b-a775-4b85-b09b-f321b316f6da%7D)), which can be cited as follows:
```
@InProceedings{Hamborg2018,
  author    = {Hamborg, Felix and Lachnit, Soeren and Schubotz, Moritz and Hepp, Thomas and Gipp, Bela},
  title     = {Giveme5W: Main Event Retrieval from News Articles by Extraction of the Five Journalistic W Questions},
  booktitle = {Proceedings of the iConference 2018},
  year      = {2018},
  month     = {March},
  location  = {Sheffield, UK},
  url       = {https://doi.org/10.1007/978-3-319-78105-1_39},
  doi       = {10.1007/978-3-319-78105-1_39}
}
```
You can find more information on this and other news projects on our [website](https://felix.hamborg.eu/).

## Contribution and support
Do you want to contribute? Great, we are always happy for any support on this project! Just send a pull request. By contributing to this project, you agree that your contributions will be licensed under the project's license (see below). If you have questions or issues while working on the code, e.g., when implementing a new feature that you would like to have added to Giveme5W1H, open an issue on GitHub and we'll be happy to help you. Please note that we usually do not have enough resources to implement features requested by users - instead we recommend to implement them yourself, and send a pull request. 

## License
Licensed under the Apache License, Version 2.0 (the "License"); you may not use Giveme5W1H except in compliance with the License. A copy of the License is included in the project, see the file [LICENSE.txt](LICENSE.txt).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 

The Giveme5W1H logo is courtesy of [Mario Hamborg](https://mario.hamborg.eu/). 

Copyright 2018 The Giveme5W1H team

