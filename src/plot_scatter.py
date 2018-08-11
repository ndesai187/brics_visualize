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


def createDataframeMultiAxis_temp(years_x_axis, country_list, x_nfi_df):
    # adding NaN value for missing years
    mux = pd.MultiIndex.from_product([x_nfi_df['country'].unique(), range(x_nfi_df['year'].min(),
                                                                          x_nfi_df['year'].max() + 1)],
                                     names=['country', 'year'])
    x_nfi_df = x_nfi_df.set_index(['country', 'year']).reindex(mux).reset_index()
    # replace NaN with 0
    x_nfi_df = x_nfi_df.fillna(0)

    asList_nfi = x_nfi_df['nfi'][x_nfi_df['year'].isin(years_x_axis) & (x_nfi_df['country'].isin(country_list))].groupby(x_nfi_df['country']).apply(list)
    return asList_nfi
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


def plotScatterMultiAxisY(years_axis, country_list, female_data_y_axis, male_data_y_axis, ppp_df, y_axis_label_1, y_axis_label_2):
    asList_PPP = createDataframeMultiAxis(years_axis, country_list, ppp_df)
    image_name_reference = "gender_based_unemp_vs_PPP"
    palette = plt.get_cmap('Set1')

    for i in range(0, len(country_list)):
        fig = plt.figure()

        ax1 = fig.add_subplot(111)
        lns1 = ax1.plot(years_axis, female_data_y_axis[i], marker='', color=palette(0), linewidth=1, alpha=0.9, label="Female unemployment %")
        lns2 = ax1.plot(years_axis, male_data_y_axis[i], marker='', color=palette(1), linewidth=1, alpha=0.9, label="male unemployment %")
        ax2 = ax1.twinx()
        lns3 = ax2.plot(years_axis, asList_PPP[i], marker='', color=palette(2), linewidth=1, alpha=0.9, label="PPP investments")

        # Add legend and labels
        ax2.grid()
        ax1.set_ylabel(y_axis_label_1)
        ax2.set_ylabel(y_axis_label_2)
        lns = lns1 + lns2 + lns3
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc=0)
        ax2.set_xlim(2000, 2017)
        plt.title(country_list[i])

        plt.savefig('../target/{}_{}.png'.format(image_name_reference, i))
        i += 1
        plt.clf()
        plt.cla()
        plt.close()


def plotScatterMultiAxisY_temp(years_axis, country_list, gdp_rate_lst, nfi_df, y_axis_label_1, y_axis_label_2):
    asList_nfi = createDataframeMultiAxis_temp(years_axis, country_list, nfi_df)
    image_name_reference = "gdp_vs_nfi"
    palette = plt.get_cmap('Set1')

    for i in range(0, len(country_list)):
        fig = plt.figure()

        ax1 = fig.add_subplot(111)
        lns1 = ax1.plot(years_axis, gdp_rate_lst[i], marker='', color=palette(0), linewidth=1, alpha=0.9, label=y_axis_label_1)
        ax2 = ax1.twinx()
        lns2 = ax2.plot(years_axis, asList_nfi[i], marker='', color=palette(1), linewidth=1, alpha=0.9, label=y_axis_label_2)

        # Add legend and labels
        ax2.grid()
        ax1.set_ylabel(y_axis_label_1)
        ax2.set_ylabel(y_axis_label_2)
        lns = lns1 + lns2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc=0)
        ax2.set_xlim(2006, 2017)
        plt.title(country_list[i])

        plt.savefig('../target/{}_{}.png'.format(image_name_reference, i))
        i += 1
        plt.clf()
        plt.cla()
        plt.close()
