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

titles = []
points = 0
def iterate_tree(subcategory,tree,earned):
    temp_list = []
    for achi_category in tree:
            if achi_category['id'] not in earned:
                #duplicate title
                if achi_category['title'] not in titles:
                    titles.append(achi_category['title'])
                    #build achievement list
                    temp_list.append(achi_category)
                    global points
                    points += achi_category['points']
    
    subcategory['achievements'] = temp_list
    #subcategory.append(temp_list)
achievements = []
if __name__=="__main__":
    #merge all characters data
    fetcher = DiskCacheFetcher('/')
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
    print points

