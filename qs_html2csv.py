import math
import subprocess

try:
	from bs4 import BeautifulSoup
except:
	subprocess.call(['pip', 'install', 'bs4'])
try:
	import numpy as np
except:
	subprocess.call(['pip', 'install', 'numpy'])
try:
	import pandas as pd
except:
	subprocess.call(['pip', 'install', 'pandas'])


with open('qs_rankings_table_html.rtf', 'r') as f:
	qshtml = BeautifulSoup(f, 'html.parser')

index_col = 'university'
cols = [
	'overall score', 
	'international students ratio',
	'international faculty ratio',
	'faculty student ratio',
	'citations per faculty',
	'academic reputation',
	'employer reputation'
]

subtables = qshtml.find_all('div', {'id': 'ranking-data-load_ind'})
universities = []
all_rows = []
for t in subtables:
	row_objects = t.find_all('div', {'class': 'row ind-row'})
	for ro in row_objects:
		ro = ro.find(
			'div', {'class': 'col-lg-12'}
		).find(
			'div', {'class': '_qs-ranking-data-header-new-white'}
		).find(
			'div', {'class': 'row'}
		)

		university = ro.find(
			'div', {'class': 'col-lg-5 _right_background'}
		).find(
			'div', {'class': 'row'}
		).find(
			'div', {'class': 'col-lg-12 no-right-padding'}
		).find(
			'div', {'class': '_qs-ranking-data-row no-top-bottom-border fixed-height'}
		).find(
			'div', {'class': 'row'}
		).find(
			'div', {'class': 'col-lg-9 no-padding-indicator-left hide-this-in-mobile-indi'}
		).find(
			'div', {'class': 'university-rank-row'}
		).find(
			'div', {'class': 'td-wrap'}
		).find(
			'div', {'class': 'td-wrap-in'}
		)('a')[0].text
		universities.append(university)

		current_metrics = []

		metric_objects = ro.find(
			'div', {'class': 'col-lg-7 no-left-margin-padding'}
		).find(
			'div', {'class': 'row'}
		).find(
			'div', {'class': 'col-lg-12 no-right-padding'}
		).find(
			'div', {'class': '_scrollable_div all-columns-by-js dxnew-container-institutes _scrollable_div_withdata move-all-js'}
		).find_all(
			'div', {'class': '_smallblocksfix-width _mt_not_scrollbar sort_by_university asc move-all-js'}
		)

		for mo in metric_objects:
			
			metric = mo.find(
				'div', {'class': '_data-set'}
			).findChildren(
				'div', recursive=False
			)[0].find(
				'span'
			).find(
				'div', {'class': 'td-wrap'}
			).find(
				'div', {'class': 'td-wrap-in'}
			).text
			if metric == '-':
				metric = math.nan
			else:
				metric = float(metric)
		
			current_metrics.append(metric)

		all_rows.append(current_metrics)


rows = np.vstack(all_rows)
data = pd.DataFrame(rows, columns=cols)
data.index = universities
data.to_csv('qs_rankings_2022.csv')
print(data.head())
