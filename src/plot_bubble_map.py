import plotly.offline as plty


def plotBubbleMap(df_gdp):
    colors = ["rgb(0,116,217)", "rgb(255,65,54)", "rgb(133,20,75)", "rgb(255,133,27)", "rgb(255,220,0)"]
    cities = []
    df_gdp['text'] = df_gdp['capital'] + '<br>GDP ' + (df_gdp['gdp_total'] / 1e12).round(4).astype(str) + ' Trillion'
    scale = 90000000000

    for i in range(0, len(df_gdp['country_code'])):
        df_sub = df_gdp[i:i+1]

        city = dict(
            type='scattergeo',
            locationmode='ISO-3',
            lon=df_sub['CapitalLongitude'],
            lat=df_sub['CapitalLatitude'],
            text=df_sub['text'][i],
            sizemode='diameter',
            marker=dict(
                size=df_sub['gdp_total'] / scale,
                color=colors[i],
                # color=df['colors'][i],
                line=dict(width=2, color='black')
            ),
            name=df_gdp['country_code'][i])
        cities.append(city)

    layout = dict(
        title='Total GDP by country for year 2017<br>(Click legend to toggle traces)',
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
    fig = dict(data=cities, layout=layout, auto_open=False)
    plty.plot(fig, validate=False, filename='../target/d3-bubble-map-gdp.html', auto_open=False)

    # city = dict(
    #     type='scattergeo',
    #     locationmode='ISO-3',
    #     lon=df_gdp['CapitalLongitude'],
    #     lat=df_gdp['CapitalLatitude'],
    #     # text=df_gdp['capital'],
    #     text=df['text'],
    #     sizemode='diameter',
    #     marker=dict(
    #         size=df_gdp['gdp_total'] / scale,
    #         # color=colors[i],
    #         color=df['colors'],
    #         line=dict(width=2, color='black')
    #     ),
    #     name=df_gdp['country_code'])
    # print(city)
    # cities.append(city)

    # city = dict(
    #     type='scattergeo',
    #     locationmode='ISO-3',
    #     lon=df_gdp['CapitalLongitude'],
    #     lat=df_gdp['CapitalLatitude'],
    #     # text=df_gdp['capital'],
    #     text=df['text'],
    #     sizemode='diameter',
    #     marker=dict(
    #         size=df_gdp['gdp_total'] / scale,
    #         # color=colors[i],
    #         color=df['colors'],
    #         line=dict(width=2, color='black')
    #     ),
    #     name=df_gdp['country_code'])
    # print(city)
    # cities.append(city)

    # url = plty.plot(fig, validate=False, filename='../target/d3-bubble-map-gdp.html', auto_open=False)
    # tls.get_embed(url)
    # plty.image.save_as(fig, filename="../target/abcd.png")
    # url = plty.plot(fig, validate=False, filename='d3-bubble-map-populations.png', image='png', format='png')
    # print(url)
