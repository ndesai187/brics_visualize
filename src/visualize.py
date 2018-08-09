import pandas as pd
import numpy as np
from resources import selection
from src import plot_scatter, plot_bubble_map

country_list = ["BRA", "CHN", "IND", "RUS", "ZAF"]


def filter_gender_stats_csv(inFile, outFile):
    f_data = pd.read_csv(inFile)

    f_data_brics = f_data[f_data["Country Code"].isin(country_list)]
    f_data_indicator = f_data_brics[f_data_brics["Indicator Code"].isin(selection.indi_list_small)]
    f_data_indicator.to_csv(outFile)


def trigger_scatter_plot(infile, indicator, step_data_points):
    # Plot GDP per capita
    gender_stats_df = pd.read_csv(infile)

    # filter based on indicator
    gender_stats_byRow_df = gender_stats_df[(gender_stats_df["Country Code"].isin(country_list)) & (
            gender_stats_df["Indicator Code"] == indicator)]
    gender_stats_byRow_df = gender_stats_byRow_df.fillna(0)
    gender_stats_byCol_list = gender_stats_byRow_df.loc[:, '1980':'2017': step_data_points].values.tolist()
    # call plot function to create graph
    plot_scatter.plot_graph(list(range(1980, 2018, step_data_points)), country_list, gender_stats_byCol_list,
                            output_png=indicator)


def trigger_bubble_plot(infile, indicator):
    # read gender stat csv
    gender_stats_df = pd.read_csv(infile)

    # filter based on indicator
    gender_stats_byRow_df = gender_stats_df[(gender_stats_df["Country Code"].isin(country_list)) & (
            gender_stats_df["Indicator Code"] == indicator)]
    gender_stats_byRow_df = gender_stats_byRow_df.fillna(0)

    total_gdp_df = pd.DataFrame()
    total_gdp_df['country_code'] = np.asarray(country_list)
    total_gdp_df['gdp_total'] = gender_stats_byRow_df['2017'].values

    country_df = pd.read_csv('../resources/Gender_StatsCountry.csv')
    total_gdp_df['country_iso'] = country_df['2-alpha code'][country_df['Country Code'].isin(country_list)].values

    country_capitals_df = pd.read_csv('../resources/country-capitals.csv')
    total_gdp_df['capital'] = country_capitals_df['CapitalName'][
        country_capitals_df['CountryCode'].isin(total_gdp_df['country_iso'].values)].values
    total_gdp_df['CapitalLatitude'] = country_capitals_df['CapitalLatitude'][
        country_capitals_df['CountryCode'].isin(total_gdp_df['country_iso'].values)].values
    total_gdp_df['CapitalLongitude'] = country_capitals_df['CapitalLongitude'][
        country_capitals_df['CountryCode'].isin(total_gdp_df['country_iso'].values)].values
    plot_bubble_map.plot_bubble_map(total_gdp_df)


def visualize():
    gender_stats_inFile = "../resources/Gender_StatsData.csv"
    gender_stats_outFile = "../target/filtered_gender_stats.csv"
    filter_gender_stats_csv(gender_stats_inFile, gender_stats_outFile)

    # trigger GDP per capita plot
    gdp_per_capita_indicator = "NY.GDP.PCAP.CD"
    step_data_points = 1
    trigger_scatter_plot(gender_stats_outFile, gdp_per_capita_indicator, step_data_points)

    gdp_growth_indicator = "NY.GDP.MKTP.KD.ZG"
    trigger_scatter_plot(gender_stats_outFile, gdp_growth_indicator, step_data_points)

    gdp_indicator = "NY.GDP.MKTP.CD"
    trigger_bubble_plot(gender_stats_outFile, gdp_indicator)


if __name__ == "__main__":
    visualize()
