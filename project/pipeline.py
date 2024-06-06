import os
import shutil
import pandas as pd
import sqlite3

class DataExtractor:
    def __init__(self, url):
        self.url = url

    def fetch_csv(self):
        # Fetch the CSV data into a DataFrame
        df = pd.read_csv(self.url)
        return df

class DataTransformer:
    def __init__(self, selected_columns, drop_zero=None, rename_columns=None, fahrenheit_column=None, celsius_column=None):
        self.selected_columns = selected_columns
        self.drop_zero = drop_zero
        self.rename_columns_map = rename_columns
        self.fahrenheit_column = fahrenheit_column
        self.celsius_column = celsius_column

    def select_columns(self, df):
        # Select specific columns
        return df[self.selected_columns]

    def drop_zero_values(self, df):
        # Drop rows where the specified column value is 0.0, if applicable
        if self.drop_zero:
            df = df[df[self.drop_zero] != 0.0]
        return df

    def rename_columns(self, df):
        # Rename columns, if applicable
        if self.rename_columns_map:
            df = df.rename(columns=self.rename_columns_map)
        return df
    
    def perform_join(self, df1, df2, join_columns):
        # Perform a join on specified columns
        return pd.merge(df1, df2, on=join_columns)

    def remove_null(self, df):
        # Removes rows with null values. 
        return df.dropna()

    def convert_fahrenheit(self, df):
        # Convert Fahrenheit to Celsius
        if self.fahrenheit_column and self.celsius_column:
            df[self.celsius_column] = (df[self.fahrenheit_column] - 32) * 5.0/9.0
            df = df.drop(columns=[self.fahrenheit_column])
        return df

    def process_data(self, df):
        df = self.select_columns(df)
        df = self.remove_null(df)
        df = self.drop_zero_values(df)
        df = self.rename_columns(df)
        df = self.convert_fahrenheit(df)
        return df

class DataLoader:
    def __init__(self, folder_path, sqlite_filename):
        self.folder_path = folder_path
        self.sqlite_filename = sqlite_filename

    def create_directory(self):
        # Ensures the target directory exists or creates it
        shutil.rmtree(self.folder_path, ignore_errors=True)
        os.makedirs(self.folder_path)

    def save_to_sqlite(self, df, table_name):
        # Save the DataFrame to SQLite database
        conn = sqlite3.connect(os.path.join(self.folder_path, self.sqlite_filename))
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

class Application:
    def __init__(self, extractor, transformer, loader=None):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        df = self.extractor.fetch_csv()
        processed_df = self.transformer.process_data(df)
        return processed_df

# Dataset 1: CO2 and Greenhouse Gas Emissions
co2_url = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
co2_selected_columns = ['country', 'year', 'co2']
co2_extractor = DataExtractor(co2_url)
co2_transformer = DataTransformer(co2_selected_columns, drop_zero='co2')
co2_app = Application(co2_extractor, co2_transformer)
co2_df_selected = co2_app.run()  # Running the extractor and transformer

# Dataset 2: Earth Surface Temperature Data
temperature_url = "https://figshare.com/ndownloader/files/4938964"
temperature_selected_columns = ['year', 'AverageTemperatureFahr', 'Country']
temperature_rename_columns = {'Country': 'country'}
temperature_extractor = DataExtractor(temperature_url)
temperature_transformer = DataTransformer(
    temperature_selected_columns, 
    rename_columns=temperature_rename_columns,
    fahrenheit_column='AverageTemperatureFahr', 
    celsius_column='AverageTemperatureCelsius'
)
temperature_app = Application(temperature_extractor, temperature_transformer)
temperature_df_selected = temperature_app.run()  # Running the extractor and transformer

# Perform a join on "year" and "country" columns
data_transformer = DataTransformer([], None)
joined_df = data_transformer.perform_join(co2_df_selected, temperature_df_selected, ['year', 'country'])

# Save the joined DataFrame to SQLite database
folder_path = "../data"
sqlite_filename = "climate_data.sqlite"
data_loader = DataLoader(folder_path, sqlite_filename)
data_loader.create_directory()
data_loader.save_to_sqlite(joined_df, "climate_data")
