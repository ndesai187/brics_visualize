import pandas as pd
from resources import selection
from src import plot_scatter

country_list = ["BRA", "IND", "RUS", "ZAF", "CHN"]


def filter_gender_stats_csv(inFile, outFile):
    f_data = pd.read_csv(inFile)

    f_data_brics = f_data[f_data["Country Code"].isin(country_list)]
    f_data_indicator = f_data_brics[f_data_brics["Indicator Code"].isin(selection.indi_list_small)]
    f_data_indicator.to_csv(outFile)


def visualize():
    gender_stats_inFile = "../resources/Gender_StatsData.csv"
    gender_stats_outFile = "../target/filtered_gender_stats.csv"
    filter_gender_stats_csv(gender_stats_inFile, gender_stats_outFile)

    # Plot GDP per capita
    gender_stats_df = pd.read_csv(gender_stats_outFile)

    # filter gdp per capita index = NY.GDP.PCAP.CD
    gender_stats_byRow_df = gender_stats_df[(gender_stats_df["Country Code"].isin(country_list)) & (
            gender_stats_df["Indicator Code"] == "NY.GDP.PCAP.CD")]
    gender_stats_byRow_df = gender_stats_byRow_df.fillna(0)
    gender_stats_byCol_list = gender_stats_byRow_df.loc[:,'1980':'2017'].values.tolist()

    # call plot function to create graph
    plot_scatter.plot_graph(list(range(1980, 2018)), country_list, gender_stats_byCol_list)


if __name__ == "__main__":
    visualize()