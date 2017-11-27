import enum
from enum import Enum, auto
import hashlib
import json
import os.path
from enum import Enum
from typing import List

from newsplease import NewsPlease

"""
This is a dataset aiming to represent clustered news around topics.


Used publisher:

    Huffington
        https://www.huffingtonpost.com/search?keywords=test+test&sortBy=recency&sortOrder=desc
    CNN	
        http://edition.cnn.com/search/?q=test
    New York Times	
        https://query.nytimes.com/search/sitesearch/#/test+test/
    NPR	
        https://www.npr.org/templates/search/index.php?searchinput=test+test
    The Sun	
        https://www.thesun.co.uk/?s=test
    Daily Mail	
       http://www.dailymail.co.uk/home/search.html?offset=0&size=50&sel=site&searchPhrase=test+test&sort=relevant&type=article&days=all
    RT	
        https://www.rt.com/search?q=test+test
    The Hindu	
        http://www.thehindu.com/search/?order=DESC&q=hokkaido+missile&sort=score
    China Daily	
        http://searchen.chinadaily.com.cn/search?query=hokkaido+missile
    Spiegel	
        http://www.spiegel.de/international/search/index.html?suchbegriff=test+test

Used time horizon:
    2016-2017

Event Source
    https://www.infoplease.com/world/current-events/2016-current-events
    http://eventregistry.org/search?type=events&query=%257B%2522categories%2522:%255B%257B%2522id%2522:145,%2522uri%2522:%2522dmoz%2FSports%2522,%2522label%2522:%2522Sports%2522,%2522negate%2522:false%257D,%257B%2522id%2522:380,%2522uri%2522:%2522dmoz%2FSociety%2FPolitics%2522,%2522label%2522:%2522Society%25E2%2586%2592Politics%2522,%2522negate%2522:false%257D,%257B%2522id%2522:19,%2522uri%2522:%2522dmoz%2FBusiness%2522,%2522label%2522:%2522Business%2522,%2522negate%2522:false%257D,%257B%2522id%2522:41,%2522uri%2522:%2522dmoz%2FScience%2FTechnology%2522,%2522label%2522:%2522Science%25E2%2586%2592Technology%2522,%2522negate%2522:false%257D%255D,%2522dateStart%2522:%25222016-01-01%2522,%2522dateEnd%2522:%25222016-12-31%2522,%2522lang%2522:%2522eng%2522,%2522minArticles%2522:200,%2522preferredLang%2522:%2522eng%2522%257D&tab=items&eventsSortBy=rel
    http://googlenews.com
    https://www.nexis.com/



"""



@enum.unique
class Category(Enum):
    global_politics = auto()
    economics = auto()
    science_tech = auto()
    entertainment = auto()
    sports = auto()

    # todo: add
    # disaster
@enum.unique
class Topic(Enum):
    unspecific = auto()
    north_korea = auto()
@enum.unique
class Event(Enum):


    #
    # politics
    #

    # misc
    las_vegas_shooting = auto()
    panama_papers = auto()  # global_politics
    boko_haram_21_schoolgirls = auto()
    harambe = auto()
    truck_attack_in_nice = auto()
    NewYearsEveSexualAssaultsGermany = auto()

    # north_korea
    north_Korea_hokkaido_missile = auto()
    north_Korea_Launches_satellite = auto()
    north_Korea_Reacts_Sanctions = auto()

    # trump

    # erdogan
    erdogan_attempted_Coup = auto()
    erdogan_elected = auto()
    erdogan_bohmermann = auto()

    zimbabwe_President_Mugabe_resigns = auto()
    zimbabwe_Military_coup = auto()




    #
    # Tech
    #
    # explosive_samsung_galaxy_note = auto() not happening at a specie time
    # dieselgate = auto()  # tech ? not happening at a specie time
    # star_wars_battlefront_lootbox = auto()  not happening at a specie time

    # Hacks:
    # Equifax_breach = auto() not happening at a specie time
    # Linkedin hack
    # Dropbox hack


    #
    # Entertainment
    # Gamescom?
    # Box_office Batman v Superman: Dawn of Justice
    # Box_office_Suicide Squad
    # Apple keynote
    # Apple headphone jack
    # google keynote

    #
    # Sport
    #

    # SuperBowl


    #
    # Disaster
    #

    # Italy Earthquakes





def write_json(path, filename, object):
    """
    writes an object to a path as json
    :param path:
    :param object:
    :return:
    """
    with open(path + '/' + filename + '.' + 'json', 'w') as data_file:
        data_file.write(json.dumps(object, sort_keys=False, indent=2))
        data_file.close()

def json_exist(path, filename):
    return os.path.exists(path + '/' + filename + '.' + 'json')


articles = []
def add_article(a_category: Category, a_topic: Topic, a_Event: Event, urls: List[str]):
    for ulr in urls:
        articles.append(
            {
                'CategoryId': a_category.value,
                'Category': a_category.name,
                'TopicId':  a_topic.value,
                'Topic': a_topic.name,
                'EventId': a_Event.value,
                'Event': a_Event.name,
                'Url': ulr
            }
        )


#
# raw data set
#

# TODO not all of them refer to the same missile...
add_article(Category.economics, Topic.north_korea, Event.north_Korea_hokkaido_missile, [
    'https://www.huffingtonpost.com/entry/un-condemns-north-korea-missile-test_us_59a681e0e4b00795c2a2ba10',
    'https://www.huffingtonpost.com/entry/north-korea-missile-guam_us_59a5ff61e4b084581a14339c',
    'https://www.huffingtonpost.com/entry/north-korea-missile-japan_us_59a4874fe4b050afa90c1eab',
    'http://edition.cnn.com/2017/09/15/asia/japan-north-korea-missile-reaction/index.html',
    'http://edition.cnn.com/2017/09/14/asia/north-korea-missile-launch/index.html',
    'https://www.nytimes.com/2016/09/06/world/asia/north-korea-japan-missile-test.html',
    'https://www.nytimes.com/2017/07/29/world/asia/us-south-korea-north-korea-missile-test.html',
    'https://www.nytimes.com/2017/08/28/world/asia/north-korea-missile.html',
    'https://www.npr.org/sections/thetwo-way/2017/09/14/551095592/north-korea-fires-another-missile-over-japan',
    'https://www.npr.org/sections/thetwo-way/2017/08/28/546888551/north-korea-launches-another-missile-this-one-over-japan',
    'https://www.thesun.co.uk/news/4469623/north-korea-missile-launch-pyonyang-japan-guam-latest/',
    'https://www.thesun.co.uk/news/4348423/north-korea-missile-launch-japan-latest-russia-evacauation-kim-jong-un/',
    'http://www.dailymail.co.uk/news/article-5053125/Trump-samurai-Japan-shot-North-Korean-missiles.html',
    'http://www.dailymail.co.uk/wires/reuters/article-4995834/Nowhere-hide--N-Korean-missiles-spur-anxiety-Japan-fishing-town.html',
    'https://www.rt.com/usa/403383-mattis-korea-missile-japan-cover/',
    'https://www.rt.com/news/403380-north-korea-pyongyang-missile/',
    'http://www.thehindu.com/news/international/north-korea-fires-missile-over-japan-in-aggressive-test/article19577734.ece',
    'http://www.thehindu.com/todays-paper/tp-international/n-korea-fires-missile-over-japan/article19695124.ece',
    'http://www.thehindu.com/news/international/north-korea-fires-missile-over-japan-on-tuesday/article19585240.ece',
    'http://europe.chinadaily.com.cn/world/2017-09/15/content_32047139.htm',
    'http://africa.chinadaily.com.cn/world/2017-09/15/content_32041310.htm',
    'http://www.chinadaily.com.cn/world/2017-09/15/content_32021877.htm'

])

for index, info_article in enumerate(articles):

    url = info_article['Url']
    dId = hashlib.sha224(url.encode('utf-8')).hexdigest()

    if not json_exist('data_raw', dId):
        # this is an object
        try:
            article = NewsPlease.from_url(url)

            # this is an dict
            article_dict = article.get_dict()

            article_dict['newsCluster'] = info_article

            # enhancement for giveme5w
            article_dict['dId'] = dId

            # datetime-datetime-not-json-serializable bugfix"
            if article_dict.get('date_publish'):
                article_dict['date_publish'] = article_dict['date_publish'].isoformat()

            write_json('data_raw', article_dict['dId'], article_dict)
            print(url)
        except Exception as e:
            print(e)
            print(url)
    else:
        print(url)
        print('skipped, already crawled')


