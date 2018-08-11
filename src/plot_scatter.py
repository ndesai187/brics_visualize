import matplotlib.pyplot as plt
import pandas as pd


# data
def createDataFrame(years_x_axis, country_list, country_data_y_axis):
    df = pd.DataFrame({
        'year': years_x_axis,
        '{}'.format(country_list[0]): country_data_y_axis[0],
        '{}'.format(country_list[1]): country_data_y_axis[1],
        '{}'.format(country_list[2]): country_data_y_axis[2],
        '{}'.format(country_list[3]): country_data_y_axis[3],
        '{}'.format(country_list[4]): country_data_y_axis[4]
    })
    return df


def createDataframeMultiAxis(years_x_axis, country_list, x_PPP_df):
    # adding NaN value for missing years
    mux = pd.MultiIndex.from_product([x_PPP_df['Country'].unique(), range(x_PPP_df['Financial closure year'].min(),
                                                                          x_PPP_df['Financial closure year'].max() + 1)],
                                     names=['Country', 'Financial closure year'])
    x_PPP_df = x_PPP_df.set_index(['Country', 'Financial closure year']).reindex(mux).reset_index()
    # replace NaN with 0
    x_PPP_df = x_PPP_df.fillna(0)

    asList_PPP = x_PPP_df['TotalInvestment'][x_PPP_df['Financial closure year'].isin(years_x_axis) & (
        x_PPP_df['Country'].isin(country_list))].groupby(x_PPP_df['Country']).apply(list)
    return asList_PPP
    # print("printing final list")
    # print(asList_PPP[3])


def plotSimpleScatterGraph(years_x_axis, country_list, country_data_y_axis, y_axis_label_lst, output_png):
    plot_frame = createDataFrame(years_x_axis, country_list, country_data_y_axis)
    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot
    num = 0
    for column in plot_frame.drop('year', axis=1):
        num += 1
        plt.plot(plot_frame['year'], plot_frame[column], marker='', color=palette(num), linewidth=1, alpha=0.9,
                 label=column)

    # Add legend
    plt.legend(loc=2, ncol=2)
    plt.ylabel(y_axis_label_lst)
    plt.savefig('../target/{}.png'.format(output_png))
    plt.clf()
    plt.cla()
    plt.close()


def plotScatterMultiAxisY(years_axis, country_list, female_data_y_axis, male_data_y_axis, ppp_df):
    asList_PPP = createDataframeMultiAxis(years_axis, country_list, ppp_df)
    image_name_reference = "gender_based_unemp_vs_PPP"

    # print("\nPPP List:\n")
    # print(type(asList_PPP[0]))
    # print(len(asList_PPP))
    # print(asList_PPP)
    # print("\nFemale List:\n")
    # print(type(female_data_y_axis))
    # print(len(female_data_y_axis))
    # print(female_data_y_axis)
    # print("\nmale List:\n")
    # print(type(male_data_y_axis))
    # print(len(male_data_y_axis))
    # print(male_data_y_axis)
    # print(country_list)
    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    i = 0
    for country in country_list:
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(years_axis, female_data_y_axis[i], marker='', color=palette(0), linewidth=1, alpha=0.9, label=country)
        ax1.plot(years_axis, male_data_y_axis[i], marker='', color=palette(1), linewidth=1, alpha=0.9, label=country)

        # Add legend
        # ax1.legend(loc=2, ncol=2)
        # ax1.savefig('../target/{}.png'.format(i))

        ax2 = ax1.twinx()
        ax2.plot(years_axis, asList_PPP[i], marker='', color=palette(2), linewidth=1, alpha=0.9, label=country)
        plt.savefig('../target/{}_{}.png'.format(image_name_reference,i))
        # Add legend

        i += 1
        plt.clf()
        plt.cla()
        plt.close()
