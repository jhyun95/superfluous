# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 23:30:00 2019

@author: jhyun_000
"""

import urllib.request, os, re, json
import pandas as pd
GTA_DIR = 'data/gtabase/' # directory to store raw HTML from GTA Base

''' Load files with GTA Base URLs '''
with open('sefUrl.txt', 'r') as f: # vehicles from https://www.gtabase.com/grand-theft-auto/vehicles
    vehicles = eval(f.read())

''' Download missing database entries from GTA Base '''
for vehicle_raw in sorted(vehicles.values()): # download raw html files
    vehicle_name = vehicle_raw.split('\/')[-1]
    vehicle_url = 'https://www.gtabase.com' + vehicle_raw.replace('\/', '/')
    vehicle_out = GTA_DIR + vehicle_name + '.html'
    if not os.path.exists(vehicle_out): # don't re-download
        print('Downloading:', vehicle_url)
        urllib.request.urlretrieve(vehicle_url, vehicle_out)
        
''' Extract data from raw HTML files '''
def remove_html_tags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

vehicle_data = {}
for vehicle_html in os.listdir(GTA_DIR):
    print(vehicle_html)
    vehicle_data[vehicle_html] = {}
    with open(GTA_DIR + vehicle_html, 'r') as f:
        label = ''
        for line in f:
            if 'field-label' in line:
                non_html = remove_html_tags(line).strip()
                label = ' '.join(non_html.split())
            elif 'field-value' in line:
                non_html = remove_html_tags(line).strip()
                value = ' '.join(non_html.split())
                if len(value) > 0:
                    if value[-3:] == 'MPH':
                        value = value.split()[0]
                    elif value[-2:] == 'KG':
                        value = value.split()[0].replace(',','')
                    elif value[0] == '$':
                        value = value[1:].replace(',','')
                        if '(Trade Price)*' in value:
                            value = value.replace('(Trade Price)*', '').strip()
                    elif 'Elitás' in value or 'ElitÃ¡s' in value:
                        value = value.replace('Elitás', 'Elitas')
                        value = value.replace('ElitÃ¡s', 'Elitas')
                    vehicle_data[vehicle_html][label] = value
                    
''' Save data to JSON and TSV '''
with open('data/vehicle_data.json', 'w') as f:
    json.dump(vehicle_data, f, sort_keys=True, indent=4)
df = pd.DataFrame.from_dict(vehicle_data).T
df.to_csv('data/vehicle_data.tsv', sep='\t')