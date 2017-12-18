# Learn Weights

# How does it work?
* A queue is created which holds all combinations.
   * Each combination consists of a complete set of extraction and scoring parameters
* Each combination is processed once for every document
* Each combination is removed from the queue and added to the queue_processed once all documents have been processed using the particular combination
* Each result is cached for each combination change TODO: WHY?
* run evaluate to extract results TODO: WHICH RESULTS?

``` delete/rename the files in /queue_caches/ if you want to start over ```