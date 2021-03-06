import pandas as pd
import numpy as np
from resources import selection
from src import plot_scatter, plot_bubble_map

country_list = ["BRA", "CHN", "IND", "RUS", "ZAF"]
# country_list = ["PAK", "PHL", "THA", "TUR",  "ZWE"]
# country_list = ["AFG", "COL", "PAK", "TUR",  "ZWE"]

# comment PPP and NFI generation
# country_list = ["AFG", "CHL", "GRC", "PAK", "SYR"]
# country_list = ["IRN", "IRQ", "MAR", "LBY", "SYR"]
# commend PPP generation
# country_list = ["DEU", "FRA", "GBR", "SWE", "USA"]

'''
This function will filter initial gender stats file to better utilise memory
The functionality is already implemented in genderFilteredByIndicator(), but
the idea is to filter initial list itself.'''
def filterGenderStatsFile(inFile, outFile):
    f_data = pd.read_csv(inFile)

    f_data_brics = f_data[f_data['Country Code'].isin(country_list)]
    f_data_indicator = f_data_brics[f_data_brics['Indicator Code'].isin(selection.indi_list_small)]
    f_data_indicator.to_csv(outFile)


'''
This function will filter gender stats file with 3 inputs
yearColumnFrom - start year
yearColumnTo - end year
indicator - index to be filtered'''
def genderFilteredByIndicator(infile, yearColumnFrom, yearColumnTo, indicator, step_data_points):
    gender_stats_df = pd.read_csv(infile)
    gender_stats_byRow_df = gender_stats_df[(gender_stats_df['Country Code'].isin(country_list)) & (
            gender_stats_df['Indicator Code'] == indicator)]
    gender_stats_byRow_df = gender_stats_byRow_df.fillna(0)
    if (yearColumnFrom == 'NA') & (yearColumnTo == 'NA'):
        return gender_stats_byRow_df
    else:
        gender_stats_byCol_list = gender_stats_byRow_df.loc[:,
                                  yearColumnFrom: yearColumnTo: step_data_points].values.tolist()
        return gender_stats_byCol_list


# Filter data and trigger simple scatter plot
def triggerScatterPlot(infile, indicator, step_data_points, y_axis_label_lst):
    gender_stats_byCol_list = genderFilteredByIndicator(infile, str(1980), str(2017), indicator, step_data_points)

    # call plot function to create graph
    plot_scatter.plotSimpleScatterGraph(list(range(1980, 2018, step_data_points)), country_list,
                                        gender_stats_byCol_list, y_axis_label_lst,
                                        output_png=indicator)


# Filter data and trigger bubble map
def triggerBubblePlot(infile, indicator):
    gender_stats_byRow_df = genderFilteredByIndicator(infile, 'NA', 'NA', indicator, 1)

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
    plot_bubble_map.plotBubbleMap(total_gdp_df)


# Filter data and trigger multi axis scatter plot
def unEmplotementAndPPP(inFile_ppp, inFile_gender, indicator_female, indicator_male, y_axis_label_1, y_axis_label_2):
    dataset_df = pd.DataFrame()

    # filter our and group by values from PPP file
    f_ppp = pd.read_excel(inFile_ppp)
    f_ppp = f_ppp.convert_objects(convert_numeric=True)
    f_ppp['TotalInvestment'] = f_ppp['TotalInvestment'].fillna(0)
    f_ppp = f_ppp.groupby(['Country', 'Financial closure year'], as_index=False)['TotalInvestment'].sum()

    # Plot GDP per capita
    gender_stats_df = pd.read_csv(inFile_gender)
    country_list_name = gender_stats_df['Country Name'][gender_stats_df['Country Code'].isin(country_list)]
    country_list_name = country_list_name.unique()
    dataset_df['Country'] = f_ppp['Country'][f_ppp['Country'].isin(country_list_name)].values
    dataset_df['Financial closure year'] = f_ppp['Financial closure year'][
        f_ppp['Country'].isin(country_list_name)].values
    dataset_df['TotalInvestment'] = f_ppp['TotalInvestment'][f_ppp['Country'].isin(country_list_name)].values

    female_stats_list = genderFilteredByIndicator(inFile_gender, str(2000), str(2017), indicator_female, 1)
    male_stats_list = genderFilteredByIndicator(inFile_gender, str(2000), str(2017), indicator_male, 1)

    plot_scatter.plotScatterMultiAxisY(list(range(2000, 2018)), country_list_name, female_stats_list, male_stats_list, dataset_df, y_axis_label_1, y_axis_label_2)
    # print(dataset_df['Country'])
    # print(dataset_df['Financial closure year'])
    # print(dataset_df['TotalInvestment'])
    # filter based on indicator
    # gender_stats_byRow_df = gender_stats_df[(gender_stats_df["Country Code"].isin(country_list)) & (
    #         gender_stats_df["Indicator Code"] == indicator)]
    # gender_stats_byRow_df = gender_stats_byRow_df.fillna(0)
    # gender_stats_byCol_list = gender_stats_byRow_df.loc[:, '2000':'2017'].values.tolist()
    # # call plot function to create graph


# Filter data and trigger multi axis scatter plot
def plotGdpAndNFI(inFile_nfi, inFile_gender, indicator_gdp, y_axis_label_1, y_axis_label_2):
    dataset_df = pd.DataFrame()

    # filter our and group by values from PPP file
    f_nfi = pd.read_excel(inFile_nfi)
    f_nfi = f_nfi.convert_objects(convert_numeric=True)
    f_nfi['nfi'] = f_nfi['nfi'].fillna(0)
    # f_ppp = f_ppp.groupby(['Country', 'Financial closure year'], as_index=False)['TotalInvestment'].sum()

    # Plot GDP per capita
    country_df = pd.read_csv('../resources/Gender_StatsCountry.csv')
    country_list_name = country_df['Short Name'][country_df['Country Code'].isin(country_list)]
    country_list_name = country_list_name.unique()
    dataset_df['country'] = f_nfi['country'][f_nfi['country'].isin(country_list_name)].values
    dataset_df['year'] = f_nfi['year'][f_nfi['country'].isin(country_list_name)].values
    dataset_df['nfi'] = f_nfi['nfi'][f_nfi['country'].isin(country_list_name)].values

    gdp_rate_list = genderFilteredByIndicator(inFile_gender, str(2006), str(2017), indicator_gdp, 1)

    plot_scatter.plotScatterMultiAxisY_temp(list(range(2006, 2018)), country_list_name, gdp_rate_list,
                                       dataset_df, y_axis_label_1, y_axis_label_2)

'''
The core function to point files and filtering criteria from input files (csv, excel)
and trigger graph plots.'''
def visualize():
    gender_stats_inFile = "../resources/Gender_StatsData.csv"
    gender_stats_outFile = "../target/filtered_gender_stats.csv"
    filterGenderStatsFile(gender_stats_inFile, gender_stats_outFile)

    # trigger GDP per capita plot
    gdp_per_capita_indicator = "NY.GDP.PCAP.CD"
    step_data_points = 1
    y_axis_label = "GDP Per Capita in US$"
    triggerScatterPlot(gender_stats_outFile, gdp_per_capita_indicator, step_data_points, y_axis_label)

    # Trigger GDP growth rate plot
    gdp_growth_indicator = "NY.GDP.MKTP.KD.ZG"
    y_axis_label = "Annual GDP growth %"
    triggerScatterPlot(gender_stats_outFile, gdp_growth_indicator, step_data_points, y_axis_label)

    # Trigger bubble map plot based on total GDP
    gdp_indicator = "NY.GDP.MKTP.CD"
    triggerBubblePlot(gender_stats_outFile, gdp_indicator)

    # Trigger unemployment vs PPP plot
    unemp_indicator_female = "SL.UEM.TOTL.FE.ZS"
    unemp_indicator_male = "SL.UEM.TOTL.MA.ZS"
    ppp_stats_inFile = "../resources/CustomQuery-8_9_2018.xls"
    y_axis_label_1 = "% unemployment of total population"
    y_axis_label_2 = "PPP in US$ millions"
    unEmplotementAndPPP(ppp_stats_inFile, gender_stats_inFile, unemp_indicator_female, unemp_indicator_male, y_axis_label_1, y_axis_label_2)

    # Trigger GDP growth rate vs NFI plot
    nfi_stats_inFile = "../resources/nfi_simple_0.xls"
    y_axis_label_1 = "Annual GDP growth %"
    y_axis_label_2 = "NFI Index"
    plotGdpAndNFI(nfi_stats_inFile, gender_stats_inFile, gdp_growth_indicator, y_axis_label_1, y_axis_label_2)


if __name__ == "__main__":
    visualize()
