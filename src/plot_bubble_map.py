import plotly.plotly as plty
import pandas as pd


def plot_bubble_map(df_gdp):
    colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","rgb(255,220,0)"]
    cities = []
    scale = 50000000000

    for color in colors:
        city = dict(
            type='scattergeo',
            locationmode='ISO-3',
            lon=df_gdp['CapitalLongitude'],
            lat=df_gdp['CapitalLatitude'],
            text=df_gdp['capital'],
            sizemode='diameter',
            marker=dict(
                size=df_gdp['gdp_total'] / scale,
                color=color,
                line=dict(width=2, color='black')
            ),
            name='Some Name')
        cities.append(city)

    layout = dict(
        title='2014 US city populations<br>(Click legend to toggle traces)',
        showlegend=True,
        geo=dict(
            scope='world',
            projection=dict(type='robinson'),
            showland=True,
            landcolor='rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

    fig = dict(data=cities, layout=layout)
    url = plty.plot(fig, validate=False, filename='d3-bubble-map-populations')
    print(url)
