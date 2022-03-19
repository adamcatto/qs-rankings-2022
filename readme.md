# Generate 2022 QS ranking data

## Introduction

Since QS hasn't gotten back to me about raw data, I decided to scrape the information that is publicly available and use it to generate the desired data.

Initial data was manually selected from source HTML elements on https://www.topuniversities.com/university-rankings/world-university-rankings/2022

The Python program transforms this HTML into a Pandas DataFrame, and writes to CSV.

## Usage

You can download this repository, `cd` to the location of this folder on your local machine, and type

`python qs_html2csv.py`

this will generate the csv file `qs_rankings_2022.csv`, to be used downstream.