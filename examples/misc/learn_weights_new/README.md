# Learn Weights

# How dose it work?
* A queue is created which holds all combinations.
   * Each combination has scoring extracting and scoring parameters
* Each combinations is processed once for every document
* Each combinations is removed from the queue and added to the queue_processed once all document have been processed
* Each result is cached for each combination change
* run evaluate to extract results

``` delete/rename the files in /cache/ if you want to start over ```