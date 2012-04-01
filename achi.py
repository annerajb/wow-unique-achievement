#!/usr/bin/env python
import json
import urllib2
import itertools

from pprint import pprint
proxies = {'http': 'http://web-proxy.fc.hp.com.com:8080'}
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
achievements = {}
titles = []
points = 0
def iterate_tree(tree,earned):
    for achi_category in tree:
            #add the achievement to a dictionary with the key as the id
            #
            if achi_category['id'] not in earned:
                #dont add the achievement if we have a achievement title with it's name
                if achi_category['title'] not in titles:
                    titles.append(achi_category['title']);
                    achievements[achi_category['id']] = achi_category;
                    global points
                    points += achi_category['points']
                    #pprint(achi_category)
if __name__=="__main__":
    #merge all characters data
    for char_file in characters:
        char_url = base_url + char_file[0]+'/'+char_file[1]+'?fields=achievements'
        #print '||'+char_url + '||\n'
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
    for categories in achi_tree['achievements']:
        #skip feast of strenght i know this can be done with a slice but it's getting late
        if categories['id'] == 81:
            continue
        if 'categories' in categories:
            for achi_under_category in categories['categories']:
                iterate_tree(achi_under_category['achievements'],earned)
        iterate_tree(categories['achievements'],earned)
    pprint(achievements)
    print len(achievements)
    print points

