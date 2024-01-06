# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 10:59:43 2024

@author: caleb
"""

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import re
from datetime import datetime

def parse_invstOrSec(element):
    """ Parse the <invstOrSec> element and return a dictionary of its children. """
    return {child.tag: child.text for child in element}

def clean_column_name(col_name):
    """ Remove the namespace from the column name """
    return col_name.replace('{http://www.sec.gov/edgar/nport}', '')

def extract_date_from_filename(file_path):
    """ Extract the date from the filename assuming the format is like 'SOI_MM_DD_YY.xml'. """
    match = re.search(r'SOI_(\d+_\d+_\d+).xml', file_path)
    if match:
        date_str = match.group(1).replace('_', '/')
        return datetime.strptime(date_str, '%m/%d/%y').strftime('%Y-%m-%d')
    return None

# Directory containing the XML files
xml_directory = 'C:/Mutual_Funds/Fidelity_Blue_Chip_Growth_Fund/XML'

# Directory to save the output CSV file
output_directory = 'C:/Mutual_Funds/Fidelity_Blue_Chip_Growth_Fund/Output'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

output_csv_filename = 'SOI_ledger.csv'
csv_file_path = os.path.join(output_directory, output_csv_filename)

# Listing all XML files in the directory
file_paths = glob.glob(os.path.join(xml_directory, '*.xml'))

aggregated_df = pd.DataFrame()

for file_path in file_paths:
    date = extract_date_from_filename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'nport': 'http://www.sec.gov/edgar/nport'}
    invstOrSec_data = [parse_invstOrSec(elem) for elem in root.findall('.//nport:invstOrSec', ns)]
    df = pd.DataFrame(invstOrSec_data)
    
    fair_val_level_column = '{http://www.sec.gov/edgar/nport}fairValLevel'
    if fair_val_level_column in df.columns:
        filtered_df = df[df[fair_val_level_column] == '3']
        filtered_df['Valuation_Date'] = date
        filtered_df['Share_Price_USD'] = pd.to_numeric(filtered_df['{http://www.sec.gov/edgar/nport}valUSD']) / pd.to_numeric(filtered_df['{http://www.sec.gov/edgar/nport}balance'])
        columns_order = ['Valuation_Date', 'Share_Price_USD'] + [col for col in filtered_df.columns if col not in ['Valuation_Date', 'Share_Price_USD']]
        filtered_df = filtered_df[columns_order]
        filtered_df.columns = [clean_column_name(col) for col in filtered_df.columns]
        aggregated_df = pd.concat([aggregated_df, filtered_df], ignore_index=True)

# Save the aggregated DataFrame to the specified output directory
aggregated_df.to_csv(csv_file_path, index=False)

print(f"Aggregated data saved to {csv_file_path}")
