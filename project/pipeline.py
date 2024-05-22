import os
import shutil
import pandas as pd
import sqlite3

def fetch_csv(url):
    # fetch the CSV data into a DataFrame
    df = pd.read_csv(url)
    return df

# Dataset 1: CO2 and Greenhouse Gas Emissions
co2_url = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
co2_df = fetch_csv(co2_url)

# Select specific columns
selected_columns = ['country', 'year', 'co2_per_capita']
co2_df_selected = co2_df[selected_columns]

# Drop rows with null values and rows where values are 0.0
co2_df_selected = co2_df_selected.dropna()
co2_df_selected = co2_df_selected[co2_df_selected['co2_per_capita'] != 0.0]

# # Save the CO2 DataFrame to an SQLite database
# sqlite_filename = "climate_data.sqlite"
# table_name = "co2_emissions"
# conn = sqlite3.connect(sqlite_filename)
# co2_df_selected.to_sql(table_name, conn, if_exists='replace', index=False)
# conn.close()



# Dataset 2: Earth Surface Temperature Data
temperature_url = "https://figshare.com/ndownloader/files/4938964"
temperature_df = fetch_csv(temperature_url)

# Select specific columns
selected_columns = ['year','AverageTemperatureFahr', 'Country']
temperature_df_selected = temperature_df[selected_columns]

# Drop rows with null values and rename column
temperature_df_selected = temperature_df_selected.dropna()
temperature_df_selected = temperature_df_selected.rename(columns={'Country': 'country'})

# # Save the temperature DataFrame to an SQLite database
# sqlite_filename2 = "temperature_data.sqlite"
# temperature_table_name = "temperature_data"
# conn = sqlite3.connect(sqlite_filename2)
# temperature_df_selected.to_sql(temperature_table_name, conn, if_exists='replace', index=False)
# conn.close()



# Perform a join on "year" and "country" columns
joined_df = pd.merge(co2_df_selected, temperature_df_selected, on=['year', 'country'])

# Creating folder
folder_path = "../data"
shutil.rmtree(folder_path, ignore_errors=True)
os.makedirs(folder_path)

# Save the joined DataFrame to SQLite database
joined_table_name = "joined_climate_data"
sqlite_filename3 = "joined_climate_data.sqlite"
conn = sqlite3.connect(os.path.join(folder_path, sqlite_filename3))
joined_df.to_sql(joined_table_name, conn, if_exists='replace', index=False)
conn.close()