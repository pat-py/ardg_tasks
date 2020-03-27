import os
import sys

import pandas as pd


class ValuationOperations:

    def __init__(self, data_file, currencies='currencies.csv', matchings='matchings.csv'):
        self.data_file = data_file
        self.currencies_file = currencies
        self.matchings_file = matchings

    def check_if_data_files_exist_and_are_correct(self):
        data_files_list = [self.data_file, self.currencies_file, self.matchings_file]

        for file in data_files_list:
            if os.path.isfile(file):
                try:
                    with open(file) as csv_file:
                        pd.read_csv(csv_file, index_col=False)
                except ValueError:
                    print(f"File {file} has incorrect format")
                    sys.exit(0)
            else:
                print(f"File {file} does not exist")
                sys.exit(0)

    def convert_to_pln_currency(self, amount: int, initial_currency: str):
        with open(self.currencies_file) as csv_file:
            df = pd.read_csv(csv_file, index_col='currency')
            converter = df.loc[initial_currency, 'ratio']
        return amount * converter

    @staticmethod
    def calculate_total_price(price: int, quantity: int):
        return price * quantity

    def change_data_prices_into_pln_currency(self):
        with open(self.data_file) as csv_file:
            df = pd.read_csv(csv_file, index_col='id').copy()
            for index, row in df.iterrows():
                if row['currency'] != 'PLN':
                    df.loc[index, 'price'] = self.convert_to_pln_currency(df.loc[index, 'price'],
                                                                          df.loc[index, 'currency'])
                    df.loc[index, 'currency'] = 'PLN'
        return df

    @staticmethod
    def add_total_price_column(data_file):
        for index, row in data_file.iterrows():
            data_file.loc[index, 'total price'] = ValuationOperations.calculate_total_price(
                data_file.loc[index, 'price'], data_file.loc[index, 'quantity'])

        return data_file

    @staticmethod
    def create_dict_with_matching_ids_keys_and_total_prices_values(data_file):
        total_prices_dict = {}
        matching_ids_set = set(data_file['matching_id'].to_list())

        for id in matching_ids_set:
            total_prices_list = []
            for index, row in data_file.iterrows():
                if data_file.loc[index, 'matching_id'] == id:
                    total_prices_list.append(data_file.loc[index, 'total price'])
                total_prices_list.sort()
            total_prices_dict[id] = total_prices_list
        return total_prices_dict

    def prepare_data_for_output_file(self, data_dict):
        ids_list = []
        total_prices_list = []
        avg_prices_list = []
        currencies_list = []
        ignored_product_counts_list = []

        with open(self.matchings_file) as csv_file:
            df = pd.read_csv(csv_file, index_col='matching_id')
            for key in list(data_dict.keys()):
                ids_list.append(key)
                aggregated_prices = sum(data_dict[key][:df.loc[key, 'top_priced_count']])
                total_prices_list.append(aggregated_prices)
                avg_prices_list.append(aggregated_prices / df.loc[key, 'top_priced_count'])
                currencies_list.append('PLN')
                ignored_product_counts_list.append(len(data_dict[key]) - df.loc[key, 'top_priced_count'])

            output_dict = {'matching_id': ids_list, 'total_price': total_prices_list, 'avg_price': avg_prices_list,
                           'currency': currencies_list, 'ignored_product_count': ignored_product_counts_list}

        return output_dict

    @staticmethod
    def write_to_csv_file(data_dict, output_file_name):
        df = pd.DataFrame(data_dict)
        df.to_csv(output_file_name, index=False)
