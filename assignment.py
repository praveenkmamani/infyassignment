
import csv
import os
from collections import defaultdict
import dateutil.parser as dparse


def parse_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def unify_data(bank_data):
    parserinfo = dparse.parserinfo(dayfirst=True, yearfirst=False)              # this is to parse the date into a single format.
    unified_data = defaultdict(list)
    for bank, data in bank_data.items():
        for entry in data:
            date_field = find_field(entry, ['date', 'timestamp', 'date_readable'])  # identifying the fields present or not
            desc_field = find_field(entry, ['type', 'transaction'])                 # and taking the values.
            amount_field = find_field(entry, ['amount', 'amounts', 'euro'])
            if amount_field == "euro":                                          # this condition is to gather euro and cents
                cents_field = entry.get("cents", "")
                entry[amount_field] = ".".join([entry[amount_field], cents_field])

            unified_data['Bank'].append(bank)
            unified_data['Date'].append(dparse.parse(entry[date_field], parserinfo, fuzzy=True).date())
            unified_data['Transaction Type'].append(entry[desc_field])
            unified_data['Amount'].append(entry[amount_field])
            unified_data['To'].append(entry["to"])
            unified_data['From'].append(entry["from"])
    return unified_data


# This function finds the field present in that csv dictionary or not.
def find_field(entry, possible_fields):
    for field in possible_fields:
        if field in entry:
            return field
    return next(iter(entry))


def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as csv_file:
        fieldnames = ['Bank', 'Date', 'Transaction Type', 'Amount', 'To', 'From']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for i in range(len(data['Date'])):
            row = {field: data[field][i] for field in fieldnames}
            csv_writer.writerow(row)


if __name__ == "__main__":
    bank_files = os.listdir(os.getcwd() + r'\files')

    # Parsing data from different banks
    bank_data = {}
    for bank_file in bank_files:
        bank_name = os.path.splitext(os.path.basename(bank_file))[0]
        file_path = "{0}\\files\\{1}".format(os.getcwd(), bank_file)
        bank_data[bank_name] = parse_csv(file_path)

    # Unifying data
    final_data = unify_data(bank_data)

    # Writing to a CSV file
    output_file = 'unified_data.csv'
    write_to_csv(final_data, output_file)

    print(f'Unified data has been written to {output_file}')

