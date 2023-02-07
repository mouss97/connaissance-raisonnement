import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""
SELECT ?item ?itemLabel ?country ?countryLabel ?participants ?participantsLabel ?winner ?winnerLabel

WHERE {
  ?item wdt:P3450 wd:Q19317;
      wdt:P17 ?country.
  ?item wdt:P3450 wd:Q19317;
      wdt:P1132 ?participants.
  ?item wdt:P3450 wd:Q19317;
      wdt:P1346 ?winner.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.io.json.json_normalize(results['results']['bindings'])
results_df= results_df[['item.value', 'itemLabel.value', 'winnerLabel.value',\
            'participantsLabel.value', 'countryLabel.value']].sort_values(by = "itemLabel.value")

results_df.columns = ['item', 'itemLabel', 'winnerLabel', 'participantsLabel', 'countryLabel']
results_df = results_df.reset_index(drop=True)
#save
results_df.to_csv('data.csv', index=False)
