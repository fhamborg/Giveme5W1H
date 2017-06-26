# GiveMe5W

GiveMe5W is an state of the art open-source 5W Question Answering system for news articles. It can either be used through a simple RESTapi or directly included in existing Python projects. Depending on the configuration  GiveMe5W parses each document for thepasse answeres of the following  questions:

* **Who** is involved?
* **What** happened?
* **Where** did it take place?
* **When** did it happen?
* **Why** did it happen?

## Getting started
Before you can use GiveMe5W you need to make sure you have an CoreNLP-server up and running.
In case you have to first install CoreNLP please refere to the CoreNLPs extensive [documentation](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) and follow the instructions on how to install CoreNLP and start a server.

Starting the CoreNLP server: 
'''
$ nohup java -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 &
'''

### (Optional) Configuration
If you are running CoreNLP on a different port or machine you have to first adjust the network settings for the prerpocessor:

(Bsp: examples/simple_api.py)
'''python
# CoreNLP host
core_nlp_host = 'localhost:9000'
'''

## License

The project is licensed under the Apache License 2.0. Make sure that you use news-GiveMe5W in compliance with applicable law. Copyright 2016 The GiveMe5W team
