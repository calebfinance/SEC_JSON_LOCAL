# Mutual Fund Data Aggregator

This Python script aggregates data from XML files of a mutual fund and generates a consolidated report.

## Description

The script processes XML files, extracts data for securities with fair value level 3, calculates the share price in USD, and aggregates this data into a single CSV file.

## How to Use

1. Place your XML files in the specified directory.
2. Run the script.
3. The aggregated data will be saved in a CSV file in the output directory.

## Script

(Here, you can include a brief snippet or overview of the script. For the full script, it is recommended to include it as a file in the repository.)

## Output

The output is a CSV file containing aggregated data from the XML files with the following additional fields:
- `Valuation_Date`: The date of valuation extracted from the file name.
- `Share_Price_USD`: Calculated as `valUSD` divided by `balance`.

## Requirements

- Python 3
- pandas
- xml.etree.ElementTree

Make sure these are installed and up to date in your Python environment.

## Author

calebfinance
