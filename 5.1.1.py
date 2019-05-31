# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Table 5.1.1: Treatment exit reasons of all young people exiting treatment 2017-18

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/statistics/substance-misuse-treatment-for-young-people-statistics-2017-to-2018')
dist = scraper.distribution(title=lambda t: t.startswith('Data tables'))
tabs = {tab.name: tab for tab in dist.as_databaker()}
tab = tabs['5.1.1 Service Exits']

cell = tab.filter('Treatment exit reason')
cell.assert_one()
treatment = cell.fill(DOWN).is_not_blank().is_not_whitespace() 
obs = tab.one_of(['n'])
observations = obs.fill(DOWN).is_not_blank().is_not_whitespace().is_number()

Dimensions = [
            HDimConst('Measure Type','Count'),
            HDim(treatment,'Clients in treatment',DIRECTLY, LEFT),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()

import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)

new_table['Clients in treatment'] = new_table['Clients in treatment'].map(
    lambda x: {
        'Total' : 'total',
        'Completed' : 'completed',
        'Dropped out / left' : 'dropped-out-or-left',
        'Referred on' : 'referred-on',
        'Treatment declined by client' : 'treatment-declined-by-client',
        'Other' : 'other',
        'Prison'  : 'prison' }.get(x, x))

new_table['Basis of treatment'] =  'treatment-exit-reasons/' + new_table['Clients in treatment']

new_table['Period'] = '2017-18'
new_table['Substance'] = 'All'
new_table = new_table[['Period','Basis of treatment','Substance','Clients in treatment','Measure Type','Value','Unit']]

new_table


