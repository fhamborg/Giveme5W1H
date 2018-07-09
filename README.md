# Giveme5W1H

<img align="right" height="128px" src="https://raw.githubusercontent.com/fhamborg/Giveme5W1H/master/misc/logo/logo-256.png" /> 

[![PyPI version](https://badge.fury.io/py/giveme5w1h.svg)](https://badge.fury.io/py/giveme5w1h)

Giveme5W1H is an open source, state of the art system that extracts phrases answering the journalistic 5W1H questions describing a news article's main event, i.e., who did what, when, where, why, and how? You can access the system through a simple RESTful API from any programming language or use it as a Python 3 library.

The figure below shows an excerpt of a news article with highlighted 5W1H phrases.
<img src="https://raw.githubusercontent.com/fhamborg/Giveme5W1H/master/misc/example5w1h.png" /> 

## Getting started
It's super easy, we promise!

### Installation
Giveme5W1H requires Python 3.6 (or later) to run. The following two commands will install Giveme5W1H and Stanford CoreNLP Server.
```
$ pip3 install giveme5w1h
$ giveme5w1h-corenlp install
```

Test if the Stanford CoreNLP Server setup was successful
```
$ giveme5w1h-corenlp
```
After a couple of second this should print `[main] INFO CoreNLP - StanfordCoreNLPServer listening at /0:0:0:0:0:0:0:0:9000`. To exit the program, press <kbd>CTRL</kbd>+<kbd>C</kbd>.

### Extract 5W1H Phrases
Giveme5W1H enables the extraction of 5W1H phrases from news articles. You can access Giveme5W1H's functionality via a RESTful API, or as a module from within your Python 3.6+ code. 

#### Starting the CoreNLP Server (mandatory) 
Either way, *you must start* the Stanford CoreNLP Server before using Giveme5W1H. To do so, run `giveme5w1h-corenlp` in a terminal, and do not close the terminal. 

##### Some information on performance
We decided to not integrate the CoreNLP Server transparently into Giveme5W1H mainly because the CoreNLP Server takes a lot of time until the initialization of all components is finished. Hence, the first run of Giveme5W1H after you started the CoreNLP Server, will likely take a couple of minutes (because components in CoreNLP Server are initialized on the fly). So, be sure to start up the server and use it to extract 5W1Hs from multiple news articles. See [below](#corenlp-host) if you want to use a CoreNLP Server that is running on a remote machine or different port.

#### RESTful API / webpage access
Start the RESTful API server that comes with Giveme5W1H (execute the following command in a separate shell, so that the CoreNLP Server started by the previous command runs in parallel):
```
$ giveme5w1h-rest
```
After a couple of seconds, you will see the following line:
```
 * Running on http://xxx.xxx.xxx.xxx:9099/ (Press CTRL+C to quit)
```

If you open the URL in your browser, you will see a page with a sample news article. Just click on `GET example`, or `run example` to analyze the shown article. You can also use this page to analyze your articles.

Of course, you can also access the RESTful API endpoints directly. You can access the endpoint at `http://localhost:9099/extract` via GET or POST requests. For GET and POST requests, the input fields are:
* `title` (mandatory)
* `description` (typically the lead paragraph)
* `text`
* `date` (must be readable by [parsedatetime](https://pypi.python.org/pypi/parsedatetime/))

Note, that GET requests have a limited request length, which may result in time-outs before the extraction of Giveme5W1H phrases was finished, and special character encoding can be tricky. If you have only the full text of an article, but separated by title, lead paragraph, and text, pass all text in the title field.

For POST requests, the required data format is the [news-please article format](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json). Besides the fields mentioned above, the following field is mandatory for POST request, too:
* `url`

#### Use within your own code (as a library)
Use the following code to extract 5W1H phrases from a single news article.
```python
from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import FiveWExtractor

extractor = MasterExtractor()
doc = Document(title, lead, text, date_publish)
doc = extractor.parse(doc)
```

Have a look at our sample Python scripts, for more information on extraction from a [single news article](https://github.com/fhamborg/Giveme5W1H/blob/master/Giveme5W1H/examples/extracting/parse_single_from_code.py), or a [folder consisting of multiple JSON files in news-please format](https://github.com/fhamborg/Giveme5W1H/blob/master/Giveme5W1H/examples/extracting/parse_documents.py). Of course, you can also run the sample scripts, e.g.:
```python
python3 -m Giveme5W1H.examples.extracting.parse_documents
```

# Additional Information
This section is currently subject to a major update. Some information may be outdated or redundant to the above information.

## Configuration
Configurations are optional.

### CoreNLP Host
You can also use a remotely installed  CoreNLP-Server. Simply parse the preprocessor another URL in case you run it on another machine:

```python
from Giveme5W1H.extractor.preprocessors.preprocessor_core_nlp import Preprocessor

preprocessor = Preprocessor('192.168.178.10:9000')
MasterExtractor(preprocessor=preprocessor)
```

### Output
- For file-based data - every input is transferred to the output
    -  For instance, annotated is already a part of the provided example files
- Each Question has their extracted candidates under extracted,
- Each Candidate, has parts, score and text property and their sentence index.
- Each part is structured as (payload, Postoken)
- Each payload has at least nlpToken which is the "basic" information.
- Each enhancer is saving his information under their name in the payload

See the [sample.json](https://github.com/fhamborg/Giveme5W1H/blob/master/misc/sample.json) for details.

## Processing-Files
Giveme5W can read and write only in a JSON format [example](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json).
[You find ready to use examples here](/examples/extracting)

> dID is used for matching input and output, not the filename!

There is an easy-to-use handler to work with files; these are all options::
```python
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


### Caching
CoreNLP and Enhancer have a long execution time; therefore it is possible to cache the result at the filesystem to speed up multiple executions.
Delete all files in "/cache", if you want to process them again, see examples in 'examples/extracting' for more details.

> if you add or remove enhancer, you must delete all files in the cache directory (if caching is enabled (set_preprocessed_path))


## Learn_Weights
/examples/misc/Learn_Weights.py is running the extractor with different weights from 0-10.
The best candidate is compared with the best annotation to get a score.
The calculated score, document id, and the used weights are saved per question under ./results.

> Because of the combined_scorer, each document is evaluated in each step. This can lead to entries with the same weights, but with different scores.


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

