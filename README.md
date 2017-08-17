# Giveme5W

Giveme5W(1H) is a state of the art open-source 5W Question Answering system for news articles. It can either be used through a simple RESTapi or directly included in existing Python projects. Depending on the configuration Giveme5W parses each document for the answers to the following  questions:

* **Who** is involved?
* **What** happened?
* **Where** did it take place?
* **When** did it happen?
* **Why** did it happen?
* **How** did it happen?

## Getting started
Before you can use Giveme5W, you need to make sure you have a CoreNLP-server up and running.
In the case you first to have to install CoreNLP please refer to the CoreNLPs extensive [documentation](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) and follow the instructions on how to install CoreNLP and start a server.

 * download the server itself from [here](https://stanfordnlp.github.io/CoreNLP/index.html#download)
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip) was the newest version
 * download also the english language package on the same page
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-english-corenlp-2017-06-09-models.jar) was the newest version
 * extract the server zip,
 * extract the language zip, copy it inside the server directory

Starting the CoreNLP server: 
```
$ nohup java -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 &
```

### (Optional) Configuration
If you are running CoreNLP on a different port or machine you have to first adjust the network settings for the prerpocessor:

(Bsp: extractor/examples/simple_api.py)
```python
# CoreNLP host
core_nlp_host = 'localhost:9000'
```

## File based usage
Giveme5W can read and write news in a json format [example](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json).
There is also a converter script to convert gate.xml files to json.

Files can be processed like a stream (parse_documents_simple.py) or can be loaded in advance and kept in memory (parse_documents.py).
Because CoreNLP server has a long execution time, it is possible to cache the result on the filesystem to speed up multiple executions.
The raw result is attached to each document under clp_result.

The included example files already preprocessed. So you can process them without a running CoreNLP server instance.
Delete all files in "/cache", if you want to precess them again.


## RESTapi
For the RESTapi it is possible to config the network:
```python
# basic configuration of the rest api
app = Flask(__name__)
log = logging.getLogger(__name__)
host = None
port = 5000
debug = False
options = None
```

You can also adjust the extractors which are used to examine the documents:
```python
# If desired, the selection of extractors can be changed and passed to the FiveWExtractor at initialization
    extractor_list = [
        action_extractor.ActionExtractor(),             # who & what
        environment_extractor.EnvironmentExtractor(),   # when & where
        cause_extractor.CauseExtractor()                # why
        method_extractor.MethodExtractor()              # how
    ]
    extractor = FiveWExtractor(preprocessor, extractor_list)
```

### Start the python script
```
$ python extractor/examples/simple_api.py
```

Now you can send articles through the RESTapi to GiveMe5W. 
The API supports the following JSON fields:

* title (always required!)
* description
* text

## Learn_Weights
Learn_Weights is running the extractor with different weights.
The best candidate is compared with the best annotation to get a score.
The calculated score, document id and the used weights are saved per question under ./results.

Because of the combined_scorer, each document is evaluated in each step. 
This can lead to entries with the same weights, but with different scores.






## License
The project is licensed under the Apache License 2.0. Make sure that you use Giveme5W in compliance with applicable law. Copyright 2016 The Giveme5W team
