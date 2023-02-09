#####################
##### Libraries #####
#####################
import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON

####################
##### First DF #####
####################
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""
SELECT ?item ?itemLabel ?country ?countryLabel ?participants ?participantsLabel ?winner ?winnerLabel ?leader ?leaderLabel

WHERE {
  ?item wdt:P3450 wd:Q19317;
      wdt:P17 ?country.
  ?item wdt:P3450 wd:Q19317;
      wdt:P1132 ?participants.
  ?item wdt:P3450 wd:Q19317;
      wdt:P1346 ?winner.
  ?item wdt:P3450 wd:Q19317;
      wdt:P3279 ?leader.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.io.json.json_normalize(results['results']['bindings'])
results_df= results_df[['item.value', 'itemLabel.value', 'winnerLabel.value',\
            'participantsLabel.value', 'countryLabel.value', 'leaderLabel.value']].sort_values(by = "itemLabel.value")
results_df.columns = ['item', 'itemLabel', 'winnerLabel', 'participantsLabel', 'countryLabel', 'leaderLabel']
results_df = results_df.reset_index(drop=True)

######################
##### MASCOTS DF #####
######################
sparql.setQuery("""
SELECT ?item ?itemLabel ?mascot ?mascotLabel

WHERE {
  ?item wdt:P3450 wd:Q19317;
      wdt:P822 ?mascot.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
""")

sparql.setReturnFormat(JSON)
mascots = sparql.query().convert()

mascots_df = pd.io.json.json_normalize(mascots['results']['bindings'])
mascots_df = mascots_df[['itemLabel.value', 'mascotLabel.value']].sort_values(by = "itemLabel.value")
mascots_df.columns = ['itemLabel', 'mascotLabel']

#####################
##### MERGE DFS #####
#####################
results_df = results_df.merge(mascots_df, how='left', on='itemLabel')

###########################
##### POST PROCESSING #####
###########################
# Change the teams name to keep the country name only
results_df['winnerLabel'] = [x.split(' ')[0] for x in results_df['winnerLabel']]

# 2002 in both South Korea and Japan
results_df = results_df[results_df['itemLabel'] != '2002 FIFA World Cup']
results_df = results_df.append({'item': 'http://www.wikidata.org/entity/Q19317', 'itemLabel': '2002 FIFA World Cup',
'winnerLabel': 'Brazil', 'participantsLabel': '32',
'countryLabel': 'South Korea & Japan',
'leaderLabel': 'Ronaldo', 'mascotLabel': 'Ato, Kaz and Nik'}, ignore_index=True)

# leaderLabel : cast to string
results_df['leaderLabel'] = results_df['leaderLabel'].astype(str)
# concatenate the leaders for each year
results_df = results_df.groupby(
    ['item', 'itemLabel', 'winnerLabel', 'participantsLabel', 'countryLabel', 'mascotLabel'], dropna=False
        ).agg({'leaderLabel': ', '.join}).reset_index()
# keep an only leader for each year
results_df.loc[results_df['itemLabel'] == '1962 FIFA World Cup', 'leaderLabel'] = 'Garrincha'
results_df.loc[results_df['itemLabel'] == '1994 FIFA World Cup', 'leaderLabel'] = 'Oleg Salenko'
results_df.loc[results_df['itemLabel'] == '2010 FIFA World Cup', 'leaderLabel'] = 'Thomas Müller'
results_df.loc[results_df['itemLabel'] == '2022 FIFA World Cup', 'leaderLabel'] = 'Kylian Mbappé'

# reset the index correctly
results_df.sort_values(by = "itemLabel", inplace = True)
results_df = results_df.reset_index(drop=True)
#save
results_df.to_csv('data.csv', index=False)
