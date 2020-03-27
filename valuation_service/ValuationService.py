from valuation_service.ValuationOperations import ValuationOperations


class ValuationService:

    def __init__(self, data='data.csv'):
        self.data = data

    def valuate_data(self):
        valuation = ValuationOperations(self.data)
        valuation.check_if_data_files_exist_and_are_correct()
        data_file = valuation.change_data_prices_into_pln_currency()
        data_file = valuation.add_total_price_column(data_file)
        data_dict = valuation.create_dict_with_matching_ids_keys_and_total_prices_values(data_file)
        output_file = valuation.prepare_data_for_output_file(data_dict)
        valuation.write_to_csv_file(output_file, 'top_products.csv')


if __name__ == "__main__":
    service = ValuationService()
    service.valuate_data()
