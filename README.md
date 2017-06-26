# GiveMe5W

GiveMe5W is a state of the art open-source 5W Question Answering system for news articles. It can either be used through a simple RESTapi or directly included in existing Python projects. Depending on the configuration GiveMe5W parses each document for the answers to the following  questions:

* **Who** is involved?
* **What** happened?
* **Where** did it take place?
* **When** did it happen?
* **Why** did it happen?

## Getting started
Before you can use GiveMe5W, you need to make sure you have a CoreNLP-server up and running.
In the case you first to have to install CoreNLP please refer to the CoreNLPs extensive [documentation](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) and follow the instructions on how to install CoreNLP and start a server.

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

For the RESTapi it is also possible to network config:
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
## License

The project is licensed under the Apache License 2.0. Make sure that you use news-GiveMe5W in compliance with applicable law. Copyright 2016 The GiveMe5W team
