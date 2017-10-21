# Giveme5W

Giveme5W(1H) is a state of the art open-source 5W Question Answering system for news articles. It can either be used through a simple RESTapi or directly included in existing Python projects. Depending on the configuration Giveme5W parses each document for the answers to the following  questions:

* **Who** is involved?
* **What** happened?
* **Where** did it take place?
* **When** did it happen?
* **Why** did it happen?
* **How** did it happen?

## Getting started
Before you can use Giveme5W, you need to make sure you have  CoreNLP-Server runtimes.

If you have to install CoreNLP, please refer to the CoreNLPs extensive [documentation](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) and follow the instructions on how to install CoreNLP and start a server.

 * download the server itself from [here](https://stanfordnlp.github.io/CoreNLP/index.html#download)
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip) was the newest version
 * download also the english language package on the same page
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-english-corenlp-2017-06-09-models.jar) was the newest version
 * extract the server zip,
 * extract the language zip, copy it inside the server directory
 * copy it into [Giveme5W-runtime-resources](#Giveme5W-runtime-resources) next to your repository folder

Run environment_enhancer.py to start up coreNLP.

## Configuration
All configurations are optional.

### CoreNLP Host
By default, Giveme5W tries to start the server with default port.

You can prevent this by setting up a preprocessor with another url in case you run it on another masch:
(Bsp: extractor/examples/simple_api.py)
```python
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
preprocessor = Preprocessor('localhost:9000')
FiveWExtractor(preprocessor=preprocessor)
```

Then start up CoreNLP by:
```
$ nohup java -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 &
```


### Output Configuration

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
CoreNLP and Enhancer have a long execution time, therefore it is possible to cache the result on the filesystem to speed up multiple executions.

The included example files already preprocessed. So you can process them without a running CoreNLP server instance.
Delete all files in "/cache", if you want to precess them again.

> if you add or remove enhancer, you must delete all files in the cache directory (if cache is enabled (set_preprocessed_path))


## REST-Service
Its also possible to use giveme5W as rest service.

```
$ python extractor/examples/extracting/simple_api.py
```
> Check the code for more details, it is well documented

* GET AND POST requests are supported
    * Keep in mind that GET has a limited request length and special character encoding can be tricky
* Input Field
    * title (mandatory)
    * description
    * text
* Output
    * [news-please format](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json)


## Learn_Weights
/examples/misc/Learn_Weights.py is running the extractor with different weights from 0-10.
The best candidate is compared with the best annotation to get a score.
The calculated score, document id and the used weights are saved per question under ./results.

> Because of the combined_scorer, each document is evaluated in each step. This can lead to entries with the same weights, but with different scores.

# Giveme5W-Enhancer
Enhancer can perform further feature extraction and/or selection.
Sourcecode of all enhancer is saved under /codebase/ to ensure results are reproachable at any time.

## AIDA
Aida is available as webservice or can be installed local.
Because of the complex installation and size; online service is set up as default.

### Online Service
Service is limited to 1000 request per day.
You can find details [here](https://www.ambiverse.com/pricing/)

### Local Installation
> AIDA repo went offline, check /codebase/ for the last version

- Source-Download [3.0.4](https://github.com/yago-naga/aida/archive/3.0.4.zip)
- copy sample_settings into settings
- open settings/aida.properties set
  - dataAccess = dmap
- create in settings a file 'dmap_aida.properties', set
  - mapsToLoad = all
  - default.preloadKeys = true
  - default.preloadValues = true


- Data-Download [DMaps](http://resources.mpi-inf.mpg.de/yago-naga/aida/download/entity-repository/AIDA_entity_repository_2014-01-02v10_dmap.tar.bz2)
 - Check also [here](http://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/aida/downloads/) for update
- Decompress the bz2 file
 - use pbzip2 on osx/linux for fast decompression
- create a folder 'dMaps' in the AIDA root directory
 - Unpack the tar file into the dMaps folder
- run
 - mvn package -Dmaven.test.skip=true

> - Warning database dump has 20GB
  - Your computer should have at least 15GB ram

Use environment_enhancer.py to startup CoreNLP and AIDA together.

usage:
```python
from Giveme5W_enhancer.aida import Aida
extractor = FiveWExtractor(extractors=[
        environment_extractor.EnvironmentExtractor(),
    ], enhancement=[
        Aida('when', 'http://myOptionalAidaServer:8080')
    ])
```

## Heideltime
[Heideltime](https://github.com/HeidelTime/heideltime) works out of the box with the 'Giveme5W-runtime-resources'.
This enhancement parse further the "when" answers to get precise time definitions.

- Download [2.2.1](https://github.com/HeidelTime/heideltime/releases/download/VERSION2.2.1/heideltime-standalone-2.2.1.zip)
- Copy it to Giveme5W-runtime-resources
- Follow the installation instruction Manual.pdf
> You must use treeTagger, Heideltime is not compatible with CoreNLP 3.X

usage:
```python
from Giveme5W_enhancer.heideltime import Heideltime
extractor = FiveWExtractor(extractors=[
        environment_extractor.EnvironmentExtractor(),
    ], enhancement=[
        Heideltime('when')
    ])
```

The enhancement is stored per candidate, a published date is mandatory for news to resolve relative times.
Example output:
```json
{
          "score": 0.5220949263502455,
          "words": [
            {
              "text": "Today",
              "tag": "NN"
            }
          ],
          "enhancement": {
            "heideltime": {
              "TimeML": {
                "TIMEX3": {
                  "@tid": "t1",
                  "@type": "DATE",
                  "@value": "2016-11-09",
                  "#text": "Today"
                }
              }
            }
          }
        },
```

# Startup - Scripts -> Giveme5W-runtime-resources
Giveme5W can start up everything. Check examples/startup scripts.
To do so all libraries must be located in the same directory 'Giveme5W-runtime-resources' and next to the Giveme5W folder.

- Folder Structure
    - Giveme5W (Master)
    - Giveme5W-enhancer (Master)
    - Giveme5W-runtime-resources (Master)
        - aida-3.0.4
        - heideltime-standalone
        - stanford-corenlp-full-2016-10-31
        - treeTagger

You can change this directory with:
```shell
Config.get()['Giveme5W-runtime-resources'] = './../Giveme5W-runtime-resources'
```

# License
The project is licensed under the Apache License 2.0. Make sure that you use Giveme5W in compliance with applicable law. Copyright 2016 The Giveme5W team
