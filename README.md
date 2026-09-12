# canadian-election-data-analyzer
Python application for analyzing and visualizing Canadian federal election data.

## Overview

This project analyzes data from the 43rd (2019) and 44th (2021) Canadian federal elections. It includes tools for comparing female representation across elections and analyzing elector and population data by province and territory.

## Features

### Female MP Representation Analysis
- Compares the number of female MPs elected in the 2019 and 2021 federal elections
- Filters election results by province or political party
- Calculates changes in female representation between elections
- Sorts results to highlight the largest changes

### Elector and Population Analysis
- Processes provincial and territorial election data from CSV files
- Calculates electors as a percentage of population
- Sorts results from highest to lowest
- Generates processed CSV reports
- Creates an interactive Plotly bar chart

## Technologies

- Python
- CSV data processing
- Plotly
- Command-line arguments

## Running the Project

Install the required dependency:

`pip install -r requirements.txt`

### Female MP Analysis

Filter by province:

`python q1_script.py province Ontario`

Compare all provinces:

`python q1_script.py province All`

Filter by political party:

`python q1_script.py party Liberal`

### Elector and Population Analysis

Run the second analysis:

`python q2_script.py table_tableau01.csv`

Specify a custom output file:

`python q2_script.py table_tableau01.csv --output results.csv`

## Data Source

This project uses publicly available Canadian federal election data from the Government of Canada.

## What I Learned

This project gave me experience working with real-world datasets, processing CSV files, designing command-line programs, validating and filtering data, generating reports, creating data visualizations, and debugging a larger Python application.
