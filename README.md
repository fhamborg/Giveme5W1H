# GiveMe5W

GiveMe5W is an state of the art open-source 5W Question Answering system for news articles. It can either be used through a simple RESTapi or directly included in existing Python projects. Depending on the configuration  GiveMe5W parses each document for thepasse answeres of the following  questions:

* **Who** is involved?
* **What** happened?
* **Where** did it take place?
* **When** did it happen?
* **Why** did it happen?

## Getting started
Before you can use GiveMe5W you need to make sure you have an CoreNLP-server up and running. Please refere to the CoreNLP documentation for detailed instruction on how to install CoreNLP and start a server.

Start teh CoreNLP server: ''' $ nohup java -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 & (Optional) Configuration ''' If you are running your CoreNLP instance on a different Port than 9000 or on a remote machine you will have to adjust the network settings:

(Bsp: simple_api.py)

from newsplease import NewsPlease article = NewsPlease.from_url('https://www.nytimes.com/2017/02/23/us/politics/cpac-stephen-bannon-reince-priebus.html?hp') print(article.title) If your server is not hosted on your local machine or

License

The project is licensed under the Apache License 2.0. Make sure that you use news-GiveMe5W in compliance with applicable law. Copyright 2016 The GiveMe5W team
