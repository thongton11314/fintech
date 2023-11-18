import csv
import json

def convert_csv_to_json(csv_filename, json_filename):
    data = []
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)
    
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# Usage:
csv_filename = 'symbols_all.csv'
json_filename = 'symbols.json'
convert_csv_to_json(csv_filename, json_filename)
