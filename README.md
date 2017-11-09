# Giveme5W

Giveme5W(1H) is a state of the art open-source 5W Question Answering system for news articles. It can either be used through a simple RESTapi or directly included in existing Python projects. Depending on the configuration Giveme5W parses each document for the answers to the following  questions:

* **Who** is involved?
* **What** happened?
* **Where** did it take place?
* **When** did it happen?
* **Why** did it happen?
* **How** did it happen?

## Getting started
Before you can use Giveme5W, you need to make sure you have CoreNLP-Server runtimes.

If you have to install CoreNLP, please refer to the CoreNLPs extensive [documentation](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) and follow the instructions on how to install CoreNLP and start a server.

 * download the server itself from [here](https://stanfordnlp.github.io/CoreNLP/index.html#download)
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip) was the newest version
 * download also the english language package on the same page
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-english-corenlp-2017-06-09-models.jar) was the newest version
 * extract the server zip,
 * extract the language zip, copy it inside the server directory
 * copy it into [Giveme5W-runtime-resources](#Giveme5W-runtime-resources) next to your repository folder

Start coreNLP by yourself (Windows, Linux, OSX)
``` bash
 java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```
or
(this is optional, there is no need to use the startup scripts;
 this is only for a simple startup while developing etc.; Linux, OSX)

```python
python3 -m examples.startup.environment
```
> see also Startup - Scripts -> Giveme5W-runtime-resources


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


# Startup - Scripts -> Giveme5W-runtime-resources
Giveme5W can start up everything for you. Check examples/startup scripts.
This is optional, especially without enhancer
All libraries must be located in the same directory 'Giveme5W-runtime-resources' and next to the Giveme5W folder.

- Folder Structure
    - Giveme5W (Master)
    - Giveme5W_NewsCluster_enhancer (Master)
    - Giveme5W-runtime-resources (Master)
        - aida-3.0.4
        - heideltime-standalone
        - stanford-corenlp-full-2016-10-31
        - treeTagger

You can change this directory with:
```shell
Config.get()['Giveme5W-runtime-resources'] = './../Giveme5W-runtime-resources'
```

> Unfortunately there is a bug in PyCharm at the time of writing: if you are viewing multiple project at once, you have to add an additional /../ to the path

# License
The project is licensed under the Apache License 2.0. Make sure that you use Giveme5W in compliance with applicable law. Copyright 2016 The Giveme5W team
