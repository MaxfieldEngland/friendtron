# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 11:34:22 2021

@author: naika
"""

import random

def pick_name(num_options=1):
    nameFile = open("./namefile.txt", "r", encoding="utf8")
    names = nameFile.read().split()
    nameFile.close()
    
    options = []
    
    for _ in range(num_options):
        options.append(random.choice(names))
    
    return options
    
def pick_townname(num_options=1):
    affixes = ['', 'port', 'clare', 'ley', 'view', 'folk', 'sex', 'karta', 'grad',
               'hampton', 'stead', 'stedt', 'stätt', 'dorf', 'wych', 'wick', 
               'wyke', 'wich', 'thorpe', 'thorp', 'ceter', 'ham', 'cester', 'stadt',
               'caster', 'by', 'dale', 'field', 'ford', 'town', 'bury', 'chester', 
               'ton', 'burgh', 'burg', 'ville']
    
    bases = pick_name(num_options)
    towns = []
    for base in bases:
        towns.append(base + random.choice(affixes))
        
    return towns