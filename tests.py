import unittest
import os, csv
import datetime
from assignment import parse_csv, unify_data, write_to_csv


class TestCSVParser(unittest.TestCase):
    def setUp(self):
        # Create temporary test files for each bank
        self.bank1_file = 'test_bank1.csv'
        self.bank2_file = 'test_bank2.csv'
        self.bank3_file = 'test_bank3.csv'

        self.create_test_csv(self.bank1_file, ['timestamp', 'type', 'amount', 'from', 'to'],
                             ['2022-10-01 10:00:00', 'Deposit', '100.00', 'John', 'Savings'])
        self.create_test_csv(self.bank2_file, ['date', 'transaction', 'amounts', 'to', 'from'],
                             ['2022-10-02', 'Withdrawal', '50.00', 'Savings', 'John'])
        self.create_test_csv(self.bank3_file, ['date_readable', 'type', 'euro', 'cents', 'to', 'from'],
                             ['2022-10-03', 'Transfer', '75', '50', 'Savings', 'John'])

    def tearDown(self):
        os.remove(self.bank1_file)
        os.remove(self.bank2_file)
        os.remove(self.bank3_file)

    def create_test_csv(self, file_path, headers, data):
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headers)
            csv_writer.writerow(data)

    def test_unify_data(self):
        bank_files = [self.bank1_file, self.bank2_file, self.bank3_file]

        bank_data = {}
        for bank_file in bank_files:
            bank_name = os.path.splitext(os.path.basename(bank_file))[0]
            bank_data[bank_name] = parse_csv(bank_file)

        unified_data = unify_data(bank_data)

        # Check if the unified data has the expected format
        self.assertIn('Date', unified_data)
        self.assertIn('Transaction Type', unified_data)
        self.assertIn('Amount', unified_data)
        self.assertIn('Bank', unified_data)

        # Check if the unified data has the correct values
        self.assertEqual(len(unified_data['Date']), 3)
        self.assertEqual(len(unified_data['Transaction Type']), 3)
        self.assertEqual(len(unified_data['Amount']), 3)
        self.assertEqual(len(unified_data['Bank']), 3)

        # Check if the Date column is in timestamp format
        for timestamp in unified_data['Date']:
            self.assertIsInstance(timestamp, datetime.date)

    def test_write_to_csv(self):
        bank_files = [self.bank1_file, self.bank2_file, self.bank3_file]
        bank_data = {}
        for bank_file in bank_files:
            bank_name = os.path.splitext(os.path.basename(bank_file))[0]
            bank_data[bank_name] = parse_csv(bank_file)

        unified_data = unify_data(bank_data)

        output_file = 'test_unified_data.csv'
        write_to_csv(unified_data, output_file)

        # Check if the output file exists
        self.assertTrue(os.path.exists(output_file))

        # Clean up
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
