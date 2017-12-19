# Learn Weights

# How does it work?
* A queue is created which holds all combinations.
   * Each combination consists of a complete set of extraction and scoring parameters
* Each combination is processed once for every document
* Each combination is removed from the queue and added to the queue_processed once all documents have been processed using the particular combination
* Each result is cached for each combination change, therefore very long executing results are not lost if something went wrong.


* run evaluate to extract results. They are stored under /result/
  * evaluation_full.json contains the full not parsed result
  * evaluation_only_avg.json contains only the avg distance per document
  * final_result.json full result but parsed
  * final_result_xxx.json full contains the weights which create the lowest distance for all tested documents

* run validation to calculate the average distance per question for the first-n documents
    * results are stored at /result/ in VALIDATION.json and VALIDATION_AVG.json


``` delete/rename the files in /queue_caches/ if you want to start over ```