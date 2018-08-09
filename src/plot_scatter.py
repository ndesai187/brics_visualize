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




