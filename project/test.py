import unittest
from unittest.mock import patch
import pandas as pd
import os
import shutil
import sqlite3
from pipeline import DataExtractor, DataTransformer, DataLoader

class TestDataExtractor(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_fetch_csv(self, mock_read_csv):
        # Test the fetch_csv method of DataExtractor with mocked data
        try:
            # Create mock data
            mock_data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
            mock_read_csv.return_value = mock_data

            # Initialize DataExtractor and fetch data
            extractor = DataExtractor('fake_url')
            df = extractor.fetch_csv()

            # Check if the fetched data matches the mock data
            self.assertTrue(df.equals(mock_data))
            print("DataExtractor: test_fetch_csv - Pass")
        except AssertionError:
            print("DataExtractor: test_fetch_csv - Fail")
            raise

class TestDataTransformer(unittest.TestCase):
    def setUp(self):
        # Setup mock data for testing
        self.data = pd.DataFrame({
            'country': ['CountryA', 'CountryB', 'CountryC'],
            'year': [2000, 2001, 2002],
            'co2': [10.0, 20.0, 0.0],
            'AverageTemperatureFahr': [32.0, 50.0, 77.0]
        })

    def test_select_columns(self):
        # Test the select_columns method
        try:
            transformer = DataTransformer(selected_columns=['country', 'year'])
            df = transformer.select_columns(self.data)
            self.assertTrue(list(df.columns) == ['country', 'year'])
            print("DataTransformer: test_select_columns - Pass")
        except AssertionError:
            print("DataTransformer: test_select_columns - Fail")
            raise

    def test_drop_zero_values(self):
        # Test the drop_zero_values method
        try:
            transformer = DataTransformer(selected_columns=['country', 'year', 'co2'], drop_zero='co2')
            df = transformer.drop_zero_values(self.data)
            self.assertFalse((df['co2'] == 0.0).any())
            print("DataTransformer: test_drop_zero_values - Pass")
        except AssertionError:
            print("DataTransformer: test_drop_zero_values - Fail")
            raise

    def test_rename_columns(self):
        # Test the rename_columns method
        try:
            transformer = DataTransformer(selected_columns=['country', 'year'], rename_columns={'country': 'nation'})
            df = transformer.rename_columns(self.data)
            self.assertIn('nation', df.columns)
            self.assertNotIn('country', df.columns)
            print("DataTransformer: test_rename_columns - Pass")
        except AssertionError:
            print("DataTransformer: test_rename_columns - Fail")
            raise

    def test_perform_join(self):
        # Test the perform_join method
        try:
            df1 = pd.DataFrame({'year': [2000, 2001], 'country': ['A', 'B'], 'value1': [1, 2]})
            df2 = pd.DataFrame({'year': [2000, 2001], 'country': ['A', 'B'], 'value2': [3, 4]})
            transformer = DataTransformer([], None)
            joined_df = transformer.perform_join(df1, df2, ['year', 'country'])
            self.assertIn('value1', joined_df.columns)
            self.assertIn('value2', joined_df.columns)
            self.assertEqual(len(joined_df), 2)
            print("DataTransformer: test_perform_join - Pass")
        except AssertionError:
            print("DataTransformer: test_perform_join - Fail")
            raise

    def test_remove_null(self):
        # Test the remove_null method
        try:
            data_with_nulls = pd.DataFrame({'A': [1, 2, None], 'B': [4, None, 6]})
            transformer = DataTransformer([], None)
            df = transformer.remove_null(data_with_nulls)
            self.assertFalse(df.isnull().values.any())
            print("DataTransformer: test_remove_null - Pass")
        except AssertionError:
            print("DataTransformer: test_remove_null - Fail")
            raise

    def test_convert_fahrenheit(self):
        # Test the convert_fahrenheit method
        try:
            transformer = DataTransformer(
                selected_columns=['AverageTemperatureFahr'],
                fahrenheit_column='AverageTemperatureFahr',
                celsius_column='AverageTemperatureCelsius'
            )
            df = transformer.convert_fahrenheit(self.data)
            self.assertIn('AverageTemperatureCelsius', df.columns)
            self.assertAlmostEqual(df['AverageTemperatureCelsius'].iloc[0], 0.0, places=1)
            self.assertAlmostEqual(df['AverageTemperatureCelsius'].iloc[1], 10.0, places=1)
            print("DataTransformer: test_convert_fahrenheit - Pass")
        except AssertionError:
            print("DataTransformer: test_convert_fahrenheit - Fail")
            raise

    def test_process_data(self):
        # Test the complete process_data method
        try:
            transformer = DataTransformer(
                selected_columns=['country', 'year', 'co2', 'AverageTemperatureFahr'],
                drop_zero='co2',
                rename_columns={'country': 'nation'},
                fahrenheit_column='AverageTemperatureFahr',
                celsius_column='AverageTemperatureCelsius'
            )
            df = transformer.process_data(self.data)
            self.assertIn('nation', df.columns)
            self.assertNotIn('country', df.columns)
            self.assertIn('AverageTemperatureCelsius', df.columns)
            self.assertNotIn('AverageTemperatureFahr', df.columns)
            self.assertFalse((df['co2'] == 0.0).any())
            print("DataTransformer: test_process_data - Pass")
        except AssertionError:
            print("DataTransformer: test_process_data - Fail")
            raise

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        # Setup for DataLoader tests
        self.folder_path = './test_data'
        self.sqlite_filename = 'test_climate_data.sqlite'
        self.data = pd.DataFrame({
            'year': [2000, 2001],
            'country': ['A', 'B'],
            'co2': [1.0, 2.0],
            'AverageTemperatureCelsius': [0.0, 10.0]
        })
        self.loader = DataLoader(self.folder_path, self.sqlite_filename)

    def tearDown(self):
        # Cleanup after tests
        shutil.rmtree(self.folder_path, ignore_errors=True)

    def test_create_directory(self):
        # Test the create_directory method
        try:
            self.loader.create_directory()
            self.assertTrue(os.path.isdir(self.folder_path))
            print("DataLoader: test_create_directory - Pass")
        except AssertionError:
            print("DataLoader: test_create_directory - Fail")
            raise

    def test_save_to_sqlite(self):
        # Test the save_to_sqlite method
        try:
            self.loader.create_directory()
            self.loader.save_to_sqlite(self.data, 'climate_data')
            conn = sqlite3.connect(os.path.join(self.folder_path, self.sqlite_filename))
            df = pd.read_sql_query("SELECT * FROM climate_data", conn)
            conn.close()
            self.assertTrue(df.equals(self.data))
            print("DataLoader: test_save_to_sqlite - Pass")
        except AssertionError:
            print("DataLoader: test_save_to_sqlite - Fail")
            raise

    def test_output_file_exists(self):
        # Test if the output SQLite file exists
        try:
            self.loader.create_directory()
            self.loader.save_to_sqlite(self.data, 'climate_data')
            output_file_path = os.path.join(self.folder_path, self.sqlite_filename)
            self.assertTrue(os.path.isfile(output_file_path))
            print("DataLoader: test_output_file_exists - Pass")
        except AssertionError:
            print("DataLoader: test_output_file_exists - Fail")
            raise

if __name__ == '__main__':
    unittest.main()
