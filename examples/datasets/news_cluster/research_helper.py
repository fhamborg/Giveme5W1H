import webbrowser

''' 
 This tool will open all relevant publisher sites with the given keyword
'''

# Set your search term here.
search_term = 'test'

search_term_plus = search_term.replace(' ', '+')
urls = [
    'https://www.huffingtonpost.com/search?sortBy=recency&sortOrder=desc&keywords=' + search_term_plus,
    'http://edition.cnn.com/search/?q=' + search_term_plus,
    'https://query.nytimes.com/search/sitesearch/#/'+ search_term_plus +'/',
    'https://www.npr.org/templates/search/index.php?searchinput=' + search_term_plus,
    'https://www.thesun.co.uk/?s=' + search_term_plus,
    'http://www.dailymail.co.uk/home/search.html?offset=0&size=50&sel=site&sort=relevant&type=article&days=all&searchPhrase=' + search_term_plus,
    'https://www.rt.com/search?q=' + search_term_plus,
    'http://www.thehindu.com/search/?order=DESC&sort=score&q='+ search_term_plus,
    'http://searchen.chinadaily.com.cn/search?query='+ search_term_plus,
    'http://www.spiegel.de/international/search/index.html?suchbegriff='+ search_term_plus
]

for url in urls:
    webbrowser.open(url)