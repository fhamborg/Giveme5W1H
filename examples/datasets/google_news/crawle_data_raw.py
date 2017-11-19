import hashlib
import json
import os.path

from newsplease import NewsPlease

"""
This is a dataset aiming to represent clsuterred news around topics.
"""


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


# There are the articels by news, sorted by their cluster/topic
urls = {
    'North Korea Missile': [
        'https://www.usatoday.com/story/news/world/2017/11/16/two-months-without-north-korean-missile-test-record-year-cause-hope/867564001/',
        'http://abcnews.go.com/International/repeated-tests-north-korea-launched-missile-56-days/story?id=51024512',
        'https://www.reuters.com/article/us-northkorea-missiles-southkorea-usa/u-s-envoy-says-no-communication-no-signal-from-north-korea-amid-nuclear-crisis-idUSKBN1DH0F7?il=0',
        'http://nationalinterest.org/blog/the-buzz/the-strange-reason-north-koreas-mighty-missile-forces-are-23208',
        'http://www.newsweek.com/us-north-korea-nuclear-defend-alaska-705124',
        'http://www.newsweek.com/north-korea-war-tests-talks-japan-710823',
        'https://www.reuters.com/article/us-trump-asia-japan/trump-says-japan-would-shoot-north-korean-missiles-out-of-sky-if-it-bought-u-s-weaponry-idUSKBN1D602F',
        'https://www.japantimes.co.jp/news/2017/11/14/asia-pacific/north-koreas-winter-training-means-fewer-missile-launches/'
    ],
    'Star Wars: Battlefront II - Loot Box': {
        'https://www.cnet.com/news/star-wars-battlefront-ii-reddit-micro-transactions/',
        'https://techcrunch.com/2017/11/16/hours-before-launch-ea-strips-micro-transactions-from-star-wars-battlefront-ii/',
        'http://comicbook.com/gaming/2017/11/17/star-wars-battlefront-ii-no-more-microtransactions-turned-off-electronic-arts/',
        'https://www.gamespot.com/articles/ea-respond-to-star-wars-loot-box-gambling-investig/1100-6455034/',
        'https://www.forbes.com/sites/insertcoin/2017/11/16/heres-the-emergency-heart-transplant-that-would-save-star-wars-battlefront-2',
        'https://arstechnica.com/gaming/2017/11/star-wars-battlefront-ii-review-nope-nope-nope-nope-nope-nope-nope/'
    },
    'IPhone-X Green-Line': [
        'http://www.thejakartapost.com/life/2017/11/13/is-samsung-display-to-blame-for-iphone-xs-screen-defect.html',
        'https://betanews.com/2017/11/12/iphone-x-green-line-cold-problems/',
        'http://www.techradar.com/news/the-latest-iphone-x-problem-is-a-bright-green-line-on-the-side-of-the-display',
        'https://www.thesun.co.uk/tech/4901708/iphone-x-owners-report-seeing-green-line-of-death-on-devices-display/',
        'https://www.engadget.com/2017/11/10/iphone-x-green-line-glitch/',
        'https://gadgets.ndtv.com/mobiles/news/iphone-x-oled-display-green-line-hardware-defect-1774664'],
    'Vegas Shooting': [
        'http://www.ktnv.com/news/national/california-shooting-gunman-was-paranoid-police-say',
        'https://www.reviewjournal.com/crime/shootings/las-vegas-police-identify-man-shot-killed-by-officer/',
        'http://www.foxnews.com/us/2017/11/16/ohio-man-threatened-to-kill-wife-carry-out-historic-mass-shooting-at-las-vegas-hotel-fbi-says.html'],
    'Dieselgate': [
        'http://www.thehindubusinessline.com/news/world/eu-car-sales-rev-up-despite-brexit-and-dieselgate/article9963851.ece',
        'http://www.telegraph.co.uk/business/2017/10/27/dieselgate-costs-continue-drag-volkswagen/',
        'https://www.reuters.com/article/us-volkswagen-emissions-britain/volkswagen-has-still-not-fixed-one-in-three-dieselgate-cars-in-britain-idUSKBN1D829C',
        'https://www.motoring.com.au/no-reason-for-dieselgate-class-action-says-vw-109733/',
        'https://www.torquenews.com/3769/dieselgate-seems-be-scandal-keeps-giving-new-vw-probe-possible',
        'http://www.wheels24.co.za/News/Industry_News/eu-raids-automaker-bmw-in-post-dieselgate-cartel-case-20171024',
        'http://www.spiegel.de/international/business/the-three-students-who-discovered-dieselgate-a-1173686.html'
    ],
    'Zimbabwe': [
        "http://www.cbc.ca/news/world/zimbabwe-mugabe-1.4404727",
        "https://www.timeslive.co.za/news/africa/2017-11-17-zimbabwe-human-rights-lawyer-nothing-is-going-to-change/",
        "http://www.bbc.com/news/world-africa-42016464"],
    'Equifax breach':
        ["https://www.wsj.com/articles/equifax-earnings-drop-27-in-quarter-marred-by-cyberattack-1510268187",
         "https://www.bloomberg.com/news/articles/2017-11-14/how-much-will-equifax-pay",
         "https://gizmodo.com/equifax-seized-138-scammy-lookalike-domains-instead-of-1820450580"]

}

for index, topic in enumerate(urls):
    for url in urls[topic]:

        dId = hashlib.sha224(url.encode('utf-8')).hexdigest()

        if not json_exist('data_raw', dId):
            # this is an object
            try:
                article = NewsPlease.from_url(url)

                # this is an dict
                article_dict = article.get_dict()

                # cluster with label and id
                article_dict['category_id'] = index
                article_dict['category'] = topic

                # enhancement for giveme5w
                article_dict['dId'] = dId

                # datetime-datetime-not-json-serializable bugfix"
                article_dict['date_publish'] = article_dict['date_publish'].isoformat()

                write_json('data_raw', article_dict['dId'], article_dict)
            except:
                print(url)
                print('something went wrong')
                # else:
                #    print('already crawled')
