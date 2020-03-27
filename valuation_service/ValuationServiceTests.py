import unittest

from valuation_service.ValuationOperations import ValuationOperations


class ValuationServiceTests(unittest.TestCase):

    def test_data_file_does_not_exist(self):
        operation = ValuationOperations('non-existing_file.csv')
        with self.assertRaises(SystemExit) as cm:
            operation.check_if_data_files_exist_and_are_correct()
        self.assertEqual(cm.exception.code, 0)

    def test_incorrect_data_file_type(self):
        operation = ValuationOperations('incorrect_data.csv')
        with self.assertRaises(SystemExit) as cm:
            operation.check_if_data_files_exist_and_are_correct()
        self.assertEqual(cm.exception.code, 0)

    def test_convert_to_pln_currency_lack_of_initial_currency_in_data_file(self):
        valuation_operation = ValuationOperations('currencies_test.csv')
        with self.assertRaises(ValueError):
            valuation_operation.convert_to_pln_currency(amount=1000, initial_currency="GBP")


if __name__ == '__main__':
    unittest.main()
