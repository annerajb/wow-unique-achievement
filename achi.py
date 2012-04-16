#!/usr/bin/env python
import json
import urllib2
import itertools
from pprint import pprint
import md5, os, tempfile, time
class DiskCacheFetcher:
    def __init__(self, cache_dir=None):
        # If no cache directory specified, use system temp directory
        if cache_dir is None:
            cache_dir = tempfile.gettempdir()
        self.cache_dir = cache_dir
    def fetch(self, url, max_age=0):
        filename = md5.new(url).hexdigest()
        filepath = os.path.join(self.cache_dir, filename)
        if os.path.exists(filepath):
            if int(time.time()) - os.path.getmtime(filepath) < max_age:
                return open(filepath).read()
        print url
        # Retrieve over HTTP and cache, using rename to avoid collisions
        data = urllib2.urlopen(url).read()
        
	print data
	fd, temppath = tempfile.mkstemp()
        fp = os.fdopen(fd, 'w')
        fp.write(data)
        fp.close()
        os.rename(temppath, filepath)
        return data
        
        
base_url = 'http://us.battle.net/api/wow/character/'
characters = [
                ['kirin%20tor','annerajb'],
                ['sen\'jin','annerajb'],
                ['sen\'jin','annerajbdk'],
                ['sen\'jin','annerajbpaly'],
                ['sen\'jin','annerajbd'],
                ['sen\'jin','annerajbbank']
            ]
earned = []
achi_duplicates = [
    [1175,230],
    [706,707],
    [224,1151],
    [873,220],
    [708,709],
    [225,1164],
    [1168,1167],
    [710,711],
    [1169,1170],
    [2017,2016],
    [203,1251],
    [1502,202],
    [1172,1173],
    [1762,2192],
    [2194,2195],
    [762,2199],
    [1737,2476],
    [1752,2276],
    [3851,4177],
    [3857,3957],
    [5213,5213],
    [5226,5227],
    [5219,5220],
    [5221,5222],
    [5552,5231],
    [5718,5719],
    [5418,5417],
    [5415,5488],
    [5490,5489],
    [5223,5259],
    [3848,3849],
    [3856,4256],
    [3846,4176],
    [1757,2200],
    [873,20],
    [908,909],
    [714,907],
    [3778,4296],
    [4297,4298],
    [1783,1782],
    [5474,5475],
    [5841,5844],
    [5842,5843],
    [1563,1784],
    [5846,5845],
    [5848,5849],
    [5850,5847],
    [5477,5476],
    [5851,5852],
    [762,948],
    [943,942],
    [763,764],
    [1011,1012],
    [4885,4886],
    [5376,5375],
    [610,615],
    [614,619],
    [611,617],
    [613,618],
    [616,612],
    [901,899],
    [701,700],
    [603,604],
    [388,1006],
    [5268,5269],
    [5322,5323],
    [5327,5324],
    [5328,5325],
    [5823,5824],
    [5329,5326],
    [5330,5345],
    [5331,5346],
    [5332,5347],
    [5333,5348],
    [5334,5349],
    [5335,5350],
    [5336,5351],
    [5337,5352],
    [5338,5359],
    [5339,5353],
    [5340,5354],
    [5341,5355],
    [5357,5342],
    [5343,5356],
    [5344,5358],
    [1693,1707],
    [2797,2798],
    [1038,1039],
    [1683,1684],
    [1656,1657],
    [3478,3656],
    [1691,1692],
    [2144,2145],
    [1279,1280],
    [2419,2497],
    [2420,2421],
    [1037,1035],
    [1033,1030],
    [6010,6007],
    [1032,1029],
    [1031,1028],
    [6014,6013],
    [1036,1034],
    [1027,1024],
    [6008,6009],
    [1023,1026],
    [1025,1022],
    [6011,6012],
    [1184,1203],
    [1041,1040],
    [963,965],
    [966,967],
    [969,968],
    [5835,5836],
    [5837,5838],
    [3576,3577],
    [3556,3557],
    [3581,3580],
    [3596,3597],
    [2756,2758],
    [2778,2785],
    [2761,2767],
    [2784,2779],
    [2766,2762],
    [2780,2787],
    [2763,2769],
    [2760,2786],
    [2777,2768],
    [2783,2781],
    [2765,2764],
    [2788,2782],
    [2771,2770],
    [2816,2817],
    [3676,3677],
    [259,1255],
    [1686,1685],
    [4437,4436],
    [5854,5853],
    [6030,6031],
    [1682,1681]
]
titles = []
points = 0
def AddDuplicates():
    for  item in achi_duplicates:
        earned.append(item[0])
        

def iterate_tree(subcategory,tree,earned):
    temp_list = []
    for achi_category in tree:
            if achi_category['id'] not in earned:
                temp_list.append(achi_category)
                global points
                points += achi_category['points']
    subcategory['achievements'] = temp_list
    
achievements = []
if __name__=="__main__":
    #merge all characters data
    fetcher = DiskCacheFetcher('/')
    print "Fetching achievements from battle.net"
    for char_file in characters:
        char_url = base_url + char_file[0]+'/'+char_file[1]+'?fields=achievements'
        #data = fetcher.fetch(char_url,60);
        data = urllib2.urlopen(char_url)
        jdata = json.load(data)
        data.close()
        earned += jdata['achievements']['achievementsCompleted']
        earned += jdata['achievements']['criteria']
    earned = list(set(earned))
    earned.sort()
    print "Finished feshing achievements from battle.net"
    print "Found %d achievement id's" % len(earned)
    AddDuplicates()
    #flatten the achievements into a single dictionary by id
    achi_filename = open("achievements.json")
    achi_tree = json.load(achi_filename)
    achi_filename.close()
    achievement_tree = []
    for main_categories in achi_tree['achievements']:
        #skip feast of strenght
        if main_categories['id'] == 81:
            continue
        main_category = {'name':main_categories['name'], 'id':main_categories['id']}
        #do we have a subcategory like quests -> eastern kingdom
        if 'categories' in main_categories:
            #loop thru all sub and add to main
            subcategory_list = [];
            for achi_under_category in main_categories['categories']:
                subcategory = {'name': achi_under_category['name'], 'id': achi_under_category['id']}
                iterate_tree(subcategory,achi_under_category['achievements'],earned)
                subcategory_list.append(subcategory)
            main_category['categories'] = subcategory_list
        iterate_tree(main_category,main_categories['achievements'],earned)
        achievement_tree.append(main_category)
    #achi_tree_pair = {'achievements':achievement_tree}
    #achievements.append(achi_tree_pair)
    pprint(achievement_tree)
    print "Account Wide Points: %d" % points

