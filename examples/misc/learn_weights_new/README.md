# Learn Weights

## How does it work?
* run run_training.py
    * A queue is created which holds all combinations.
       * Each combination consists of a complete set of extraction and scoring parameters
    * Each combination is processed once for every sampling='training' document
    * Each combination is removed from the queue and added to the queue_processed once all documents have been processed using the particular combination

* copy the best weights from training_final_result_xxxx.json to run_test.py
    * the same functions as run_training are applied to the training set

* run evaluate to extract results. They are stored under /result/
  * evaluation_full.json contains the full not parsed result
  * evaluation_only_avg.json contains only the avg distance per document
  * final_result.json full result but parsed
  * final_result_xxxx.json full contains the weights which create the lowest distance for all tested documents


``` delete/rename the files in /queue_caches/ if you want to start over ```

## Installation
* pip install --upgrade ortools
  * https://developers.google.com/optimization/introduction/installing/binary
* python3 -m spacy download en
  * https://spacy.io/models/
* python -m spacy download en_core_web_lg
  * https://spacy.io/usage/vectors-similarity
