import urllib
import webbrowser
import urllib.parse
''' 
 This tool will open all relevant publisher sites with the given keyword and well defined search parameter
 - inspect all pages an pick 1-2 relevant news per event 
 - they should annotated the same event at the same days 
'''

# Set your search term here.
search_term = 'Benghazi US consulate attack'
search_term_plus = search_term.replace(' ', '+')
search_term_encoded = urllib.parse.quote(search_term)
urls = [
    #'https://www.huffingtonpost.com/search?sortBy=recency&sortOrder=desc&keywords=' + search_term_plus,
    'http://edition.cnn.com/search/?sort=relevance&size=100&type=article&q=' + search_term_plus,
    'https://query.nytimes.com/search/sitesearch/#/'+ search_term_plus +'/',
    'https://www.npr.org/templates/search/index.php?searchinput=' + search_term_plus,
    'https://www.thesun.co.uk/?s=' + search_term_plus, # no serach for relevante or date
    'http://www.dailymail.co.uk/home/search.html?offset=0&size=50&sel=site&sort=relevant&type=article&days=all&searchPhrase=' + search_term_plus,
    'https://www.rt.com/search?q=' + search_term_plus,
    'http://www.thehindu.com/search/?order=DESC&ct=text&sort=score&q='+ search_term_plus, # search for date but no date in results
    'http://searchen.chinadaily.com.cn/search?query='+ search_term_plus,
    'http://www.spiegel.de/international/search/index.html?suchbegriff='+ search_term_plus,
    'https://www.washingtonpost.com/newssearch/?sort=Relevance&datefilter=All%20Since%202005&contenttype=Article&query='+ search_term_encoded
]

for url in urls:
    webbrowser.open(url)