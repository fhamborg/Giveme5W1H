import enum
import glob
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
    see research_helper

Used time horizon:
    2016-2017

Event Source
    https://www.infoplease.com/world/current-events/2016-current-events
    http://eventregistry.org/search?type=events&query=%257B%2522categories%2522:%255B%257B%2522id%2522:145,%2522uri%2522:%2522dmoz%2FSports%2522,%2522label%2522:%2522Sports%2522,%2522negate%2522:false%257D,%257B%2522id%2522:380,%2522uri%2522:%2522dmoz%2FSociety%2FPolitics%2522,%2522label%2522:%2522Society%25E2%2586%2592Politics%2522,%2522negate%2522:false%257D,%257B%2522id%2522:19,%2522uri%2522:%2522dmoz%2FBusiness%2522,%2522label%2522:%2522Business%2522,%2522negate%2522:false%257D,%257B%2522id%2522:41,%2522uri%2522:%2522dmoz%2FScience%2FTechnology%2522,%2522label%2522:%2522Science%25E2%2586%2592Technology%2522,%2522negate%2522:false%257D%255D,%2522dateStart%2522:%25222016-01-01%2522,%2522dateEnd%2522:%25222016-12-31%2522,%2522lang%2522:%2522eng%2522,%2522minArticles%2522:200,%2522preferredLang%2522:%2522eng%2522%257D&tab=items&eventsSortBy=rel
    http://googlenews.com
    https://www.nexis.com/
    https://en.wikipedia.org/wiki/Portal:Current_events/May_2016



"""

@enum.unique
class Category(Enum):
    global_politics = auto() # elections  # International relations # Armed conflicts and attacks
    economics = auto() # Business
    science_tech = auto() #  science
    entertainment = auto()
    sports = auto()

    # todo: add
    # disaster and accidents
    # World

@enum.unique
class Topic(Enum):
    unspecific = auto()
    north_korea = auto()
    hack = auto()

@enum.unique
class Event(Enum):


    #
    # politics
    #

    # misc
    las_vegas_shooting = auto()
    panama_papers = auto()  # global_politics, 3. April 2016, # Journalist Daphne Galizia
    boko_haram_21_schoolgirls_freed = auto()
    harambe = auto() # 28. Mai 2016
    truck_attack_in_nice = auto() # 14 July 2016
    NewYearsEveSexualAssaultsGermany = auto()

    # north_korea
    north_Korea_hokkaido_missile = auto()
    north_Korea_Launches_satellite = auto()

    hack_equifax_breach = auto()

    # Gold_standart events
    Benghazi_US_consulate_attack = auto() # 11. September 2012,
    croydon_tram_trash = auto()
    f1_crash = auto()
    cubs_win_championship = auto()
    china_boy_well = auto()
    # trump

    # erdogan
    #erdogan_attempted_Coup = auto()
    #erdogan_elected = auto()
    ##erdogan_bohmermann = auto()

    #zimbabwe_President_Mugabe_resigns = auto()
    #zimbabwe_Military_coup = auto()

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


def json_exist_has_content(path, filename):
    _path = path + '/' + filename + '.' + 'json'
    if os.path.exists(_path):
        if os.stat(_path).st_size != 0:
            return True
    return False


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


# http://www.dailymail.co.uk/wires/ap/article-4050308/Truck-rams-German-Christmas-market-killing-12-people.html

add_article(Category.sports, Topic.unspecific, Event.china_boy_well, [
    "http://www.bbc.com/news/world-asia-china-37906226",
    "http://www.bbc.com/news/world-asia-china-37946716",
    "http://www.dailymail.co.uk/news/article-3916560/Dramatic-footage-shows-rescuers-using-eighty-diggers-save-boy-fell-130ft-deep-picking-cabbages-Chinese-farm.html",
    "http://www.dailymail.co.uk/news/article-3923808/Mystery-Chinese-boy-fell-deep-massive-rescue-operation-involving-80-diggers-chute-empty.html"
])

add_article(Category.sports, Topic.unspecific, Event.cubs_win_championship, [
        "https://www.theguardian.com/sport/2016/nov/03/world-series-game-7-chicago-cubs-cleveland-indians-mlb",
        "https://www.washingtonpost.com/sports/believe-it-chicago-cubs-win-classic-game-7-to-win-first-world-series-since-1908/2016/11/03/99cfc9c2-a0b3-11e6-a44d-cc2898cfab06_story.html",
        "https://www.thesun.co.uk/sport/othersports/2106710/chicago-cubs-win-world-series-hillary-clinton-bill-murray-and-barack-obama-lead-celebrations-as-cubs-end-108-year-curse/",
        "http://nypost.com/2016/11/03/cubs-end-drought-in-chaotic-epic-world-series-finale/",
        "http://www.bbc.com/sport/baseball/37857919",
        "https://www.washingtonpost.com/sports/nationals/you-knew-it-couldnt-come-easy-but-the-cubs-are-world-series-champions/2016/11/03/a4487ade-a0b3-11e6-a44d-cc2898cfab06_story.html",
        "http://www.telegraph.co.uk/baseball/2016/11/03/chicago-cubs-break-108-year-curse-of-the-billy-goat-winning-worl/",
        "http://www.mirror.co.uk/sport/other-sports/american-sports/chicago-cubs-win-world-series-9185077",
        "http://www.standard.co.uk/sport/other-sports/chicago-cubs-win-world-series-to-end-108year-curse-and-earn-invite-from-barack-obama-a3386411.html",
        "http://www.independent.co.uk/sport/us-sport/major-league-baseball/world-series-chicago-cubs-cleveland-indians-108-year-title-drought-a7394706.html",
        "http://www.independent.co.uk/sport/us-sport/major-league-baseball/chicago-cubs-fans-celebrate-world-series-title-a7394736.html",
        "http://www.dailymail.co.uk/news/article-3899956/Chicago-Cubs-win-World-Series-epic-Game-7-showdown-Cleveland.html",
        "http://www.usatoday.com/story/sports/ftw/2016/11/03/sports-world-reacts-to-the-chicago-cubs-winning-their-first-world-series-since-1908/93225730/"
])

add_article(Category.sports, Topic.unspecific, Event.f1_crash, [
 "http://www.dailymail.co.uk/sport/formulaone/article-3932890/Max-Verstappen-amazes-Red-Bull-principal-Christian-Horner-performance-Brazil-witnessed-special.html",
        "https://www.thesun.co.uk/sport/2177804/felipe-massa-retires-f1-legend-makes-a-very-emotional-farewell-after-crashing-in-his-last-home-race-in-brazil/",
        "http://www.dailymail.co.uk/sport/sportsnews/article-3934424/Formula-One-star-Max-Verstappen-shows-nerves-steel-avoid-accident.html",
        "http://www.mirror.co.uk/sport/formula-1/red-bull-boss-christian-horner-9254708",
        "http://www.dailymail.co.uk/sport/formulaone/article-3932386/F1-legend-Felipe-Massa-makes-emotional-farewell-crashing-Brazil-Grand-Prix-Interlagos.html",
        "https://www.thesun.co.uk/sport/2177105/lewis-hamilton-wins-the-brazilian-grand-prix-after-two-red-flags/",
        "http://www.standard.co.uk/sport/brazilian-grand-prix-redflagged-after-dramatic-kimi-raikkonen-crash-a3394411.html",
        "http://www.telegraph.co.uk/formula-1/2016/11/13/max-verstappen-even-stuns-his-dad-by-storming-home-into-third-pl/",
        "http://www.usatoday.com/story/sports/motor/formula1/2016/11/13/brazils-massa-crashes-but-gets-warm-farewell-at-home-gp/93771246/",
        "http://www.dailymail.co.uk/sport/formulaone/article-3932252/Brazilian-Grand-Prix-thrown-chaos-Kimi-Raikkonen-accident-brings-red-flag-Sebastian-Vettel-fumes-stupid-conditions-mad.html",
        "http://www.express.co.uk/sport/f1-autosport/731858/Max-Verstappen-avoids-crash-Kimi-Raikkonen-Brazilian-Grand-Prix-wet",
        "http://www.mirror.co.uk/sport/formula-1/brazilian-f1-grand-prix-riddled-9253267"
])


add_article(Category.global_politics, Topic.unspecific, Event.croydon_tram_trash, [
        "http://www.standard.co.uk/news/transport/croydon-tram-derailment-people-trapped-after-tram-overturns-in-at-sandilands-a3390796.html",
        "http://www.nytimes.com/2016/11/10/world/europe/tram-derails-croydon-london.html",
        "http://www.dailymail.co.uk/wires/pa/article-3919284/Five-trapped-40-injured-tram-overturns-tunnel.html",
        "https://www.theguardian.com/uk-news/2016/nov/09/croydon-tram-crash-kills-at-least-seven-and-injures-more-than-50",
        "http://www.mirror.co.uk/news/uk-news/huge-rescue-operation-sandilands-station-9226276",
        "http://www.telegraph.co.uk/news/2016/11/10/croydon-tram-crash-police-check-drivers-mobile-phone-records/",
        "http://www.express.co.uk/news/uk/730639/Croydon-tram-crash-carnage-survivor-derailment-seven-dead",
        "http://www.usatoday.com/story/news/2016/11/09/least-7-killed-tram-accident-south-london/93549248/",
        "http://www.bbc.com/news/uk-england-london-37919658",
        "http://nypost.com/2016/11/09/several-dead-and-dozens-injured-after-tram-overturns-in-london/",
        "http://www.independent.co.uk/news/uk/home-news/five-trapped-40-injured-after-tram-overturns-south-london-croydon-a7406496.html"
])

add_article(Category.global_politics, Topic.unspecific, Event.Benghazi_US_consulate_attack,[
    "http://www.telegraph.co.uk/news/2016/11/10/taliban-attack-german-consulate-in-northern-afghan-city-of-mazar/",
    "http://www.express.co.uk/news/world/731052/German-consulate-explosion-gunfire-Afghanistan",
    "https://www.theguardian.com/world/2016/nov/10/taliban-attack-german-consulate-mazar-i-sharif-afghanistan-nato-airstrikes-kunduz",
    "http://www.bbc.com/news/world-asia-37944115",
    "http://www.nytimes.com/2016/11/11/world/asia/taliban-strike-german-consulate-in-afghan-city-of-mazar-i-sharif.html?_r=0",
    "http://www.independent.co.uk/news/world/middle-east/german-consulate-afghanistan-attacked-bomb-suicide-taliban-revenge-mazar-i-sharif-kunduz-attack-two-a7410746.html",
    "https://www.thesun.co.uk/news/2162467/taliban-suicide-bomber-truck-german-consulate-afghanistan-killing-two/amp/",
    "http://www.nytimes.com/2016/11/11/world/asia/taliban-strike-german-consulate-in-afghan-city-of-mazar-i-sharif.html?_r=0",
    "http://www.bbc.com/news/world-asia-37944115"
])


add_article(Category.global_politics, Topic.north_korea, Event.north_Korea_Launches_satellite, [
  'http://edition.cnn.com/2016/02/07/asia/gallery/north-korea-missile-launch/index.html',
    'http://www.nytimes.com/2013/01/31/world/asia/on-3d-try-south-korea-launches-satellite-into-orbit.html',
    'https://www.npr.org/2015/09/15/440443821/north-korea-says-its-ready-to-launch-satellites-aboard-rockets',
    'http://www.dailymail.co.uk/wires/afp/article-4322652/Japan-launches-latest-North-Korea-spy-satellite.html',
    'http://www.thehindu.com/news/international/north-korea-to-launch-satellites-to-mark-party-anniversary/article7654457.ece',
    'http://www.chinadaily.com.cn/world/2016-02/07/content_23426008.htm',
    'https://www.washingtonpost.com/world/north-korea-launches-satellite-sparks-fears-about-long-range-missile-program/2016/02/06/0b6084e5-afd1-42ec-8170-280883f23240_story.html'
])


add_article(Category.global_politics, Topic.unspecific, Event.NewYearsEveSexualAssaultsGermany, [
   'http://www.chinadaily.com.cn/opinion/2016-01/11/content_23017934.htm',
    'http://www.dailymail.co.uk/news/article-3411720/A-staggering-359-sexual-assaults-migrants-reported-Cologne-police-New-Year-s-Eve-mob-went-rampage-causing-821-complaints.html',
    'https://www.npr.org/2016/01/06/462114345/migrants-in-germany-accused-of-coordinated-sexual-assaults',
    'https://www.npr.org/sections/parallels/2016/01/05/462059765/mass-sexual-assaults-in-cologne-germany-renew-tensions-over-migrants'
])

add_article(Category.global_politics, Topic.unspecific, Event.truck_attack_in_nice, [
    'http://edition.cnn.com/2016/07/14/europe/nice-france-truck/index.html',
    'http://edition.cnn.com/2016/07/14/world/nice-attack-witness-accounts/index.html',
    'https://www.nytimes.com/2016/07/16/world/europe/truck-attack-nice-france.html',
    'https://www.nytimes.com/2016/07/15/world/europe/nice-france-truck-bastille-day.html',
    'https://www.npr.org/2016/07/14/486097589/more-than-70-people-killed-in-truck-attack-in-nice-france',
    'https://www.npr.org/2016/07/14/486095754/president-obama-briefed-on-truck-attack-in-nice-france',
    'https://www.thesun.co.uk/news/1447619/at-least-77-dead-and-100-injured-as-lorry-crashes-into-crowd-of-revellers-celebrating-in-france-terror-attack/',
    'http://www.dailymail.co.uk/wires/afp/article-3692450/Tunisians-Algerians-dead-Nice-attack.html',
    'http://www.thehindu.com/news/84-killed-in-France-as-terror-truck-ploughs-through-crowd/article14491015.ece',
    'http://www.thehindu.com/news/international/Truck-attacker-in-Nice-kills-84-celebrating-Bastille-Day/article14490871.ece',
    'http://www.chinadaily.com.cn/world/2016-08/05/content_26355611.htm',
    'http://europe.chinadaily.com.cn/world/2016-07/15/content_26095924.htm',
    'http://usa.chinadaily.com.cn/epaper/2016-07/15/content_26104748.htm'
])


add_article(Category.global_politics, Topic.unspecific, Event.harambe, [
    'http://edition.cnn.com/2016/03/18/health/seaworld-blackfish-effect-circuses-zoos/index.html',
    'https://www.npr.org/sections/thetwo-way/2016/05/29/479919582/gorilla-killed-to-save-boy-at-cincinnati-zoo',
    'https://www.thesun.co.uk/news/1230550/hear-the-dramatic-moment-little-isiahs-mum-calls-for-help-after-her-son-falls-into-gorilla-enclosure-at-zoo/',
    'http://www.dailymail.co.uk/news/article-3614480/Small-child-falls-gorilla-enclosure-zoo.html',
    'http://www.thehindu.com/news/international/Ohio-zoo-kills-gorilla-to-protect-small-child-in-enclosure/article14347705.ece',
    'http://usa.chinadaily.com.cn/world/2016-05/30/content_25527063.htm',
    'https://www.washingtonpost.com/news/post-nation/wp/2016/05/29/it-could-have-been-very-bad-gorilla-killed-after-boy-falls-into-cincinnati-zoo-exhibit/?tid=a_inl',
    'https://www.rt.com/news/344746-cincinnati-zoo-gorilla-killed/'
])

add_article(Category.global_politics, Topic.unspecific, Event.boko_haram_21_schoolgirls_freed, [
  'http://edition.cnn.com/2016/10/13/africa/nigeria-chibok-girls-released/index.html',
    'https://www.nytimes.com/2016/10/14/world/africa/boko-haram-nigeria.html',
    'https://www.npr.org/sections/thetwo-way/2016/10/13/497803083/nigeria-says-21-schoolgirls-abducted-by-boko-haram-have-been-released',
    'https://www.thesun.co.uk/news/1971191/isis-splinter-group-boko-haram-release-21-kidnapped-nigerian-schoolgirls-in-exchange-for-four-jailed-militants/',
    'http://www.dailymail.co.uk/wires/afp/article-3836078/Boko-Haram-releases-21-Chibok-girls-Nigerian-official.html',
    'http://www.thehindu.com/news/international/21-abducted-Chibok-schoolgirls-freed/article15513701.ece',
    'http://www.thehindu.com/news/international/21-abducted-Chibok-schoolgirls-freed-in-Nigeria/article16070198.ece',
    'http://africa.chinadaily.com.cn/world/2017-05/09/content_29261603.htm',
    'https://www.washingtonpost.com/world/boko-haram-militants-free-21-captive-chibok-schoolgirls-amid-talks-with-nigeria/2016/10/13/9e94610a-0ed3-4a26-96f1-6c5d7cccfdcd_story.html'
])


add_article(Category.global_politics, Topic.hack, Event.panama_papers, [
    'http://edition.cnn.com/2016/04/04/opinions/panama-papers-ghitis/index.html',
    'http://edition.cnn.com/2016/04/04/world/panama-papers-explainer/index.html',
    'https://www.nytimes.com/2017/11/06/world/bank-of-utah-leonid-mikhelson.html',
    'https://www.npr.org/sections/thetwo-way/2016/04/04/472985787/heres-what-you-need-to-know-so-far-about-panama-papers',
    'https://www.npr.org/sections/parallels/2016/05/04/476745041/panama-rises-despite-dents-to-its-reputation-from-papers-leaks',
    'http://www.dailymail.co.uk/wires/afp/article-3523948/Big-China-presence-Panama-Papers-law-firm.html',
    'http://www.dailymail.co.uk/wires/afp/article-3522970/African-leaders-relatives-named-Panama-Papers.html',
    'http://www.dailymail.co.uk/wires/afp/article-3523775/Panama-Papers-revelations-trigger-global-probes.html',
    'https://www.rt.com/news/338270-panama-papers-corruption-report/',
    'https://www.rt.com/op-edge/338388-putin-western-media-leaks/',
    'http://www.chinadaily.com.cn/cndy/2016-04/05/content_24280080.htm',
    'https://www.washingtonpost.com/opinions/where-have-russias-billions-gone/2016/04/04/44ebd46a-fa9a-11e5-80e4-c381214de1a3_story.html',
    'https://www.washingtonpost.com/world/the_americas/where-the-papers-got-their-name/2016/04/09/f088582e-fcf8-11e5-813a-90ab563f0dde_story.html',
    'https://www.washingtonpost.com/world/as-panama-leaks-spread-chinas-red-nobility-would-rather-not-talk-about-it/2016/04/07/ab5ab28e-fc4d-11e5-813a-90ab563f0dde_story.html'
])


#
# raw data set
# add_article(Category.science_tech, Topic.hack, Event.hack_equifax_breach,  [])
add_article(Category.science_tech, Topic.hack, Event.hack_equifax_breach,  [
    "https://www.wsj.com/articles/equifax-earnings-drop-27-in-quarter-marred-by-cyberattack-1510268187",
    "https://www.bloomberg.com/news/articles/2017-11-14/how-much-will-equifax-pay",
    "https://gizmodo.com/equifax-seized-138-scammy-lookalike-domains-instead-of-1820450580",
    'https://www.nytimes.com/2017/09/27/your-money/equifax-credit-freeze-lock-apology.html',
    'https://www.nytimes.com/2017/10/02/business/equifax-breach.html',
    'https://www.npr.org/sections/thetwo-way/2017/09/19/552124551/equifax-confirms-another-security-incident',
    'https://www.thesun.co.uk/news/4425740/cyber-attack-equifax-data-stolen-brits/',
    'https://www.thesun.co.uk/tech/4475843/equifax-admits-that-400000-british-peoples-private-info-was-accessed-during-major-cybersecurity-incident/',
    'https://www.thesun.co.uk/news/4657635/credit-company-equifax-says-new-security-attack-means-that-almost-700000-brits-have-had-personal-details-stolen-by-cyber-hackers/',
    'http://www.dailymail.co.uk/news/article-4942344/Equifax-2-5-million-Americans-affected-hack.html',
    'http://www.dailymail.co.uk/news/article-4863648/Credit-agency-Equifax-info-143-million-stolen.html',
    'https://www.rt.com/shows/boom-bust/402559-hurricane-harvey-irma-damage/'
])


add_article(Category.global_politics, Topic.unspecific, Event.las_vegas_shooting, [
    'http://edition.cnn.com/videos/us/2017/10/02/vegas-witness-crowd-running.cnn',
    'http://edition.cnn.com/2017/10/02/us/gallery/las-vegas-shooting/index.html',
    'http://edition.cnn.com/videos/tv/2017/10/02/exp-tsr-elam-las-vegas-concert-mass-shooting.cnn',
    'http://edition.cnn.com/videos/us/2017/10/02/donald-trump-entire-las-vegas-shooting-address-sot.cnn',
    'https://www.nytimes.com/2017/10/02/us/stephen-paddock-vegas-shooter.html',
    'https://www.nytimes.com/interactive/2017/10/02/us/mandalay-bay-vegas-shooting.html',
    'https://www.rt.com/usa/405321-las-vegas-shooting-panic/',
    'https://www.rt.com/shows/news-with-ed-schultz/405483-news-with-ed-october2/',
    'https://www.rt.com/usa/405409-isis-responsibility-vegas-shooting/',
    'http://www.thehindu.com/news/international/las-vegas-shooting-deadliest-in-us-several-killed-injured/article19787232.ece',
    'http://www.thehindu.com/news/international/live-updates-las-vegas-strip-shooting/article19784319.ece',
    'http://usa.chinadaily.com.cn/world/2017-10/03/content_32789696.htm',
    'http://www.chinadaily.com.cn/cndy/2017-10/03/content_32789038.htm',
    'http://usa.chinadaily.com.cn/world/2017-10/03/content_32788252.htm'

])

# TODO i think not all of them refer to the same missile/event...
add_article(Category.global_politics, Topic.north_korea, Event.north_Korea_hokkaido_missile, [
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


if __name__ == '__main__':
    # crawling itself
    for index, info_article in enumerate(articles):
        url = info_article['Url']
        dId = hashlib.sha224(url.encode('utf-8')).hexdigest()

        if not json_exist_has_content('data_raw', dId):
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
                if article_dict.get('date_download'):
                    article_dict['date_download'] = article_dict['date_download'].isoformat()

                write_json('data_raw', article_dict['dId'], article_dict)
                print(url)
            except Exception as e:
                print(e)
                print(url)
        else:
            print('skipped, newsCluster updated')
            with open('data_raw' + '/' + dId + '.' + 'json', encoding='utf-8') as data_file:
                data = json.load(data_file)
                data['newsCluster'] = info_article
            with open('data_raw' + '/' + dId + '.' + 'json', encoding='utf-8', mode='w') as data_file:
                data_file.write(json.dumps(data, sort_keys=False, indent=2))



    # preprocess into data
    # TODO cleanup directories before writing
    for filepath in glob.glob('data_raw/*.json'):
        with open(filepath, encoding='utf-8') as data_file:
            try:
                data = json.load(data_file)
                target = None

                # giveme5w(and enhancer) needs at least these 3 fields to work proper
                if data.get('date_publish') is not None and data.get('title') is not None and data.get('text') is not None:
                    target = 'data'
                else:
                    target = 'data_damaged'

                outfile = open(target + '/' + data['dId'] + '.json', 'w')
                outfile.write(json.dumps(data, sort_keys=False, indent=2))
                outfile.close()
            except json.decoder.JSONDecodeError:
                print('skipped:' + filepath)
