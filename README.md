# Exercise Badges

![](https://byob.yarr.is/AnikKazi-dev/Kazi_MADE/score_ex1) ![](https://byob.yarr.is/AnikKazi-dev/Kazi_MADE/score_ex2) ![](https://byob.yarr.is/AnikKazi-dev/Kazi_MADE/score_ex3) ![](https://byob.yarr.is/AnikKazi-dev/Kazi_MADE/score_ex4) ![](https://byob.yarr.is/AnikKazi-dev/Kazi_MADE/score_ex5)

# Climate Confluence: Analyzing the Impact of CO2 Emissions on Global Temperature Trends

## Project Overview
This project, "Climate Confluence: Analyzing the Impact of CO2 Emissions on Global Temperature Trends," examines the correlation between CO2 emissions and global temperature changes. The study utilizes datasets on CO2 emissions and global temperatures to explore this relationship, aiming to provide evidence for effective climate change strategies.

## Contents
- [Introduction](#introduction)
- [Datasets](#datasets)
- [Data Pipeline](#data-pipeline)
- [Project Setup](#project-setup)
- [Analysis and Results](#analysis-and-results)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction
The primary objective of this project is to understand how CO2 emissions influence global temperatures. By analyzing historical data, we aim to identify trends and correlations that highlight the impact of CO2 emissions on global warming.

## Datasets
We have used two main datasets for this analysis:
1. **CO2 and Greenhouse Gas Emissions Dataset**
   - **Metadata URL:** [GitHub Repository](https://github.com/owid/co2-data/tree/master)
   - **Data URL:** [Download CSV](https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv)
2. **Earth Surface Temperature Data**
   - **Metadata URL:** [Figshare](https://figshare.com/articles/dataset/temperature_csv/3171766/1)
   - **Data URL:** [Download CSV](https://figshare.com/ndownloader/files/4938964)

## Data Pipeline
The project follows an ETL (Extract, Transform, Load) pipeline to process the data:

<figure align="center" style="width:120%">
    <img src="project/assets/ETL_Pipeline_Diagram.png"
         alt="ETL Pipeline Flow"
         style="width:60%">
    <figcaption>Figure: ETL Pipeline</figcaption>
</figure>


1. **Extract**
   - Fetches CSV data from specified URLs.
2. **Transform**
   - Cleans and preprocesses the data, including handling null values, converting temperatures from Fahrenheit to Celsius, and renaming columns.
3. **Load**
   - Saves the processed data into an SQLite database.


## Project Setup
To set up this project, follow these steps:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/AnikKazi-dev/Kazi_MADE.git
   cd Kazi_MADE

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments
This project was conducted by Kazi Anik Islam at Friedrich-Alexander-Universität Erlangen-Nürnberg in a course named Methods of Advanced Data Engineering. Special thanks to the providers of the CO2 emissions and temperature datasets.

