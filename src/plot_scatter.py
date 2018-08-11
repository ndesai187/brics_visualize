import matplotlib.pyplot as plt
import pandas as pd


# data
def create_frame(years_x_axis, country_list, country_data_y_axis):
    df = pd.DataFrame({
        'year': years_x_axis,
        '{}'.format(country_list[0]): country_data_y_axis[0],
        '{}'.format(country_list[1]): country_data_y_axis[1],
        '{}'.format(country_list[2]): country_data_y_axis[2],
        '{}'.format(country_list[3]): country_data_y_axis[3],
        '{}'.format(country_list[4]): country_data_y_axis[4]
    })
    return df


def create_frame_3x(years_x_axis, country_list, country_data_y_axis, x_df):
    mux = pd.MultiIndex.from_product([x_df['Country'].unique(),range(x_df['Financial closure year'].min(), x_df['Financial closure year'].max() + 1)], names=['Country', 'Financial closure year'])

    x_df_n = x_df.set_index(['Country', 'Financial closure year']).reindex(mux).reset_index()
    print(x_df_n)
    x_df_n = x_df_n.fillna(0)
    final_list = x_df_n['TotalInvestment'][x_df_n['Financial closure year'].isin(years_x_axis) & (
        x_df_n['Country'].isin(country_list))].groupby(x_df_n['Country']).apply(list)
    print("printing final list")
    print(final_list)
    for l in final_list:
        print(len(l))
    return final_list


def plot_graph(years_x_axis, country_list, country_data_y_axis, output_png):
    plot_frame = create_frame(years_x_axis, country_list, country_data_y_axis)
    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot
    num = 0
    for column in plot_frame.drop('year', axis=1):
        num += 1
        plt.plot(plot_frame['year'], plot_frame[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)

    # Add legend
    plt.legend(loc=2, ncol=2)
    plt.savefig('../target/{}.png'.format(output_png))
    plt.clf()
    plt.cla()
    plt.close()


def plot_3x_graph(years_axis, country_list, country_data_y_axis, ppp_df):
    final_list = create_frame_3x(years_axis, country_list, country_data_y_axis,ppp_df)
    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    i=0
    for country in country_list:
        # fig = plt.figure()
        # ax1 = fig.add_subplot(111)
        # ax1.plot(years_axis, country_data_y_axis[i], marker='', color=palette(i), linewidth=1, alpha=0.9, label=country)

        # Add legend
        # ax1.legend(loc=2, ncol=2)
        # ax1.savefig('../target/{}.png'.format(i))

        # ax2 = ax1.twinx()
        # ax2.plot(years_axis, final_list[i], marker='', color=palette(i), linewidth=1, alpha=0.9, label=country)

        # Add legend

        i += 1
        plt.clf()
        plt.cla()
        plt.close()

