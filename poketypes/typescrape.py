# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:29:14 2019

@author: jhyun_000
"""

import pandas as pd

monotype_effectiveness = {}; values = []
with open('data/monotypes_raw.html', 'r') as f:
    for line in f:
        if 'type-fx-cell' in line:
            for entry in line.split('</td>'):
                if '<td' in entry:
                    ''' Parse two involved types and effectiveness '''
                    data = entry.replace('"','')
                    data = data.split('<td title=')[1]
                    data = data.split('class=type-fx-cell')[0]
                    offensive, _, defensive= data.split()[:3]
                    multiplier = entry.split('>')[-1]
                    multiplier = {'2':2.0, '':1.0, '&frac12;':0.5, '0':0}[multiplier]
                    #result = data.split('=')[-1].strip().replace('"','')
                    #print(offensive, defensive, result, multiplier)
                    
                    ''' Convert effectiveness into multiplier '''
                    if not offensive in monotype_effectiveness:
                        monotype_effectiveness[offensive] = {} 
                    monotype_effectiveness[offensive][defensive] = multiplier
                    values.append(multiplier)

df_monotype = pd.DataFrame.from_dict(monotype_effectiveness).T
df_monotype.to_csv('data/monotypes.csv')