# -*- coding: utf-8 -*-

# Dash and Plotly
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools

import pandas as pd
import numpy as np
import math
import json

from app import df
#from app import encoded_image5, encoded_image6
FREEDOM_COLORS = [["#4a386e", "#9370DB", "#b39be6", '#c9b8ed'], ["#806200", "#FFC300", "#ffd54d", '#ffe180'], ["#086405", "#10C80A", "#58d954", '#88e485']]

# ----- configurable variables -----
PLOT_HEIGHT = 400
MARKER_SIZE = 10
PLOT_COLORS = {"country": "#FF8A5B",
               "region": "#38C0E1",
               "men": "#F3CA40",
               "women": "#6A5ACD",
               "urban": "#EDC79B",
               "rural": "#63A375",
               "title": "#38C0E1"}


# ----- general utility functions -----

def generate_table(df_table, title=None, description=None):
    """
    Generates a Dash table html component from the df_table DataFrame. The DataFrame's column names are used as headers.
    generate_table() will return a div containing first a div with class table-title for the title, and then the table
    itself. If title is passed, a Dash span component containing the title string will be added to the title div. If
    description is passed, a Dash img component of the info icon will be added to the title div. The description will
    appear when the cursor hovers over the info icon. If neither title nor description are passed, the title div will be
    empty but will still be included in the returned div for consistencies sake.

    :param df_table: DataFrame containing data to be formatted. Headers will be used as header names for the table.
    :param title: (optional) the title string to add above the table
    :param description: (optional) the description to display on cursor hover
    :return: An html.Div component with an html.Div and an html.Table as children
    """

    # construct table row for headers
    headers = html.Tr(
        children=[html.Th(col) for col in list(df_table.columns)]
    )

    # append table rows containing elements to headers
    table_children = [headers]
    for i in range(len(df_table)):
        row = df_table.loc[i]
        elem_list = []
        for elem in row:
            elem_list.append(html.Td(elem))
        table_children.append(html.Tr(elem_list))

    table = html.Table(
        children=html.Tbody(table_children)
    )

    # create an empty list for children of title div
    title_children = []

    # add title span to title children list if title is passed
    if title is not None:
        title_children.append(html.Span(title))

    # add info icon to title div if description is passed
    if description is not None:
        title_children.append(
            html.Img(src='https://s3-us-west-2.amazonaws.com/da2i/Images/Info_Icon_Purple.png',
                     title=description)
        )

    # create div for title
    title_div = html.Div(
        className="table-title",
        children=title_children
    )

    # wrap table in div
    table_div = html.Div(
        children=[title_div, table]
    )

    return table_div


def generate_dummy_table():
    df_table = pd.DataFrame({"Column 1": ["Value 1"],
                             "Column 2": ["Value 2"],
                             "Column 3": ["Value 3"],
                             })
    return generate_table(df_table,
                          title="Table Title",
                          description="Table description")


def generate_sparklines_slider_bar_chart(selected_country, indicator, title, categories=None):
    """
    generates a sparklines style (compact) bar chart for the selected country and indicator.

    :param selected_country: selected country
    :param indicator: name of indicator
    :param title: title of the bar chart
    :param categories: a list of dicts defining the "name", "range", and "color" of categorical variables.
    EX: [{"name": "category 1", "range": [lower_bound, upper_bound], "color": "#0000FF"}, ... ]

    :return: sparklines bar chart
    """

    #filtered data
    df_filtered = df[df["Country"] == selected_country]
    df_filtered = df_filtered[df_filtered["Name"] == indicator] # filtered by selected country and indicator
    df_filtered = df_filtered.dropna(axis="index",subset=["value"]) # drop rows with missing indicator values

    df_filtered.sort_values('Year',inplace=True)
    values = df_filtered['value'].tail(1).tolist()[0] if len(df_filtered) != 0 else 'NA'
    years = int(df_filtered['Year'].tail(1).tolist()[0]) if len(df_filtered) != 0 else 'NA'

    if years == 'NA':
        yrs_range = [2018,2018.5]
    else:
        yrs_range = [years,years+0.5]

    if values != 'NA' and indicator == "FitW.total.aggregate.score":
        if values >= 70:
            colors = '#10C80A'
        elif values >= 30:
            colors = '#FFC300'
        else:
            colors = '#9370DB'
    elif values != 'NA' and indicator == "FotN":
        if values >= 70:
            
            colors = '#10C80A'
        elif values >= 40:
            colors = '#FFC300'
        else:
            colors = '#9370DB'
    elif values != 'NA' and indicator == "GII":
        if values >= 0.7:
            colors = '#FF8A5B'
        elif values >= 0.3:
            colors = '#FF8A5B'
        else:
            colors = '#FF8A5B'
    else:
        colors = "#000000"
    

    
    trace = go.Bar( y = [years],
                    x = [values],
                    orientation = 'h',
                    width = 0.5,
                    marker = {'color': colors},
                        )
    if indicator == 'FitW.total.aggregate.score' or indicator == 'GII':
        layout = go.Layout( title = title,
                        xaxis=dict(showgrid=False,
                                        showline=True,
                                        showticklabels=False,
                                        zeroline=False,
                                        tickfont=dict(family='Raleway',size=14),
                                        range=[0,1] if indicator == 'GII' else [0,100]
                                    ),
                        yaxis=dict(showgrid=False,
                                   showline=False,
                                   showticklabels=False,
                                   zeroline=False,
                                   range= yrs_range
                                   ),
                        height = 150,
                        width=500,
                        margin=go.layout.Margin(
                                                l=40,
                                                #r=50,
                                                #b=0,
                                                t=0,
                                                #pad=4
                                              ),
                        annotations=[
                                        dict(
                                            text="NO DATA AVAILABLE",
                                            showarrow=False,
                                            visible=True if (len(df_filtered) == 0) else False
                                        ),
                                        dict(x=0.0,
                                            y=-.85,
                                            xref='x',
                                            axref='x',
                                            yref='paper',
                                            ayref='pixel',
                                            xanchor='left',
                                            align='left',
                                            text='Source: ' + df.loc[df['Name'] == indicator, 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                                              df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                                            showarrow=False,
                                            font=dict(family='Raleway',size=14)
                                          ),
                                         dict(
                                             text="More Equal (0)" if indicator == 'GII' else "Least free (0)",
                                             x=0,
                                             xanchor="left",
                                             y=-0.00,
                                             yanchor="top",
                                             xref='x',
                                             yref='paper',
                                             showarrow=False,
                                             font=dict(family='Raleway',size=13, color='blue')
                                          ),
                                        dict(
                                            text="Less Equal (1)" if indicator == 'GII' else "Most free (100)",
                                            x=1 if indicator == 'GII' else 100,
                                            xanchor="right",
                                            y=-0.00,
                                            yanchor="top",
                                            xref='x',
                                            yref='paper',
                                            showarrow=False,
                                            font=dict(family='Raleway',size=13,color='blue')
                                        ),]
                        )
    else:
                layout = go.Layout( title = title,
                        xaxis=dict(showgrid=False,
                                        showline=True,
                                        showticklabels=False,
                                        zeroline=False,
                                        tickfont=dict(family='Raleway',size=14),
                                        range=[0,100]
                                    ),
                        yaxis=dict(showgrid=False,
                                   showline=False,
                                   showticklabels=False,
                                   zeroline=False,
                                   range= yrs_range
                                   ),
                        height = 150,
                        width=500,
                        margin=go.layout.Margin(
                                                l=40,
                                                #r=50,
                                                #b=100,
                                                t=0,
                                                #pad=4
                                              ),
                        annotations=[
                                        dict(
                                            text="NO DATA AVAILABLE",
                                            showarrow=False,
                                            visible=True if (len(df_filtered) == 0) else False
                                        ),
                                        dict(x=0.0,
                                            y=-.85,
                                            xref='x',
                                            axref='x',
                                            yref='paper',
                                            ayref='pixel',
                                            xanchor='left',
                                            align='left',
text='Source: ' + df.loc[df['Name'] == indicator, 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                                              df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                                            showarrow=False,
                                            font=dict(family='Raleway',size=14)
                                          ),
                                         dict(
                                             text="Least free (0)",
                                             x=0,
                                             xanchor="left",
                                             y=-0.00,
                                             yanchor="top",
                                             xref='x',
                                             yref='paper',
                                             showarrow=False,
                                             font=dict(family='Raleway',size=13, color='blue')
                                          ),
                                        dict(
                                            text="Most free (100)",
                                            x=100,
                                            xanchor="right",
                                            y=-0.00,
                                            yanchor="top",
                                            xref='x',
                                            yref='paper',
                                            showarrow=False,
                                            font=dict(family='Raleway',size=13,color='blue')
                                        ),]
                        )
    return go.Figure(data=[trace],layout=layout)


def generate_sparklines_bar_chart(selected_country, indicator, title, categories=None):
    """
    generates a sparklines style (compact) bar chart for the selected country and indicator.

    :param selected_country: selected country
    :param indicator: name of indicator
    :param title: title of the bar chart
    :param categories: a list of dicts defining the "name", "range", and "color" of categorical variables.
    EX: [{"name": "category 1", "range": [lower_bound, upper_bound], "color": "#0000FF"}, ... ]

    :return: sparklines bar chart
    """

    # filter data
    df_filtered = df[df["Country"] == selected_country]  # by selected country
    df_filtered = df_filtered[df_filtered["Name"] == indicator]  # by indicator
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])  # drop rows with missing indicator values

    values = list(df_filtered["value"])
    years = list(df_filtered["Year"])

    trace = go.Bar(
        x=years,
        y=values,
    )

    layout = go.Layout(
        
        
        annotations=[
            dict(
                text='Source: ' + df.loc[df['Name'] == indicator, 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                    df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                showarrow=False,
                x=0.0,
                y=-.65,
                yref='paper',
                xref='paper',
                # axref='x',
                font=dict(family='Raleway',size=14),


                align='left',
            ),
         
            dict(
                text="NO DATA AVAILABLE",
                showarrow=False,
                visible=True if (len(df_filtered) == 0) else False
            ),
        ],
        title={'text': title, 'xanchor': 'center', 'x':0.5,},
        titlefont=dict(color=PLOT_COLORS["title"],family='Raleway',size=20),
        height=275,
        width=550,
        showlegend = False,
         margin=dict(
                    l=50,
                    r=50,
                    b=75,
                    t=80,
                    pad=10
                ),
        xaxis=dict(
            #tickmode="auto",
            tickfont=dict(family='Raleway',size=14),
            range=[2009.5,2018.5] if indicator == 'FitW.total.aggregate.score' else [2010.5,2018.5],
            side="top"
        ),
        yaxis=dict(
            #tickmode="auto",
            tickfont=dict(family='Raleway',size=14),
            range=[1,0] if indicator == 'GII' else [100,0]
        )
    )

    if categories is not None:
        # create colorscale for bars
        colorscale = []
        for cat in categories:
            colorscale.append([cat["range"][0] / (1 if indicator == 'GII' else 100), cat["color"]])
            colorscale.append([cat["range"][1] / (1 if indicator == 'GII' else 100), cat["color"]])

        trace["marker"]["cmin"] = categories[0]["range"][0]  # set the minimum value of the colorbar
        trace["marker"]["cmax"] = categories[-1]["range"][1]  # set the maximum value of the colorbar
        trace["marker"]["color"] = values  # color bars based on bar height(value)
        trace["marker"]["colorscale"] = colorscale  # set colorscale
        trace["marker"]["showscale"] = True  if indicator != "GII" else False # display colorbar
        trace["marker"]["colorbar"] = dict(  # format colorbar
            tickmode='array',
            tickvals=[cat["range"][1] for cat in categories],
            ticktext=[cat["name"] for cat in categories],
            ticks='outside',
            thickness = 20
        )

    # a figure combining data and layout
    return go.Figure(data=[trace], layout=layout)


# ----- layout generation functions -----

def generate_country_profile(description):
    """
    Generates country profile layout

    :return: country profile layout
    """

    return html.Div(
        id='country-profile',
        children=[

            # ----- country profile title -----
            html.H4('COUNTRY PROFILE'),

            # ----- country profile sections -----
            html.Div(
                children=[

                    # ----- country population -----
                    html.Div(
                        className='country-profile-section',
                        children=[
                            html.Div(
                                children=[

                                    # ----- title -----
                                    html.Span(
                                        className="title",
                                        children='Population'
                                    ),
                                ]
                            ),

                            # ----- value -----
                            html.Div(
                                html.Span(
                                    className="value",
                                    id='country-population-value'),
                            )
                        ]
                    ),

                    # ----- country income group -----
                    html.Div(
                        className='country-profile-section',
                        children=[
                            html.Div(
                                children=[

                                    # ----- title -----
                                    html.Span(
                                        className="title",
                                        children='Income Group'
                                    ),
                                ]
                            ),

                            # ----- value -----
                            html.Div(
                                html.Span(
                                    className="value",
                                    id='country-income-group'),
                            )
                        ]
                    ),

                    # ----- UN sub region group -----
                    html.Div(
                        className='country-profile-section',
                        children=[
                            html.Div(
                                children=[

                                    # ----- title -----
                                    html.Span(
                                        className="title",
                                        children='UN Sub Region'
                                    ),

                                    # ----- (optional) info icon -----
                                    html.Img(
                                        src='https://s3-us-west-2.amazonaws.com/da2i/Images/Info_Icon_Purple.png',title=', '.join(description)
                                    )
                                ]
                            ),

                            # ----- value -----
                            html.Div(
                                html.Span(
                                    className="value",
                                    id='country-sub-region'),
                            )
                        ]
                    )
                ]
            )
        ]
    )

def generate_quick_look_layout(dashboard, sections):
    """
    This function generates a quick look layout with the number of sections specified by the sections parameter. Section ids are of
    the form <dashboard>-quick-look-section-<section number>. Section numbers are indexed from 1.

    :param dashboard: name of the dashboard for which the quick look layout is being generated
    :param sections: the number of sections to be generated
    :return: quick look layout
    """
    quick_look = html.Div(
        className='quick-look',
        children=[

            # ----- title -----
            html.Div(
                className='quick-look-title',
                children=[
                    html.Span('QUICK LOOK'),
                    html.Img(
                        src='https://s3-us-west-2.amazonaws.com/da2i/Images/Spyglass_Icon.png',
                    ),
                ],
            )
        ])

    section_divs = []

    for i in range(sections):
        temp_div = html.Div(
            className='quick-look-section',
            id='{}-quick-look-section-{}'.format(dashboard, i + 1)
        )
        section_divs.append(temp_div)

    quick_look.children.extend(section_divs)
    return quick_look


# ----- connectivity helper functions -----

# -- misc --

# TODO: Remove style from generateTable()
def generateConnectivityTable(indicator, rank, pct_change, selected_country, max_year, name, description):
    """
    This function generates a Table component containing the passed values. It was originally named generateTable().
    It is only used to generate tables in the connectivity dashboard.

    :return: Table component
    """
    return html.Table(
        # Header

        [html.Tr([html.Th('Indicator Name', style={'textAlign': 'left'}),
                  html.Th('', style={'padding': '0 0 0 18px', 'textAlign': 'left'}),
                  html.Th(selected_country, style={'padding': '0 0 0 8px', 'textAlign': 'right'}),
                  html.Th('Year', style={'padding': '0 0 0 8px', 'textAlign': 'right'}),
                  html.Th('% change', style={'padding': '0 0 0 8px', 'textAlign': 'right'})],
                 style={'borderTop': '1px solid light-grey', 'fontSize': '16px', 'color': 'grey'})] +

        # Body
        [html.Tr([html.Td(name,
                          style={'textAlign': 'left', 'fontSize': '16px'}),
                  html.Td(html.Div(html.Img(src='https://s3-us-west-2.amazonaws.com/da2i/Info_Icon_Purple.png',
                                            style={'width': '20px', 'marginTop': '2px'}),
                                   title=description),
                          style={'float': 'left'}),
                  html.Td(str(indicator),
                          style={'textAlign': 'right', 'fontSize': '16px'}),
                  # html.Td(str(indicator) + ' (' + str(max_year) + ')',
                  # style={'textAlign': 'right','fontSize':'16px'}),
                  # html.Td(str(rank),
                  # style={'textAlign': 'right','fontSize':'16px'}),
                  html.Td(str(max_year),
                          style={'textAlign': 'right', 'fontSize': '16px'}),
                  html.Td(str(pct_change),
                          style={'textAlign': 'right', 'fontSize': '16px'})],
                 style={'borderTop': '1px solid light-grey', 'border-bottom': '1px solid light-grey',
                        'color': '#38C0E1'}),

         ],
        style={'width': '100%'}
    )


def getCountryData(selected_country, indicator):
    """
    This function filters data by selected_country and indicator and return NaN if none available.

    :param selected_country: the country to filter by
    :param indicator: indicator to filter by
    :return: DataFrame filtered by selected_country
    """
    filtered_df = df.loc[(df['Country'] == selected_country) & (df['Name'] == indicator) & (df['Year'] >= 2006)]
    if (filtered_df.shape[0] == 0):
        filtered_df['Year'] = range(2006, 2017)
        filtered_df['value'] = np.nan
        filtered_df['Country'] = selected_country
        filtered_df['Name'] = indicator
        return filtered_df
    else:
        return filtered_df


def getCountryRank(selected_country, region, indicator, ascending=True):
    """
    This function computes the rank of selected_country within its region for the specified indicator. By default, a
    country with a higher indicator value is assigned a higher rank. This behavior can be reversed by using
    ascending=False.

    :param selected_country: country for which to compute rank within region
    :param region:
    :return: rank
    """
    # get latest years data for each country in region
    rnk = df.loc[(df['Region'] == region) & (df['Name'] == indicator)]
    rnk.sort_values(['Country', 'Year'], inplace=True)
    rnk = rnk.groupby('Country').tail(1)

    if ascending is True:
        rnk.sort_values('value', ascending=False, inplace=True)
    else:
        rnk.sort_values('value', inplace=True)

    rnk['ranks'] = range(1, rnk.shape[0] + 1)

    return str(rnk.loc[rnk['Country'] == selected_country, 'ranks'].tolist()[0]) + ' of ' + str(rnk.shape[0])


def weightedAverage(region, indicator):
    """
    Computes weighted average of indicator by population for the specified region and indicator.

    :return: weighted average or NaN if no data exists
    """
    rgl = df.loc[(df['Region'] == region) & (df['Name'] == indicator)]
    ## get population data and merge in
    rgl = rgl.merge(df.loc[(df['Region'] == region) & (df['Name'] == 'population'), ['Country', 'Year', 'value']],
                    on=['Country', 'Year'],
                    how='left')
    
    rgl['population'] = rgl.groupby('Country')['value_y'].ffill()
    rgl['population'] = rgl.groupby('Country')['value_y'].bfill()

    ## compute weighted average by year
    rgl['w_value'] = rgl['value_x'] * rgl['population']

    result = rgl.groupby('Year', as_index=False).agg({'w_value': sum}).merge(rgl.groupby('Year', as_index=False).agg({'population': sum}))
    result['w_avg'] = result['w_value'] / result['population']

    return result[['Year', 'w_avg']]


# -- charts --

def generate_time_series_line_chart(selected_country, indicator, title, ylabel):
    """
    This function generates a time series line chart showing the value of the selected indicator for the selected
    country and its region over time.
    
    :param selected_country: selected country from dropdown
    :param indicator: indicator for which to plot data
    :param title: title of the plot
    :param ylabel: label of the y axis
    :return: time series line chart
    """
    # Create and style traces
    filtered_df = getCountryData(selected_country, indicator=indicator)

    # Compute regional average weighted by country population
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    regional = weightedAverage(rgn, indicator=indicator)
    maxValue = max([filtered_df['value'].max(), regional['w_avg'].max()]) if len(filtered_df) != 0 else 'NA'


    sourceText = 'Source: ' + df.loc[df['Name'] == indicator, 'Source'].tail(1).tolist()[0] + ' (' + str(int(df.loc[df['Name'] == indicator, 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington'

    return {
        'data': [
            go.Scatter(  # Country data
                x=filtered_df['Year'],
                y=filtered_df['value'],
                text=filtered_df['Country'],
                name=filtered_df['Country'].tolist()[0],
                line=dict(
                    color=(PLOT_COLORS["country"]),
                    width=4),
                marker=dict(
                    size=MARKER_SIZE
                )
            ),
            go.Scatter(  # Regional average
                x=regional['Year'],
                y=regional['w_avg'],
                text=rgn,
                name=rgn,
                line=dict(
                    color=(PLOT_COLORS["region"]),
                    width=4),
                marker=dict(
                    size=MARKER_SIZE
                )
            )
        ],

        ## Edit the layout
        'layout': go.Layout(
            title=title, titlefont=dict(size=20, color=PLOT_COLORS["title"], family='Raleway'),
            font=dict(family='Raleway', size=13),
            xaxis=dict(title='',
                       range=[2005.5, 2018.5] if indicator != 'ind.internet' else [2005.5,2018.5],  # NOTE: Should this range be dynamic?
                       tick0=2006,
                       dtick=2),
            yaxis=dict(title=ylabel,
                       range=[0, 100]), #if maxValue < 100 else int(math.ceil(maxValue / 50.0)) * 50] if maxValue != 'NA' else [0,100]),
            legend=dict(x=.1,
                        y=1 if filtered_df['value'].tolist()[0] < 40 else 0.1),
            height=PLOT_HEIGHT,
            width=500,
            # paper_bgcolor='#FCFCFC',  # set figure background color
            # plot_bgcolor='#CCC',  # set plot area background color
            annotations=[dict(text="NO DATA AVAILABLE",
                         showarrow=False,
                         visible=True if (len(filtered_df) == 0) else False
                        ),
                dict(
                    x=2005.5,
                    y=-.35,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
                    text=sourceText,
                    showarrow=False,
                    font=dict(family='Raleway')
                )
            ]
        )
    }


def generate_internet_user_gender_gap_chart(selected_country):
    """
    This function generates the "internet user gender gap" chart on the connectivity dashboard.
    :param selected_country: selected country from dropdown
    :return: internet user gender gap chart
    """
    ## Create and style traces
    filtered_df = df.loc[(df.Country == selected_country) & \
                         (df['Name'].isin(['ind.internet.female', 'ind.internet.male',
                                           'Pct.internet.All.Rural', 'Pct.internet.All.Urban']))]
    filtered_df.sort_values('Year', inplace=True)
    
    ## safely pull data, planning for lots of missing
    x1 = [filtered_df.loc[filtered_df['Name'] == 'ind.internet.male', 'value'].tail(1).tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'ind.internet.male' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'ind.internet.female', 'value'].tail(1).tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'ind.internet.female' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x2 = [
        filtered_df.loc[filtered_df['Name'] == 'Pct.internet.All.Rural', 'value'].tail(1).tolist()[0] if (filtered_df.shape[
                                                                                                      0] > 0) & (
                                                                                                         'Pct.internet.All.Rural' in
                                                                                                         filtered_df[
                                                                                                             'Name'].unique()) else np.nan,
        filtered_df.loc[filtered_df['Name'] == 'Pct.internet.All.Urban', 'value'].tail(1).tolist()[0] if (filtered_df.shape[
                                                                                                      0] > 0) & (
                                                                                                         'Pct.internet.All.Urban' in
                                                                                                         filtered_df[
                                                                                                           'Name'].unique()) else np.nan]
    # Create the graph with subplots
    trace1 = go.Bar(
        x=x1,
        y=['Men  ', 'Women  '],
        orientation='h',
        opacity=0.6,
        textposition='auto',
        name='Internet use by gender',
        width=0.8, 
        marker=dict(
            color=[PLOT_COLORS["men"], PLOT_COLORS["women"]],
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,
            )
        )
    )
    trace2 = go.Bar(
        x=x2,
        y=['Rural  ', 'Urban  '],
        orientation='h',
        opacity=0.6,
        textposition='auto',
        name='Internet use by urban/rural',
        width=0.8,
        marker=dict(
            color=[PLOT_COLORS["rural"], PLOT_COLORS["urban"]],
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,

            )
        )
    )
    src_text = 'Source: International Telecommunication Union (2019)<br>Technology & Social Change Group, University of Washington'

    fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.25,subplot_titles=())
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig['layout'].update(height=400,width=500)
    fig['layout']['xaxis1'].update(range=[0, 100],tickfont=dict(family='Raleway',size=12))
    fig['layout']['yaxis1'].update(tickfont=dict(family='Raleway',size=12),linewidth=0)
    fig['layout'].update(showlegend=False, title='Who is using the internet?')
    fig['layout'].update(font=dict(size=20, family='Raleway'))
    fig['layout']['yaxis2'].update(tickfont=dict(family='Raleway',size=12))
    fig['layout']['title'].update(font=dict(family='Raleway',size=20,color=PLOT_COLORS["title"]))
    fig.update_xaxes(range=[0, 100])
    if (sum(np.isnan(x1)) < 2) & (sum(np.isnan(x2)) < 2):
        fig['layout'].update(annotations=[
            dict(x=0.5, y=-.35, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left', align='left', text=src_text,
                 showarrow=False, font=dict(family='Raleway',size=12))])
    elif (sum(np.isnan(x1)) == 2) & (sum(np.isnan(x2)) == 0):
        fig['layout'].update(annotations=[
            dict(x=0.5, y=-.35, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left', align='left', text=src_text,
                 showarrow=False, font=dict(family='Raleway',size=12)),
            dict(x=20, y=.83, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left',
                 text='NO DATA AVAILABLE', showarrow=False,font=dict(family='Raleway',size=8))])
    elif (sum(np.isnan(x1)) == 0) & (sum(np.isnan(x2)) == 2):
        fig['layout'].update(annotations=[
            dict(x=0.5, y=-.35, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left', align='left', text=src_text,
                 showarrow=False, font=dict(family='Raleway',size=12)),
            dict(x=20, y=.17, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left',
                 text='NO DATA AVAILABLE', showarrow=False, font=dict(family='Raleway',size=12))])
    else:
        fig['layout'].update(annotations=[
            dict(x=0.5, y=-.35, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left', align='left', text=src_text,
                 showarrow=False, font=dict(family='Raleway',size=12)),
            dict(x=20, y=.17, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left',
                 text='NO DATA AVAILABLE', showarrow=False, font=dict(family='Raleway')),
            dict(x=20, y=.83, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left',
                 text='NO DATA AVAILABLE', showarrow=False, font=dict(family='Raleway'))])
    return fig


def generate_mobile_broadband_cost_pie_chart(selected_country):
    pcolors = ['#ff8a5b', '#38C0E1']
    cost = df.loc[(df.Country == selected_country) & (df.Name == 'mobile.broadband.cost')]
    cost.sort_values('Year', inplace=True)

    if len(cost) != 0:
        cost = round(cost['value'].iloc[-1], 2)
        gni = 100 - cost if cost < 100 else 0
    else:
        cost = 'NA'
        gni = 'NA'

    if cost != 'NA':
        return {'data': [go.Pie(labels=["Monthly income spent on Mobile Broadband", "Proportion of remaining income"],
                            values=[cost, gni],
                            hoverinfo='label+percent',
                            textinfo='none',
							textfont=dict(size=14,family='Raleway'),
                            marker=dict(colors=pcolors,
                                        line=dict(color='#000000', width=0)), hole=.7, pull=[0.1, 0])],
            'layout': {'fill': '#ff8a5b',
                       'title': 'What percent of a person’s monthly income <br> is needed to pay for mobile broadband services?',
                       'titlefont': {'size': '20', 'color': PLOT_COLORS["title"], 'family': 'Raleway'},
                       "height": "450",
                       "legend": {"x": "14","y":"-0.15"},
                       "width": "500",
                       "font": {"size": "14","family":"Raleway"},
					   "insidetextfont":{"size":"12","family":"Raleway"},
                    #    "margin": {"b" : "500"},
                       "annotations": [
                           {
                               "showarrow": False,
                               "font": {"family":"Raleway"},
                               "align": "left",
                               "text": 'Source: ' +
                                       str(df.loc[df['Name'] == 'mobile.broadband.cost', 'Source'].tail(1).tolist()[
                                           0]) + ' (' + str(int(df.loc[df['Name'] == 'mobile.broadband.cost', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                               "x": 0.00,
                               "y": -0.3

                           }
                       ]}
            }
    else:
        return {'data': [go.Pie(labels=["Monthly income spent on Mobile Broadband", "Proportion of remaining income"],
                            values=[0,0],
                            hoverinfo='label+percent',
                            textinfo='none',
			    textfont=dict(size=14,family='Raleway'),
                            marker=dict(colors=pcolors,
                                        line=dict(color='#000000', width=0)), hole=.7, pull=[0.1, 0])],
            'layout': {'fill': '#ff8a5b',
                       'title': 'What percent of a person’s monthly income is needed to pay <br>for mobile broadband services?',
                       'titlefont': {'size': '20', 'color': PLOT_COLORS["title"], 'family': 'Raleway'},
                       "height": "450",
                       "legend": {"x": "14","y":"-0.15"},
                       "width": "650",
                       "font": {"size": "14","family":"Raleway"},
					   "insidetextfont":{"size":"12","family":"Raleway"},
                       "annotations": [
                           {
                               "showarrow": False,
                               "font": {"family":"Raleway","size":"16"},
                               "text": 'NO DATA AVAILABLE',
                               "visible": True if cost == 'NA' else False,
                               "x": 0.5,
                               "y": 0.5

                           },
                           {
                               "showarrow": False,
                               "font": {"family":"Raleway"},
                               "text": 'Source: International Telecommunication Union (2019)<br>Technology & Social Change Group, University of Washington',
                               "x": 0.00,
                               "y": -0.3

                           }
                       ]}
            }
        

    # -- tables --


def generate_most_recent_value_table(selected_country, indicator, indicator_name, format_as_rate=False):
    """
    Generates tables for all but "internet user gender gap" table on the connectivity dashboard.

    :param selected_country: selected country from dropdown
    :param indicator: indicator for which to generate table
    :param indicator_name: Name of the indicator to display in table
    :param format_as_rate: boolean to format as <value>/100 instead of as percent
    :return: most recent value table
    """

    # Filter data by selected_country and indicator, then sort by year
    ind_internet = df.loc[(df.Country == selected_country) & (df.Name == indicator)]
    ind_internet.sort_values('Year', inplace=True)

    if (len(ind_internet) == 0):
        return ""

    # find most recent year for which there is data
    max_year = ind_internet['Year'].tail(1).tolist()[0] if len(ind_internet) != 0 else 'NA'

    # get region of selected_country
    region = df.loc[df.Country == selected_country, 'Region'].tolist()[0] if len(ind_internet) != 0 else 'NA'

    # compute percent change
    val1 = ind_internet['value'].tail(1).tolist()[0] if len(ind_internet) != 0 else 'NA'
    val2 = ind_internet['value'].tail(2).head(1).tolist()[0] if len(ind_internet) != 0 else 'NA'
    if indicator == 'GII':
        pctChange = round(((val1 - val2) / val2) * 100, 3) if len(ind_internet) != 0 else 'NA'
    else:
        pctChange = int(round(((val1 - val2) / val2) * 100, )) if len(ind_internet) != 0 else 'NA'

    if pctChange == 'NA':
        pctChange = pctChange
    elif pctChange > 0:
        pctChange = '▲ ' + str(abs(pctChange)) + '%'
    elif pctChange < 0:
        pctChange = '▼ ' + str(abs(pctChange)) + '%'
    else:
        pctChange = str(pctChange) + '%'

    # create description string  
    description = str(df.loc[df['Name'] == indicator, 'Long.name'].tail(1).tolist()[0]) \
                  + '\n\n' \
                  + str(df.loc[df['Name'] == indicator,'Description'].tail(1).tolist()[0]) \
                  + '\n\nSource: ' + str(df.loc[df['Name'] == indicator, 'Source'].tail(1).tolist()[0]) \
                  + ' (' + str(int(df.loc[df['Name'] == indicator, 'db_year'].tail(1).tolist()[0])) + ')'

    if indicator == 'GII':
        value = str(round(ind_internet['value'].tail(1).tolist()[0],3)) if len(ind_internet) != 0 else 'NO DATA'
    else:
        if format_as_rate is True:
            value = str(int(ind_internet['value'].tail(1).tolist()[0])) + '/100' if len(ind_internet) != 0 else 'NO DATA'
        else:
            value = str(int(round(val1, 0))) + '%' if len(ind_internet) != 0 else 'NO DATA'

    # create table dataframe
    df_table = pd.DataFrame()
    df_table[selected_country] = [value]
    df_table["Year"] = [max_year]
    df_table["▲▼"] = [pctChange]

    # generate html table
    indicator_table = generate_table(df_table,
                                     title=indicator_name,
                                     description=description)

    return indicator_table


def generate_gender_gap_table(selected_country):
    """
    This function generates a table for the "internet user gender gap" table on the connectivity dashboard.

    :param selected_country: selected country from dropdown
    :return: internet user gender gap table
    """

    # create DataFrame containing "gender_gap" indicator derived from "ind.internet.female" and "ind.internet.male"
    dff = df.loc[(df.Country == selected_country) & (df.Name == 'ind.internet.female')]
    dff = dff.rename(columns={'value': 'internet.female'})
    dfm = df.loc[(df.Country == selected_country) & (df.Name == 'ind.internet.male')]
    dfm = dfm.rename(columns={'value': 'internet.male'})
    dff = dff.merge(dfm[['Country', 'Year', 'internet.male']])
    dff['gender_gap'] = ((dff['internet.male'] - dff['internet.female']) / dff['internet.male']) * 100
    dff.sort_values('Year', inplace=True)

    dff = dff.tail(2)

    latest_year = dff['Year'].tail(1).tolist()[0] if dff.shape[0] > 0 else 'NA'
    first_year = dff['Year'].head(1).tolist()[0] if dff.shape[0] > 1 else 'NA'

    # compute percent change since previous year
##    value = round(dff['gender_gap'].tail(1).tolist()[0], 1) if dff.shape[0] > 0 else 'NO DATA'
##    value2 = round(dff.loc[dff['Year'] == latest_year-1,'gender_gap'].iloc[0]) if latest_year != 'NA' else 'NA'
##    print(value2)
##    #value2 = last_year if last_year > 1 else 'NA'

    check = sum([True if val == (latest_year - 1) else False for val in dff['Year'].values])
    #print(dff.loc[dff['Year'] == latest_year - 1,'gender_gap'].iloc[0] if latest_year != 'NA' else 'NA')
    

    # compute percent change since previous year
    value = round(dff['gender_gap'].tail(1).tolist()[0],1) if dff.shape[0] > 0 else 'NO DATA'
    value2 = round(dff.loc[dff['Year'] == latest_year - 1,'gender_gap'].iloc[0],1) if (latest_year != 'NA' and check == 1) else 'NA'
    pctChange= int(round(((value - value2) / value2)*100,0)) if value != 'NO DATA' and value2 != 'NA' else 'NA'
    
    #value2 = value2 + ' (' + str(first_year) + ')' if first_year != 'NA' else 'NA'
    name = 'Internet user gender gap'
    description = name + '\n\nThe gender gap represents the difference between the internet user penetration rates for males and females relative to the internet user penetration rate for males, expressed as a percentage. Values greater than 0 show women trailing men.' + '\n\nSource: International Telecommunication Union (2019)'

    if value == 'NO DATA':
        value = str(value)
    else:
        value = str(value) + '%'
    
    if pctChange == 'NA':
        pctChange = str(pctChange)
    elif pctChange > 0:
        pctChange = '▲ ' + str(abs(pctChange)) + '%'
    elif pctChange < 0:
        pctChange = '▼ ' + str(abs(pctChange)) + '%'
    else:
        pctChange = str(pctChange) + '%'
        
    # create table dataframe
    df_table = pd.DataFrame()
    df_table[selected_country] = [value]
    df_table["Year"] = [latest_year]
    df_table["▲▼"] = [pctChange]

    # generate html table
    indicator_table = generate_table(df_table,
                                     title=name,
                                     description=description)

    return indicator_table


# ----- freedom helper functions -----

# -- charts --
def generate_freedom_in_the_world_chart_political(selected_country, indicators, max_values,indicator_colors, years, title):
    # filter data by country and year
    df_filtered = df[df["Country"] == selected_country]
    df_filtered = df_filtered[[(y in years) for y in df_filtered["Year"]]]

    #filtered data
    df_filtered_Agg = df[df["Country"] == selected_country]
    df_filtered_Agg = df_filtered_Agg[df_filtered_Agg["Name"] == "FitW.total.aggregate.score"] # filtered by selected country and indicator
    df_filtered_Agg = df_filtered_Agg.dropna(axis="index",subset=["value"]) # drop rows with missing indicator values

    conditions = [(df_filtered_Agg['value'] < 33.33),(df_filtered_Agg['value'] >= 33.33) & (df_filtered_Agg['value'] < 66.66),(df_filtered_Agg['value'] >= 66.66)]
    choices = [0,1,2]
    df_filtered_Agg['color'] = np.select(conditions, choices, default='blue')

    years_agg = list(df_filtered_Agg["Year"])
    color_agg = list(df_filtered_Agg["color"])

    df_intermediate = pd.DataFrame(data = df_filtered_Agg, columns=["Year","color"])
    df_filtered = pd.merge(df_filtered,df_intermediate,how='left', on=['Year'])

    for indicator in indicators:
        df_filtered.append(df_filtered[df_filtered["Name"] == indicator])


        
    # create traces for each indicator
    traces = []
    colors = {}


    bar_colors = {}
    indicator_vals = {}

    for idx,indicator in enumerate(indicators):
        df_indicator = df_filtered[df_filtered["Name"] == indicator]
        values = list(df_indicator["value"])
        df_colors = list(df_indicator["color"])
        color_vals = []
        for idy,val in enumerate(values):
            color_vals.append(FREEDOM_COLORS[ int(df_colors[idy]) ][idx])
        bar_colors[indicator] = color_vals

    for idx,indicator in enumerate(indicators):
        df_indicator = df_filtered[df_filtered["Name"] == indicator]
        values = list(df_indicator["value"])
        yrs = [str(int(y)) for y in df_indicator["Year"]]
        name = str(df_indicator["Long.name"].iloc[0])

        traces.append(go.Bar(  # value trace
            x=values,
            y=yrs,
            name=name[48:],
            text=["%0.0f" % val for val in values],
            orientation="h",
            hoverinfo="text+name",
            width=0.4,
            marker=dict(color = bar_colors[indicator])
            
            ))

    layout = go.Layout(
        barmode="stack",
        autosize=False,
        height=600,
        width=500,
        xaxis=dict(
            #title="Score"
            tickfont=dict(family='Raleway',size=13),
        ),
 
            margin=dict(
                    l=50,
                    r=50,
                    b=150,
                    t=100,
                    pad=10
                ),
        yaxis=dict(
            #title="Year",
            type="category",
            ticks='outside',
            tick0=0,
            dtick=0.25,
            ticklen=8,
            tickwidth=1,
            tickcolor='#fff',
            tickfont=dict(family='Raleway',size=13),
        ),
        # title=title,
        title={'text': title, 'xanchor': 'center', 'x':0.5,},

        titlefont=dict(
            size=20,
            color=PLOT_COLORS["title"],
            family='Raleway'
        ),
   
        legend=dict(
            orientation="h",
            #x=2,
            #xanchor="center",
            y=-0.15,
            traceorder='normal',
            #yanchor="top",
            
            font=dict(family='Raleway',size=14),
        ),
        annotations=[
            dict(
                text="Least free (0)",
                x=0,
                xanchor="left",
                y=-0.08,
                yanchor="top",
                xref='x',
                yref='paper',
                showarrow=False,
                font=dict(family='Raleway',size=13, color='blue')
            ),
            dict(
                text="Most free ("+str(sum(max_values.values()))+")",
                x=sum(max_values.values())+5,
                xanchor="right",
                y=-0.08,
                yanchor="top",
                xref='x',
                yref='paper',
                showarrow=False,
                font=dict(family='Raleway',size=13,color='blue')
            ),
            dict(
                x=0.0,
                y=-.4,
                xref='x',
                axref='x',
                yref='paper',
                ayref='pixel',
                xanchor='left',
                align='left',
                text='Source: ' + df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                    df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                showarrow=False,
                font=dict(family='Raleway',size=14)
            )
        ]
    )

    # a figure combining data and layout
    return go.Figure(data=traces, layout=layout)


def generate_freedom_in_the_world_chart(selected_country, indicators, max_values,indicator_colors, years, title):
    # filter data by country and year
    df_filtered = df[df["Country"] == selected_country]
    df_filtered = df_filtered[[(y in years) for y in df_filtered["Year"]]]

    #filtered data
    df_filtered_Agg = df[df["Country"] == selected_country]
    df_filtered_Agg = df_filtered_Agg[df_filtered_Agg["Name"] == "FitW.total.aggregate.score"] # filtered by selected country and indicator
    df_filtered_Agg = df_filtered_Agg.dropna(axis="index",subset=["value"]) # drop rows with missing indicator values

    conditions = [(df_filtered_Agg['value'] < 33.33),(df_filtered_Agg['value'] >= 33.33) & (df_filtered_Agg['value'] < 66.66),(df_filtered_Agg['value'] >= 66.66)]
    choices = [0,1,2]
    df_filtered_Agg['color'] = np.select(conditions, choices, default='blue')

    years_agg = list(df_filtered_Agg["Year"])
    color_agg = list(df_filtered_Agg["color"])

    df_intermediate = pd.DataFrame(data = df_filtered_Agg, columns=["Year","color"])
    df_filtered = pd.merge(df_filtered,df_intermediate,how='left', on=['Year'])

    bar_colors = {}

    for idx,indicator in enumerate(indicators):
        df_indicator = df_filtered[df_filtered["Name"] == indicator]

        df_filtered.append(df_filtered[df_filtered["Name"] == indicator])
        values = list(df_indicator["value"])
        df_colors = list(df_indicator["color"])
        color_vals = []
        for idy,val in enumerate(values):
            color_vals.append(FREEDOM_COLORS[ int(df_colors[idy]) ][idx])
        bar_colors[indicator] = color_vals


    # create traces for each indicator
    traces = []
    for idx,indicator in enumerate(indicators):
        df_indicator = df_filtered[df_filtered["Name"] == indicator]
        values = list(df_indicator["value"])
        yrs = [str(int(y)) for y in df_indicator["Year"]]
        name = str(df_indicator["Long.name"].iloc[0])
        traces.append(go.Bar(  # value trace
            x=values,
            y=yrs,
            name=name[48:],
            text=["%0.0f" % val for val in values],
            orientation="h",
            hoverinfo="text+name",
            width=0.4,
            marker=dict(color = bar_colors[indicator])
            ))

    layout = go.Layout(
        barmode="stack",
        autosize=False,
        height=550,
        width=500,
        xaxis=dict(
            #title="Score"
            tickfont=dict(family='Raleway',size=13),
        ),
        yaxis=dict(
            #title="Year",
            type="category",
            ticks='outside',
            tick0=0,
            dtick=0.25,
            ticklen=8,
            tickwidth=1,
            tickcolor='#fff',
            tickfont=dict(family='Raleway',size=13),
        ),
        # title=title,
        title={'text': title, 'xanchor': 'center', 'x':0.5,},

        titlefont=dict(
            size=20,
            color=PLOT_COLORS["title"],
            family='Raleway'
        ),
        legend=dict(
            orientation="h",
            #x=2,
            #xanchor="center",
            y=-0.15,
            traceorder='normal',
            #yanchor="top",
            font=dict(family='Raleway',size=14),
        ),
                margin=dict(
                l=50,
                r=50,
                b=175,
                t=100,
                pad=10
            ),
        annotations=[
            dict(
                text="Least free (0)",
                x=0,
                xanchor="left",
                y=-0.08,
                yanchor="top",
                xref='x',
                yref='paper',
                showarrow=False,
                font=dict(family='Raleway',size=13, color='blue')
            ),
            dict(
                text="Most free ("+str(sum(max_values.values()))+")",
                x=sum(max_values.values())+5,
                xanchor="right",
                y=-0.08,
                yanchor="top",
                xref='x',
                yref='paper',
                showarrow=False,
                font=dict(family='Raleway',size=13,color='blue')
            ),
            dict(
                x=0.0,
                y=-.6,
                xref='x',
                axref='x',
                yref='paper',
                ayref='pixel',
                xanchor='left',
                align='left',
text='Source: ' + df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                    df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                showarrow=False,
                font=dict(family='Raleway',size=14)
            )
        ]
    )

    # a figure combining data and layout
    return go.Figure(data=traces, layout=layout)

def generate_political_rights_rating_chart(selected_country):
    """
    This function generates the political rights rating chart.

    :param selected_country: selected country from dropdown
    :return: political rights rating chart
    """

    indicators = ["FitW.PRR.Political.Pluralism", "FitW.PRR.Functioning.of.Government","FitW.PRR.Electoral.Process"]

    indicator_colors = {"FitW.PRR.Electoral.Process": "#ddd1e7",
                        "FitW.PRR.Functioning.of.Government": "#9975b9",
                        "FitW.PRR.Political.Pluralism": "#551a8b"}

    max_values = {"FitW.PRR.Electoral.Process": 12,
                  "FitW.PRR.Functioning.of.Government": 12,
                  "FitW.PRR.Political.Pluralism": 16}

    years = [2010,2011,2012,2013,2014,2015,2016,2017,2018]

    title = 'Are political rights protected in the country?'

    return generate_freedom_in_the_world_chart_political(selected_country=selected_country,
                                               indicators=indicators,
                                               max_values=max_values,
                                               indicator_colors=indicator_colors,
                                               years=years,
                                               title=title)


def generate_civil_liberties_rating_chart(selected_country):
    """
    This function generates the civil liberties rating chart.

    :param selected_country: selected country from dropdown
    :return: civil liberties rating chart
    """

    indicators = ["FitW.CLR.Personal.Autonomy.and.Individual.Rights",
                  "FitW.CLR.Rule.of.Law",
                  "FitW.CLR.Associational.and.Organizational.Rights",
                  "FitW.CLR.Freedom.of.Expression.and.Belief"]

    max_values = {"FitW.CLR.Freedom.of.Expression.and.Belief": 16,
                  "FitW.CLR.Associational.and.Organizational.Rights": 12,
                  "FitW.CLR.Rule.of.Law": 16,
                  "FitW.CLR.Personal.Autonomy.and.Individual.Rights": 16}


    indicator_colors = {"FitW.CLR.Freedom.of.Expression.and.Belief": "#ddd1e7",
                        "FitW.CLR.Associational.and.Organizational.Rights": "#9975b9",
                        "FitW.CLR.Rule.of.Law": "#551a8b",
                        "FitW.CLR.Personal.Autonomy.and.Individual.Rights": "#330f53"}

    years = [2010,2011,2012,2013,2014,2015,2016,2017,2018]

    title = 'Are civil liberties guaranteed in the country?'

    return generate_freedom_in_the_world_chart(selected_country=selected_country,
                                               indicators=indicators,
                                               max_values=max_values,
                                               indicator_colors=indicator_colors,
                                               years=years,
                                               title=title)


def generate_percent_using_internet_vs_freedom_on_net_chart(selected_country):
    """
    This function generates the percent using internet vs freedom on the net chart.

    :param selected_country: selected country from dropdown
    :return: percent using internet vs freedom on the net chart.
    """
    ## Create and style traces
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    selected_country_year = df.loc[(df.Country == selected_country) & (df.Name == 'ind.internet'),'Year'].tolist()
    max_year = max(selected_country_year)
    # max_year = 2017

    # df.loc[df.groupby(["sp", "mt"])["count"].idxmax()]  
    x1 = df.loc[(df['Name'] == 'FotN') & (df['Region'] == rgn)]

    x1 = x1.sort_values('Year').groupby(['Country']).tail(1)

    # x1 = df.loc[(df['Year'] == max_year) & (df['Name'] == 'FotN') & (df['Region'] == rgn)]
    # x1 = x1.sort_values('Year').groupby(['Country']).tail(1)
    # x1 = x1.loc(x1.groupby(['Country'])['Year'].idxmax())

    x2 = df.loc[(df['Name'] == 'ind.internet')].sort_values('Year').groupby(['Country']).tail(1)
    x2.rename(columns={'value': 'internet'}, inplace=True)
    x1 = x1.merge(x2[['Country', 'internet']],
                  how='left', left_on=['Country'], right_on=['Country'])
                  
 
##    x11 = df.loc[(df['Name'] == 'FoD') & (df['Country'] == selected_country)].tail(3)
##    x22 = df.loc[(df['Name'] == 'ind.internet') & (df['Country'] == selected_country)].tail(3)
##    x22.rename(columns={'value':'internet'},inplace=True)
##    x33 = x11.merge(x22[['Country','Year','internet']],how='left',left_on=['Country','Year'],right_on=['Country','Year'])
    x3 = x1.loc[(x1['Country'] == selected_country)]
    
    if (x3.shape[0] > 0):
        x4 = x3['internet']
        y4 = x3['value']
        ct = selected_country
        return {
        'data': [
            go.Scatter(  # All data for FotN
                x=x1['value'] if x3.shape[0] == 0 else x1.loc[x1['Country'] != ct, 'value'],
                y=x1['internet'] if x3.shape[0] == 0 else x1.loc[x1['Country'] != ct, 'internet'],
                mode='markers',
                text=x1['Country'] if x3.shape[0] == 0 else x1.loc[x1['Country'] != ct, 'Country'],
                # textposition = 'bottom center',
                name=rgn,
                marker=dict(
                    color=('#38C0E1'),
                    line = dict(width = 1.5),
                    size=15)
            ),
            go.Scatter(  # Country data
                x=y4,
                y=x4,
                
                mode='markers',
                text= x3['Year'],
                textposition='bottom center',
                name=ct,
                marker=dict(
                    color=('#FF8A5B'),
                    line = dict(width = 1.5),
                    size=15)
            )
        ],
        ## Edit the layout
        'layout': go.Layout(
            title='As more people around the world come online, is higher internet use,<br> leading to higher freedom online in the country?',
            titlefont=dict(size=20,
                           color='#38C0E1',
                           family='Raleway'),
            font=dict(family='Raleway', size=13),
            xaxis=dict(title='Freedom on the Net',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 102],zeroline=False),
            yaxis=dict(title='% of population using the Internet',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 102]),
            showlegend=True,
       
            #width = 500,
            height=500,
            legend=dict(x=.8,
                            y=1.03 if x3['value'].tolist()[0] < 40 else 0.1
                            #, orientation="h"
                            ),
            annotations=[
                dict(
                    text="NO DATA AVAILABLE",
                    showarrow=False,
                    visible=True if (len(x3) == 0) else False
                    ),
                dict(
                    x=0.0,
                    y=-.45,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
                    text='Source: ' + df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                        df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                    showarrow=False,
                    font=dict(family='Raleway',size=14)
                ),
                dict(
                    x=.75,
                    y=.05,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='No data for ' + ct if x3.shape[0] == 0 else '',
                    showarrow=False,
                    font=dict(family='Raleway')
                ),
                dict(
                    x=0.0,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='Less free',
                    showarrow=False,
                    font=dict(family='Raleway',size=13,color='blue')
                ),
                dict(
                    x=95,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='More free',
                    showarrow=False,
                    font=dict(family='Raleway',size=13,color='blue')
                )
            ]
        )
    }
    
    else:
        x4 = np.nan
        y4 = np.nan
        ct = selected_country

    return {
        'data': [],
        ## Edit the layout
        'layout': go.Layout(
            title='As more people around the world come online, is higher internet use,<br> leading to higher freedoms online in the country?',
            titlefont=dict(size=20,
                           color='#38C0E1',
                           family='Raleway'),
            font=dict(family='Raleway', size=13),
            xaxis=dict(title='Freedom on the Net',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 100],zeroline=False),
            yaxis=dict(title='Population using Internet (%)',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 100], zeroline=False),
            showlegend=True,
            #width = 500,
            height=600,
            legend = dict(x=.1,
                          y=-0.4 ),
                         
            annotations=[
                dict(
                    text="NO DATA AVAILABLE",
                    showarrow=False,
                    visible=True if (len(x3) == 0) else False
                    ),
                dict(
                    # x=0.0,
                    y=-.4,
                    # xref='x',
                    # axref='x',
                    yref='paper',
                    ayref='pixel',
                    # xanchor='left',
                    align='left',
text='Source: ' + df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                        df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                    showarrow=False,
                    font=dict(family='Raleway',size=14)
                ),
##                dict(
##                    x=.75,
##                    y=.05,
##                    xref='x',
##                    axref='x',
##                    yref='paper',
##                    ayref='pixel',
##                    xanchor='left',
##                    text='No data for ' + ct if x3.shape[0] == 0 else '',
##                    showarrow=False,
##                    font=dict(family='Raleway')
##                ),
                dict(
                    x=0.0,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='More free',
                    showarrow=False,
                    font=dict(family='Raleway',size=13,color='blue')
                ),
                dict(
                    x=95,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='Less free',
                    showarrow=False,
                    font=dict(family='Raleway',size=13,color='blue')
                )
            ]
        )
    }

def generate_country_percent_using_internet_vs_freedom_on_net_chart(selected_country):
    """
    This function generates the percent using internet vs freedom on the net chart.

    :param selected_country: selected country from dropdown
    :return: percent using internet vs freedom on the net chart.
    """
    ## Create and style traces
    x1 = df.loc[(df.Country == selected_country) & (df['Name'] == 'FotN')]
    x2 = df.loc[(df['Name'] == 'ind.internet')]
    x2.rename(columns={'value': 'internet'}, inplace=True)
    x3 = x1.merge(x2[['Country', 'Year', 'internet']],how='left', left_on=['Country', 'Year'], right_on=['Country', 'Year'])
    x3.sort_values('Year',inplace=True)
    x3 = x3.tail(5)
    if (len(x3) != 0):
        x4 = x3['internet']
        y4 = x3['value']
        z4 = [str(ele) for ele in x3['Year']]
        ct = selected_country
        colors = ['#ffd27f','#ffb732','#ffa500','#cc8400','#996300','#664200','#4c3100']
        
        trace=[]
        for i in range(len(z4)):
            trace.append(go.Scatter(  # Country data
                    x=y4,
                    y=x4,
                    mode='markers',
                    text=x3['Year'],
                    #textposition = "middle right",
                    name=z4[i],
                    marker=dict(line = dict(width = 1),
                                size=15)
                                )
                     ),

            ## Edit the layout
            layout = go.Layout(
                title='% using internet vs Freedom on Net<br>Country Progress',
                hovermode= 'closest',
                titlefont=dict(size=20,
                           color='#38C0E1',
                           family='Raleway'),
                font=dict(family='Raleway', size=13),
                xaxis=dict(title='Freedom on the Net',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 100]),
                yaxis=dict(title='Population using Internet (%)',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 100]),
                showlegend=True,
                width = 500,
                height=500,
                legend=dict(x=.8,
                            y=1 if x3['value'].tolist()[0] < 40 else 0.1
                            #, orientation="h"
                            ),
                annotations=[
                    dict(text="NO DATA AVAILABLE",
                         showarrow=False,
                         visible=True if (len(x3) == 0) else False
                        ),
                    dict(
                        x=0.0,
                        y=-.25,
                        xref='x',
                        axref='x',
                        yref='paper',
                        ayref='pixel',
                        xanchor='left',
                        align='left',
text='Source: ' + df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                            df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                        showarrow=False,
                        font=dict(family='Raleway',size=14)
                    ),
                    dict(
                        x=0.0,
                        y=-.15,
                        xref='x',
                        axref='x',
                        yref='paper',
                        ayref='pixel',
                        xanchor='left',
                        text='More free',
                        showarrow=False,
                        font=dict(family='Raleway',size=13,color='blue')
                    ),
                dict(
                    x=90,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='Less free',
                    showarrow=False,
                    font=dict(family='Raleway',size=13,color='blue')
                )])
        
        return go.Figure(data=trace,layout=layout)

    else:
        x4 = 'NO DATA'
        y4 = 'NA'
        z4 = 'NA'
        ct = selected_country

        ## Edit the layout
        layout = go.Layout(
            title='% using internet vs Freedom on Net<br>Country Progress',
            hovermode= 'closest',
            titlefont=dict(size=20,
                           color='#38C0E1',
                           family='Raleway'),
            font=dict(family='Raleway', size=13),
            xaxis=dict(title='Freedom on the Net',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 100]),
            yaxis=dict(title='Population using Internet (%)',titlefont = dict(size=15,family='Raleway'),
                       range=[0, 100]),
            showlegend=True,
            width = 500,
            height=500,
            annotations=[
                dict(
                    text="NO DATA AVAILABLE",
                    showarrow=False,
                    visible=True if (len(x3) == 0) else False
                    ),
                dict(
                    x=0.0,
                    y=-.25,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
text='Source: ' + df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                        df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                    showarrow=False,
                    font=dict(family='Raleway',size=14)
                ),
                dict(
                    x=0.0,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='More free',
                    showarrow=False,
                    font=dict(family='Raleway',size=13,color='blue')
                ),
                dict(
                    x=90,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='Less free',
                    showarrow=False,
                    font=dict(family='Raleway',size=13,color='blue')
                )])
        
        return go.Figure(data=[],layout=layout)


def generate_freedom_on_the_net_choropleth_chart():
    """
    This function generates the freedom on the net choropleth map.

    :return: freedom on the net choropleth map
    """
    dt = df.loc[df['Name'] == 'FotN']
    dg = dt.groupby(['Name', 'Country']).aggregate({'Year': 'max'}).reset_index()
    dt = dg.merge(dt[['Name', 'Country', 'ISO3', 'Year', 'value']], how='left', on=['Name', 'Country', 'Year'])

    blanks = df.loc[~(df['ISO3'].isin(dt['ISO3'])), ['Country', 'ISO3']].drop_duplicates()
    blanks['Name'] = 'FotN'
    blanks['Year'] = np.nan
    blanks['value'] = np.nan
    dt = pd.concat([dt, blanks])
    # colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    # [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],

    return {

        'data': [dict(
            type='choropleth',
            locations=dt['ISO3'],
            z=dt['value'],
            text=dt['Country'],
            colorscale=[[0, "rgb(5, 10, 172)"], [35, "rgb(40, 60, 190)"], [50, "rgb(70, 100, 245)"], \
                        [60, "rgb(90, 120, 245)"], [70, "rgb(106, 137,247)"], [100, "rgb(220, 220, 220)"]],
            autocolorscale=False,
            reversescale=True,
            marker=dict(
                line=dict(
                    color='rgb(0,0,0)',
                    width=0.5
                )),
            colorbar=dict(
                autotick=False,
                tickmode='array',
                tickvals=[dt['value'].min(), dt['value'].max()],
                ticktext=['0  (Most free)', '100 (Least free)'],
                ticks='outside',
                title=''),
        )],

        'layout': dict(
            title='Freedom on the Net',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection=dict(
                    type='Mercator'
                )
            )
        )

    }

    # -- tables --


def generate_freedom_in_the_world_table(selected_country, indicator, max_values,indicator_name):
    """
    This function generates tables associated with both "Freedom in the World Political Rights Rating" and "Freedom
    in the World Civil Liberties Rating charts".

    :param selected_country: selected country from dropdown
    :param indicator: Either "FitW.PRR.aggregate.score" for Political Rights Rating or "FitW.CLR.aggregate.score"
    for Civil Liberties Rating.
    :param indicator_name: Either "Political Rights Rating" or "Civil Liberties Rating"
    :return: a Dash html.Table component
    """
    prr = df.loc[(df.Country == selected_country) & (df.Name == indicator)]
    prr.sort_values('Year', inplace=True)
    if (prr.shape[0] > 0):
        value = str(int(prr['value'].tail(1).tolist()[0]))
        max_year = prr['Year'].tail(1).tolist()[0]
        rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
        change = int(prr.iloc[-1,2]) - int(prr.iloc[-2,2])
        rank = getCountryRank(selected_country=selected_country,
                              region=rgn,
                              indicator=indicator,
                              ascending=True)
    else:
        value = 'NO DATA'
        max_year = 'NA'
        rank = 'NA'
        change = 'NA'

    name = indicator_name
    description = df.loc[df['Name'] == indicator, 'Long.name'].tail(1).tolist()[0] + '\n\n' + \
                  df.loc[df['Name'] == indicator, 'Description'].tail(1).tolist()[0] + '\n\nSource: ' + \
                  df.loc[df['Name'] == indicator, 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == indicator, 'db_year'].tail(1).tolist()[0])) + ')'

    if change == 'NA':
        change = str(change)
    elif change > 0:
        change = '▲ ' + str(abs(change))
    elif change < 0:
        change = '▼ ' + str(abs(change))
    else:
        pctChange = str(change)
        
    df_table = pd.DataFrame()
    df_table[selected_country] = [value+"/"+str(max_values)]
    df_table["Year"] = [max_year]
    df_table["▲▼"] = [change]

    return generate_table(df_table=df_table,
                          title=indicator_name,
                          description=description)


def generate_percent_using_internet_vs_freedom_on_net_table(selected_country):
    """
    This function generates a table associated with the "% using the internet vs Freedom on the Net" chart.

    :param selected_country: selected country from dropdown
    :return: a Dash html.Table component
    """
    fotn = df.loc[(df.Country == selected_country) & (df.Name == 'FotN')]
    fotn.sort_values('Year', inplace=True)
    if (fotn.shape[0] > 0):
        value = int(fotn['value'].tail(1).tolist()[0])
        max_year = fotn['Year'].tail(1).tolist()[0]
        rating = 'Not Free' if value <= 40 else ('Partly Free' if value <= 70 else 'Free')
        rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
        rank = getCountryRank(selected_country=selected_country,
                              region=rgn,
                              indicator='FotN',
                              ascending=False)
    else:
        value = 'NO DATA'
        max_year = 'NA'
        rating = 'NA'

    value = str(value) + '/100' if value != 'NO DATA' else value
    name = 'Freedom on the Net'
    description = df.loc[df['Name'] == 'FotN', 'Long.name'].tail(1).tolist()[0] + '\n\n' + \
                  df.loc[df['Name'] == 'FotN', 'Description'].tail(1).tolist()[0] + '\n\nSource: ' + \
                  df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')'

    df_table = pd.DataFrame()
    df_table[selected_country] = [value]
    df_table["Rating"] = [rating]
    df_table["Year"] = [max_year]

    return generate_table(df_table=df_table,
                          title=name,
                          description=description)

def generate_country_percent_using_internet_vs_freedom_on_net_table(selected_country):
    """
    This function generates a table associated with the "% using the internet vs Freedom on the Net" chart.

    :param selected_country: selected country from dropdown
    :return: a Dash html.Table component
    """
    fotn = df.loc[(df.Country == selected_country) & (df.Name == 'FotN')]
    fotn.sort_values('Year', inplace=True)
    if (fotn.shape[0] > 0):
        value = int(fotn['value'].tail(1).tolist()[0])
        max_year = fotn['Year'].tail(1).tolist()[0]
        rating = 'Free' if value <= 30 else ('Partly Free' if value <= 60 else 'Not Free')
        rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
        rank = getCountryRank(selected_country=selected_country,
                              region=rgn,
                              indicator='FotN',
                              ascending=False)
    else:
        value = 'NO DATA'
        max_year = 'NA'
        rating = 'NA'

    name = 'Freedom on the Net'
    description = df.loc[df['Name'] == 'FotN', 'Long.name'].tail(1).tolist()[0] + '\n\n' + \
                  df.loc[df['Name'] == 'FotN', 'Description'].tail(1).tolist()[0] + '\n\nSource: ' + \
                  df.loc[df['Name'] == 'FotN', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')'

    df_table = pd.DataFrame()
    df_table["Score"] = [value]
    df_table["Rating"] = [rating]
    df_table["Year"] = [max_year]

    return generate_table(df_table=df_table,
                          title=name,
                          description=description)


    # ----- gender helper functions -----


def generate_technology_use_chart(selected_country,title_text):
    """
    This function generates the "technology use" chart in the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: technology use chart
    """
    ## Create and style traces
    filtered_df = df.loc[(df.Country == selected_country) & \
                         (df['Name'].isin(['ind.internet.female', 'ind.internet.male',
                                           'Computer.use.female', 'Computer.use.male',
                                           'mobile.use.female', 'mobile.use.male']))]
    filtered_df.sort_values('Year', inplace=True)

    ## safely pull data, planning for lots of missing
    x1 = [filtered_df.loc[filtered_df['Name'] == 'ind.internet.male', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'ind.internet.male' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'ind.internet.female', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'ind.internet.female' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x2 = [filtered_df.loc[filtered_df['Name'] == 'Computer.use.male', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'Computer.use.male' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'Computer.use.female', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'Computer.use.female' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x3 = [
        filtered_df.loc[filtered_df['Name'] == 'mobile.use.male', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                               0] > 0) & (
                                                                                                  'mobile.use.male' in
                                                                                                  filtered_df[
                                                                                                      'Name'].unique()) else np.nan,
        filtered_df.loc[filtered_df['Name'] == 'mobile.use.female', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                 0] > 0) & (
                                                                                                    'mobile.use.female' in
                                                                                                    filtered_df[
                                                                                                        'Name'].unique()) else np.nan]

    # Create the graph with subplots
    trace1 = go.Bar(
        x=x1,
        y=['Men ', 'Women '],
        orientation='h',
        text=x1,
        textposition='auto',
        name='Internet use by gender',
        width=0.6,
        marker=dict(
            color=[PLOT_COLORS["men"], PLOT_COLORS["women"]],
            opacity = 0.5,
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,
            )
        )
    )
    trace2 = go.Bar(
        x=x2,
        y=['Men ', 'Women '],
        orientation='h',
        text=x2,
        textposition='auto',
        name='Computer use by gender',
        width=0.6,
        marker=dict(
            color=[PLOT_COLORS["men"], PLOT_COLORS["women"]],
            opacity = 0.6,
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,

            )
        )
    )
    trace3 = go.Bar(
        x=x3,
        y=['Men ', 'Women '],
        orientation='h',
        text=x3,
        textposition='auto',
        name='Mobile phone use by gender',
        width=0.6,
        
        marker=dict(
            color=[PLOT_COLORS["men"], PLOT_COLORS["women"]],
            opacity = 0.5,
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,

            )
        )
    )

    # asdf
    src_text = 'Source: International Telecommunication Union (2019)<br>Technology & Social Change Group, University of Washington'

    fig = tools.make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.15,
                              subplot_titles=('Internet use', 'Computer use', 'Mobile phone use',src_text))
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 3, 1)
    
    fig['layout'].update(height=600,width=500)
    fig['layout']['xaxis1'].update(range=[0, 100],position=0.3,tickfont=dict(family='Raleway',size=14))
    fig.update_xaxes(range=[0, 100])

    fig['layout'].update(font=dict(size=14, family='Raleway'))
    fig['layout']['yaxis1'].update(tickfont=dict(family='Raleway',size=14),linewidth=0)
    fig['layout']['yaxis2'].update(tickfont=dict(family='Raleway',size=14))
    fig['layout']['yaxis3'].update(tickfont=dict(family='Raleway',size=14))

    annotations = []
    if (math.isnan(x1[0]) or math.isnan(x1[1])):
        annotations.append(dict(x=0.5, y=0.9,text="Internet Use<br><br>NO DATA AVAILABLE",showarrow=False, font=dict(family='Raleway',size=16)))
    else:
        annotations.append(dict(x=0.5, y=1,text="Internet Use",showarrow=False, font=dict(family='Raleway',size=16)))

    if (math.isnan(x2[0]) or math.isnan(x2[1])):
        annotations.append(dict(x=0.5, y=0.62, text="Computer Use<br><br>NO DATA AVAILABLE",showarrow=False, font=dict(family='Raleway',size=16)))
    else:
        annotations.append(dict(x=0.5, y=0.75, text="Computer Use",showarrow=False, font=dict(family='Raleway',size=16)))

    if (math.isnan(x3[0]) or math.isnan(x3[1])):
        annotations.append(dict(x=0.5, y=0.33,text="Mobile Phone Use<br><br>NO DATA AVAILABLE",showarrow=False, font=dict(family='Raleway',size=16)))
    else:
        annotations.append(dict(x=0.5, y=0.45,text="Mobile Phone Use",showarrow=False, font=dict(family='Raleway',size=16)))
      
    annotations.append(dict(x=0.5, y=0.1, xref='x', axref='x', yref='paper', ayref='pixel', xanchor='left', align='left', text=src_text,showarrow=False,font=dict(family='Raleway',size=14),opacity=0.8))

    fig['layout'].update(annotations=annotations)
        

    fig['layout'].update(showlegend=False, title=dict(text=title_text,xanchor='center',x=0.5,font=dict(family='Raleway',size=20,color=PLOT_COLORS["title"])))

    return fig

def generate_technology_use_table(selected_country, title_text):
    filtered_df = df.loc[(df.Country == selected_country) & \
                         (df['Name'].isin(['ind.internet.female', 'ind.internet.male',
                                           'Computer.use.female', 'Computer.use.male',
                                           'mobile.use.female', 'mobile.use.male']))]
    filtered_df.sort_values('Year', inplace=True)

    ## safely pull data, planning for lots of missing
    x1 = [filtered_df.loc[filtered_df['Name'] == 'ind.internet.male', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'ind.internet.male' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'ind.internet.female', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'ind.internet.female' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x2 = [filtered_df.loc[filtered_df['Name'] == 'Computer.use.male', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'Computer.use.male' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'Computer.use.female', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'Computer.use.female' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x3 = [
        filtered_df.loc[filtered_df['Name'] == 'mobile.use.male', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                               0] > 0) & (
                                                                                                  'mobile.use.male' in
                                                                                                  filtered_df[
                                                                                                      'Name'].unique()) else np.nan,
        filtered_df.loc[filtered_df['Name'] == 'mobile.use.female', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                 0] > 0) & (
                                                                                                    'mobile.use.female' in
                                                                                                    filtered_df[
                                                                                                        'Name'].unique()) else np.nan]

    df_table = pd.DataFrame()
    df_table[''] = ['Internet use', 'Computer use', 'Mobile use']

    df_table['Male (%)'] = [str(x1[0]) if str(x1[0]) != 'nan' else 'No data',str(x2[0]) if str(x2[0]) != 'nan' else 'No data',str(x3[0]) if str(x3[0]) != 'nan' else 'No data']

    df_table['Female (%)'] = [str(x1[1]) if str(x1[1]) != 'nan' else 'No data',str(x2[1]) if str(x2[1]) != 'nan' else 'No data',str(x3[1]) if str(x3[1]) != 'nan' else 'No data']

    # generate html table
    indicator_table = generate_table(df_table,
                                     title=title_text,
                                     description='Individuals using the Internet refers to people who used the Internet from any location and for any purpose, irrespective of the device and network used in the last three months. It can be via a computer (i.e. desktop computer, laptop computer, tablet or similar handheld computer), mobile phone, games machine, digital TV, etc. Access can be via a fixed or mobile network. Data are obtained by countries through national household surveys and are either provided directly to ITU by national statistical offices (NSOs), or obtained by ITU through its own research, for example from NSO websites. There are certain data limits to this indicator, insofar as estimates have to be calculated for many developing countries which do not yet collect ICT household statistics. Over time, as more data become available, the quality of the indicator will improve.\n\nIndividuals using a computer (from any location), by gender (%)\n\nIndividuals using a mobile cellular telephone, by gender (%)\n\nInternational Telecommunication Union (2019)')

    return indicator_table

def generate_ict_skills_chart(selected_country,title_text):
    """
    This function generates the "ict skills" chart in the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: ict skills chart
    """
    ## Create and style traces
    filtered_df = df.loc[(df.Country == selected_country) & \
                         (df['Name'].isin(['IS.F.Using copy and p', 'IS.M.Using copy and p',
                                           'IS.F.Using basic arit', 'IS.M.Using basic arit',
                                           'IS.F.Writing a comput', 'IS.M.Writing a comput']))]
    filtered_df.sort_values('Year', inplace=True)

    ## safely pull data, planning for lots of missing
    x1 = [filtered_df.loc[filtered_df['Name'] == 'IS.M.Using copy and p', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'IS.M.Using copy and p' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'IS.F.Using copy and p', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'IS.F.Using copy and p' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x2 = [filtered_df.loc[filtered_df['Name'] == 'IS.M.Using basic arit', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'IS.M.Using basic arit' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'IS.F.Using basic arit', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'IS.F.Using basic arit' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x3 = [
        filtered_df.loc[filtered_df['Name'] == 'IS.M.Writing a comput', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                               0] > 0) & (
                                                                                                  'IS.M.Writing a comput' in
                                                                                                  filtered_df[
                                                                                                      'Name'].unique()) else np.nan,
        filtered_df.loc[filtered_df['Name'] == 'IS.F.Writing a comput', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                 0] > 0) & (
                                                                                                    'IS.F.Writing a comput' in
                                                                                                    filtered_df[
                                                                                                        'Name'].unique()) else np.nan]

    # Create the graph with subplots
    trace1 = go.Bar(
        x=x1,
        y=['Men ', 'Women '],
        orientation='h',
        text=x1,
        textposition='auto',
        name='Copy and Paste Tools',
        width=0.6,
        marker=dict(
            color=[PLOT_COLORS["men"], PLOT_COLORS["women"]],
            opacity = 0.5,
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,
            )
        )
    )
    trace2 = go.Bar(
        x=x2,
        y=['Men ', 'Women '],
        orientation='h',
        text=x2,
        textposition='auto',
        name='Arithmetic Operations',
        width=0.6,
        marker=dict(
            color=[PLOT_COLORS["men"], PLOT_COLORS["women"]],
            opacity = 0.6,
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,

            )
        )
    )
    trace3 = go.Bar(
        x=x3,
        y=['Men ', 'Women '],
        orientation='h',
        text=x3,
        textposition='auto',
        name='Computer Programming',
        width=0.6,
        marker=dict(
            color=[PLOT_COLORS["men"], PLOT_COLORS["women"]],
            opacity = 0.5,
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,

            )
        )
    )

    src_text = 'Source: International Telecommunication Union (2019)<br>Technology & Social Change Group, University of Washington'

    fig = tools.make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.15,
                              subplot_titles=(['Copy and Paste Tools','Arithmetic Operations','Computer Programming',src_text]))
    fig['layout'].update(height=600,width=500, xaxis={ 'range': [0, 100]}, barmode= 'relative')

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 3, 1)
    #    'xaxis': {'title': 'Query Duration', 'range': [1, 10]},




    # todo here

    annotations = []
    if (math.isnan(x1[0]) or math.isnan(x1[1])):
        annotations.append(dict(x=0.5,y=0.9,text='Copy and Paste Tools<br><br>NO DATA AVAILABLE'))
    else:
        annotations.append(dict(x=0.5,y=1,text='Copy and Paste Tools'))

    if (math.isnan(x2[0]) or math.isnan(x2[1])):
        annotations.append(dict(x=0.5,y=0.62,text='Arithmetic Operations<br><br>NO DATA AVAILABLE'))
        
    else:
        annotations.append(dict(x=0.5,y=0.76,text='Arithmetic Operations'))

    if (math.isnan(x3[0]) or math.isnan(x3[1])):
        annotations.append(dict(x=0.5,y=0.33,text='Computer Programming<br><br>NO DATA AVAILABLE'))
    else:
        annotations.append(dict(x=0.5,y=0.45,text='Computer Programming'))
      
    annotations.append(dict(x=0.0,y=0.1,text=src_text,font=dict(family='Raleway',size=14), align='left',xanchor='left'))

    fig['layout'].update(annotations=annotations)
    fig['layout']['xaxis1'].update(range=[0, 100],position=0.3,tickfont=dict(family='Raleway',size=14))
    fig['layout'].update(font=dict(size=14, family='Raleway'))
    fig.update_xaxes(range=[0, 100])

    fig['layout']['yaxis1'].update(tickfont=dict(family='Raleway',size=14),linewidth=0)
    fig['layout']['yaxis2'].update(tickfont=dict(family='Raleway',size=14))
    fig['layout']['yaxis3'].update(tickfont=dict(family='Raleway',size=14))
    fig['layout'].update(showlegend=False, title=dict(text=title_text,xanchor='center',x=0.5,font=dict(family='Raleway',size=20,color=PLOT_COLORS["title"])))

    return fig


def generate_ict_skills_table(selected_country, title_text):
    ## Create and style traces
    filtered_df = df.loc[(df.Country == selected_country) & \
                         (df['Name'].isin(['IS.F.Using copy and p', 'IS.M.Using copy and p',
                                           'IS.F.Using basic arit', 'IS.M.Using basic arit',
                                           'IS.F.Writing a comput', 'IS.M.Writing a comput']))]
    filtered_df.sort_values('Year', inplace=True)

    ## safely pull data, planning for lots of missing
    x1 = [filtered_df.loc[filtered_df['Name'] == 'IS.M.Using copy and p', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'IS.M.Using copy and p' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'IS.F.Using copy and p', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'IS.F.Using copy and p' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x2 = [filtered_df.loc[filtered_df['Name'] == 'IS.M.Using basic arit', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                   0] > 0) & (
                                                                                                      'IS.M.Using basic arit' in
                                                                                                      filtered_df[
                                                                                                          'Name'].unique()) else np.nan,
          filtered_df.loc[filtered_df['Name'] == 'IS.F.Using basic arit', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                     0] > 0) & (
                                                                                                        'IS.F.Using basic arit' in
                                                                                                        filtered_df[
                                                                                                            'Name'].unique()) else np.nan]
    x3 = [
        filtered_df.loc[filtered_df['Name'] == 'IS.M.Writing a comput', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                               0] > 0) & (
                                                                                                  'IS.M.Writing a comput' in
                                                                                                  filtered_df[
                                                                                                      'Name'].unique()) else np.nan,
        filtered_df.loc[filtered_df['Name'] == 'IS.F.Writing a comput', 'value'].tolist()[0] if (filtered_df.shape[
                                                                                                 0] > 0) & (
                                                                                                    'IS.F.Writing a comput' in
                                                                                                    filtered_df[
                                                                                                        'Name'].unique()) else np.nan]


    df_table = pd.DataFrame()
    df_table[''] = ['Copy and paste tools', 'Aritmetical operations', 'Computer programming']
    df_table['Male (%)'] = [str(x1[0]) if str(x1[0]) != 'nan' else 'No data',str(x2[0]) if str(x2[0]) != 'nan' else 'No data',str(x3[0]) if str(x3[0]) != 'nan' else 'No data']

    df_table['Female (%)'] = [str(x1[1]) if str(x1[1]) != 'nan' else 'No data',str(x2[1]) if str(x2[1]) != 'nan' else 'No data',str(x3[1]) if str(x3[1]) != 'nan' else 'No data']

    # generate html table
    indicator_table = generate_table(df_table,
                                     title=title_text,
                                     description='Individuals with ICT skills, by type of skills by gender. This refers to ICT skills, defined for the purpose of this indicator as having undertaken certain computer-related activities in the last three months. \n\nSource: International Telecommunication Union (2019)')

    return indicator_table


def generate_unemployment_chart(selected_country,title_text):
    """
    This function generates the UNEMPLOYMENT chart in the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: UNEMPLOYMENT chart
    """
    ## Create and style traces
    women = getCountryData(selected_country, 'Unemp.Female')
    men = getCountryData(selected_country, 'Unemp.Male')
    ## Compute regional average weighted by country population
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    regional = weightedAverage(rgn, 'Unemp.Female')
    regional_male = weightedAverage(rgn, 'Unemp.Male')
    maxValue = max([women['value'].max(), regional['w_avg'].max()])
    src_text = 'Source: ' + df.loc[df['Name'] == 'Unemp.Female', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == 'Unemp.Female', 'db_year'].tail(1).tolist()[0]))+ ')<br>Technology & Social Change Group, University of Washington'
    ct = women['Country'].tolist()[0]
    
    return {
        'data': [
            go.Scatter(  # Country data
                x=women['Year'],
                y=women['value'],
                text=women['Country'],
                name=women['Country'].tolist()[0] + ', Women',
                opacity=0.5,
                line=dict(
                    color=PLOT_COLORS["women"],
                    width=4),
                marker=dict(
                    size=MARKER_SIZE)
            ),
            go.Scatter(  # Country data
                x=men['Year'],
                y=men['value'],
                text=women['Country'],
                name=women['Country'].tolist()[0] + ', Men',
                opacity=0.5,
                line=dict(
                    color=PLOT_COLORS["men"],
                    width=4),
                marker=dict(
                    size=MARKER_SIZE)
            ),
        ],

        ## Edit the layout
        'layout': go.Layout(
            title=title_text,
            titlefont=dict(size=20, color='#38C0E1', family='Raleway'),
            font=dict(size=14, family='Raleway'),
            height=PLOT_HEIGHT,width=500,
            xaxis=dict(title='',
                       range=[2005.5, 2019.5],
                       tick0=2006,
                       dtick=2),
            yaxis=dict(title='Percent',
                       range=[0,100],tickfont=dict(size=14, family='Raleway'),),
            legend=dict(x=.1,
                        y=1 if regional['w_avg'].tolist()[0] < 60 else 0.1),
            annotations=[
                dict(
                    x=2005.5,
                    y=-.35,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text=src_text,
                    showarrow=False,
                    align='left',
                    font=dict(family='Raleway')),
                dict(
                    x=2006,
                    y=.05,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='No data for ' + ct if sum(women['value'].notnull()) == 0 else '',
                    showarrow=False,
                    font=dict(family='Raleway')
                )
            ]
        )
    }


def generate_neet_chart(selected_country,title_text):
    """
    This function generates the NEET chart in the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: NEET chart
    """
    ## Create and style traces
    women = getCountryData(selected_country, 'NEET.Female')
    men = getCountryData(selected_country, 'NEET.Male')
    ## Compute regional average weighted by country population
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    regional = weightedAverage(rgn, 'NEET.Female')
    regional_male = weightedAverage(rgn, 'NEET.Male')
    maxValue = max([women['value'].max(), regional['w_avg'].max()])
    src_text = 'Source: ' + df.loc[df['Name'] == 'NEET.Female', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == 'NEET.Female', 'db_year'].tail(1).tolist()[0]))+ ')<br>Technology & Social Change Group, University of Washington'
    ct = women['Country'].tolist()[0]
    
    return {
        'data': [
            go.Scatter(  # Country data
                x=women['Year'],
                y=women['value'],
                text=women['Country'],
                name=women['Country'].tolist()[0] + ', Women',
                opacity=0.5,
                line=dict(
                    color=PLOT_COLORS["women"],
                    width=4),
                marker=dict(
                    size=MARKER_SIZE)
            ),
            go.Scatter(  # Country data
                x=men['Year'],
                y=men['value'],
                text=women['Country'],
                name=women['Country'].tolist()[0] + ', Men',
                opacity=0.5,
                line=dict(
                    color=PLOT_COLORS["men"],
                    width=4),
                marker=dict(
                    size=MARKER_SIZE)
            ),
        ],

        ## Edit the layout
        'layout': go.Layout(
            title=title_text,
            titlefont=dict(size=20, color='#38C0E1', family='Raleway'),
            font=dict(size=14, family='Raleway'),
            height=PLOT_HEIGHT,width=500,
            xaxis=dict(title='',
                       range=[2005.5, 2019.5],
                       tick0=2006,
                       dtick=2),
            yaxis=dict(title='Percent',
                       range=[0, 100],tickfont=dict(size=14, family='Raleway'),),
            legend=dict(x=.1,
                        y=1 if regional['w_avg'].tolist()[0] < 60 else 0.1),
            annotations=[
                dict(
                    x=2005.5,
                    y=-.35,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
                    text=src_text,
                    showarrow=False,
                    font=dict(family='Raleway')),
                dict(
                    x=2006,
                    y=.05,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='No data for ' + ct if sum(women['value'].notnull()) == 0 else '',
                    showarrow=False,
                    font=dict(family='Raleway')
                )
            ]
        )
    }


def generate_gender_inequality_choropleth():
    """
    This function generates the gender inequality choropleth chart in the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: gender inequality choropleth chart
    """
    dt = df.loc[df['Name'] == 'GII']
    dg = dt.groupby(['Name', 'Country']).aggregate({'Year': 'max'}).reset_index()
    dt = dg.merge(dt[['Name', 'Country', 'ISO3', 'Year', 'value']], how='left', on=['Name', 'Country', 'Year'])

    return {

        'data': [dict(
            type='choropleth',
            locations=dt['ISO3'],
            z=dt['value'],
            text=dt['Country'],
            colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"], \
                        [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
            autocolorscale=False,
            reversescale=True,
            marker=dict(
                line=dict(
                    color='rgb(180,180,180)',
                    width=0.5
                )),
            colorbar=dict(
                autotick=False,
                tickmode='array',
                tickvals=[dt['value'].min(), dt['value'].max()],
                ticktext=['0.0 (More equal)', '1.0 (Less equal)'],
                ticks='outside',
                title=''),
        )],

        'layout': dict(
            title='Gender Inequality Index',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection=dict(
                    type='Mercator'
                )
            )
        )

    }


def generate_gender_inequality_vs_internet_use_chart(selected_country):
    """
    This function generates the gender inequality vs internet use chart in the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: gender inequality vs internet use chart
    """
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    yaxis = df.loc[(df['Name'].isin(pd.Series(['ind.internet.female', 'GII']))) & (df['Region'] == rgn)]
    dg = yaxis.groupby(['Name', 'Country']).aggregate({'Year': 'max'}).reset_index()
    yaxis = dg.merge(yaxis[['Name', 'Country', 'Year', 'value']], how='left', on=['Name', 'Country', 'Year'])
    yaxis = yaxis[['Name', 'Country', 'value']].pivot('Country', 'Name', 'value').reset_index()
    yaxis = yaxis.dropna(axis=0)
    # x1 = yaxis['GII']
    # y1 = yaxis['ind.internet.female']
    # cts = yaxis['Country']

    x3 = yaxis.loc[(yaxis['Country'] == selected_country)]
    if (x3.shape[0] > 0):
        x4 = x3['GII']
        y4 = x3['ind.internet.female']
        ct = selected_country
    else:
        x4 = np.nan
        y4 = np.nan
        ct = selected_country

    return {
        'data': [
            go.Scatter(  # All data
                x=yaxis['GII'] if x3.shape[0] == 0 else yaxis.loc[yaxis['Country'] != ct, 'GII'],
                y=yaxis['ind.internet.female'] if x3.shape[0] == 0 else yaxis.loc[
                    yaxis['Country'] != ct, 'ind.internet.female'],
                mode='markers',
                text=yaxis['Country'] if x3.shape[0] == 0 else yaxis.loc[yaxis['Country'] != ct, 'Country'],
                ## textposition = 'bottom center',
                name=rgn,
                marker=dict(
                    color=('rgb(56, 192, 225)'),
                    size=10)
            ),
            go.Scatter(  # Country data
                x=x4,
                y=y4,
                mode='markers+text',
                text=ct,
                textposition='bottom center',
                name=ct,
                marker=dict(
                    color=('rgb(222,184,65)'),
                    size=15)
            )
        ],
        ## Edit the layout
        'layout': go.Layout(
            title='Gender inequality vs internet use',
            titlefont=dict(size=24,
                           color='#38C0E1',
                           family='Raleway'),
            xaxis=dict(title='Gender Inequality Index',
                       range=[0, 1]),
            yaxis=dict(title='% of female population using internet',
                       range=[0, 100]),
            showlegend=True,
            annotations=[
                dict(
                    x=0.0,
                    y=-.3,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
                    text='Source: ' + df.loc[df['Name'] == 'GII', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                        df.loc[df['Name'] == 'FotN', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                    showarrow=False,
                    font=dict(family='Raleway')
                ),
                dict(
                    x=.05,
                    y=.05,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='No data for ' + ct if x3.shape[0] == 0 else '',
                    showarrow=False,
                    font=dict(family='Raleway')
                ),
                dict(
                    x=0.0,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='More equal',
                    showarrow=False,
                    font=dict(family='Raleway')
                ),
                dict(
                    x=0.9,
                    y=-.15,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='Less equal',
                    showarrow=False,
                    font=dict(family='Raleway')
                )
            ]

        )
    }

def generate_women_in_parliament_line_chart(selected_country,title_text):
    """
    This function generates the women in Parliament chart the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: women in Parliament chart
    """
    ## Create and style traces
    filtered_df = getCountryData(selected_country, 'SG.GEN.PARL.ZS')
    ## Compute regional average weighted by country population
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    regional = weightedAverage(rgn, 'SG.GEN.PARL.ZS')

    src_text = 'Source: ' + df.loc[df['Name'] == 'SG.GEN.PARL.ZS', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == 'SG.GEN.PARL.ZS', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington'

    return {
        'data': [
            go.Scatter(  # Country data
                x=filtered_df['Year'],
                y=filtered_df['value'],
                text=filtered_df['Country'],
                name=filtered_df['Country'].tolist()[0],
                line=dict(
                    color=(PLOT_COLORS["country"]),
                    width=4),
                marker=dict(
                    size=MARKER_SIZE
                )
            ),
            go.Scatter(  # Regional average
                x=regional['Year'],
                y=regional['w_avg'],
                text=rgn,
                name=rgn,
                line=dict(
                    color=(PLOT_COLORS["region"]),
                    width=4),
                marker=dict(
                    size=MARKER_SIZE
                )
            )
        ],

        ## Edit the layout
        'layout': go.Layout(
            title=title_text,
            titlefont=dict(size=20, color='#38C0E1', family='Raleway'),
            font=dict(family='Raleway', size=13),
            height=PLOT_HEIGHT,
            width=500,
            xaxis=dict(title='',
                       range=[2005.5, 2018.5],
                       tick0=2006,
                       tickfont=dict(family='Raleway',size=14),
                       dtick=2),
            yaxis=dict(title='Women in Parliament (%)',
                       range=[0, 100],
                       tickfont=dict(family='Raleway',size=14)),
            legend=dict(x=.1,
                        y=1 if regional['w_avg'].tolist()[0] < 40 else 0.1),
            annotations=[
                dict(
                    x=2005.5,
                    y=-.35,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
                    text=src_text,
                    showarrow=False,
                    font=dict(family='Raleway')
                ),
                dict(
                    x=2006,
                    y=.05,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='No data for ' + filtered_df['Country'].tolist()[0] if sum(
                        filtered_df['value'].notnull()) == 0 else '',
                    showarrow=False,
                    font=dict(family='Raleway')
                )
            ]
        )
    }

def generate_women_in_stem_line_chart(selected_country,title_text):
    """
    This function generates the women in STEM chart the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: women in STEM chart
    """
    ## Create and style traces
    filtered_df = getCountryData(selected_country, 'women.in.stem')
    ## Compute regional average weighted by country population
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    regional = weightedAverage(rgn, 'women.in.stem')
    src_text = 'Source: ' + df.loc[df['Name'] == 'women.in.stem', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == 'women.in.stem', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington'

    return {
        'data': [
            go.Scatter(  # Country data
                x=filtered_df['Year'],
                y=filtered_df['value'],
                text=filtered_df['Country'],
                name=filtered_df['Country'].tolist()[0],
                line=dict(
                    color=(PLOT_COLORS["country"]),
                    width=4),
                marker=dict(
                    size=MARKER_SIZE
                )
            ),
            go.Scatter(  # Regional average
                x=regional['Year'],
                y=regional['w_avg'],
                text=rgn,
                name=rgn,
                line=dict(
                    color=(PLOT_COLORS["region"]),
                    width=4),
                marker=dict(
                    size=MARKER_SIZE
                )
            )
        ],

        ## Edit the layout
        'layout': go.Layout(
            title=title_text,
            titlefont=dict(size=20, color='#38C0E1', family='Raleway'),
            font=dict(family='Raleway', size=13),
            height=PLOT_HEIGHT,
            width=500,
            xaxis=dict(title='',
                       range=[2005.5, 2018.5],
                       tick0=2006,
                       tickfont=dict(family='Raleway',size=14),
                       dtick=2),
            yaxis=dict(title='Women in STEM (%)',
                       range=[0, 100],
                       tickfont=dict(family='Raleway',size=14)),
            legend=dict(x=.1,
                        y=1 if regional['w_avg'].tolist()[0] < 40 else 0.1),
            annotations=[
                dict(
                    x=2005.5,
                    y=-.35,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
                    text=src_text,
                    showarrow=False,
                    font=dict(family='Raleway')
                ),
                dict(
                    x=2006,
                    y=.05,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    text='No data for ' + filtered_df['Country'].tolist()[0] if sum(
                        filtered_df['value'].notnull()) == 0 else '',
                    showarrow=False,
                    font=dict(family='Raleway')
                )
            ]
        )
    }

def generate_educational_attainment_basic_level_by_gender_bar_chart(selected_country,title_text):
    """
    This function generates educational attainment basic level by gender bar chart,
    :param selected_country: selected country from dropdown
    :return: educational attainment by gender bar chart
    """
    # Women Data
    primary_women = getCountryData(selected_country,'primary.female')
    women_df_final = primary_women.sort_values('Year')
    women_df_final['New_Name'] = PLOT_COLORS["women"]


    # Men Data
    primary_men = getCountryData(selected_country,'primary.male')
    men_df_final = primary_men.sort_values('Year')
    men_df_final['New_Name'] = PLOT_COLORS["men"]
    max_val = max(df.loc[df['Name'].str.contains("primary.female")==True,'value'].tolist())

##    primary_total = getCountryData(selected_country,'primary.total')
##    total_df_final = primary_total.sort_values('Year')
##    total_df_final['New_Name'] = '#38C0E1'

    
##    lower_secondary_women = getCountryData(selected_country, 'lower.secondary.female')
##    lower_secondary_women.sort_values('Year',inplace=True)
##    women_df_final = primary_women.append(lower_secondary_women, ignore_index=True)
##    women_df_final.loc[(women_df_final['Name'] == "primary.female"),['New_Name']] = 'Primary'
##    women_df_final.loc[(women_df_final['Name'] == 'lower.secondary.female'),['New_Name']] = 'Lower Secondary'
##    lower_secondary_men = getCountryData(selected_country, 'lower.secondary.male')
##    lower_secondary_men.sort_values('Year',inplace=True)
##    men_df_final = primary_men.append(lower_secondary_men, ignore_index=True)

##    men_df_final.loc[(men_df_final['Name'] == 'primary.male'),['New_Name']] = 'Primary'
##    men_df_final.loc[(men_df_final['Name'] == 'lower.secondary.male'),['New_Name']] = 'Lower Secondary'

    
    #primary_women = primary_women.tail(1)
    #lower_secondary_women = lower_secondary_women.tail(1)
##    upper_secondary_women = getCountryData(selected_country, 'upper.secondary.female')
##    upper_secondary_women.sort_values('Year',inplace=True)
##    upper_secondary_women = upper_secondary_women.tail(1)
##    bachelors_women = getCountryData(selected_country, 'bachelors.female')
##    bachelors_women.sort_values('Year',inplace=True)
##    bachelors_women = bachelors_women.tail(1)
##    women_df2 = upper_secondary_women.append(bachelors_women, ignore_index=True)
##    women_df_final = women_df1.append(women_df2,ignore_index=True)
##    women_df_final.loc[(women_df_final['Name'] == 'upper.secondary.female'),['New_Name']] = 'Upper Secondary'
##    women_df_final.loc[(women_df_final['Name'] == 'bachelors.female'),['New_Name']] = 'Bachelors'
    #primary_men = primary_men.tail(1)
    #lower_secondary_men = lower_secondary_men.tail(1)
##    upper_secondary_men = getCountryData(selected_country, 'upper.secondary.male')
##    upper_secondary_men.sort_values('Year',inplace=True)
##    upper_secondary_men = upper_secondary_men.tail(1)
##    bachelors_men = getCountryData(selected_country, 'bachelors.male')
##    bachelors_men.sort_values('Year',inplace=True)
##    bachelors_men = bachelors_men.tail(1)
##    men_df2 = upper_secondary_men.append(bachelors_men, ignore_index=True)
##    men_df_final = men_df1.append(men_df2,ignore_index=True)
##    men_df_final.loc[(men_df_final['Name'] == 'upper.secondary.male'),['New_Name']] = 'Upper Secondary'
##    men_df_final.loc[(men_df_final['Name'] == 'bachelors.male'),['New_Name']] = 'Bachelors'


    # Plot the graph
    trace1 = go.Bar(
            x = list(women_df_final['Year']),
            y = list(women_df_final['value']),
            name='Women',
            width=0.4,
            opacity = 0.5,
            marker=dict(
            color=women_df_final['New_Name'],
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,
            )
        )
    )
    trace2 = go.Bar(
            x = list(men_df_final['Year']),
            y = list(men_df_final['value']),
            name='Men',
            opacity = 0.5,
            width = 0.4,
            marker=dict(
            color=men_df_final['New_Name'],
            line=dict(
                color='rgb(8,48,107)',
                width=0.3,
            )
        )

        )
##    trace3 = go.Scatter(
##            x = list(total_df_final['Year']),
##            y = list(total_df_final['value']),
##            name='Total'
##            #color = total_df_final['New_Name'],
##        )
    
    layout=go.Layout(
            title=title_text, titlefont=dict(size=20, color=PLOT_COLORS["title"], family='Raleway'),
            font=dict(family='Raleway', size=13),
            barmode='group',
            yaxis=dict(range=[0, max_val]),
            xaxis=dict(range=[2005.5,2016.5],dtick=2),
            height=PLOT_HEIGHT,
            width = 500.5,
            annotations=[
                dict(
                text="NO DATA AVAILABLE",
                x=0.5,
                showarrow=False,
                visible=True if (women_df_final['value'].isnull().all()) else False
                ),
                dict(
                    x=-0.1,
                    y=-.35,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    #xanchor='left',
                    align='left',
text='Source: ' + df.loc[df['Name'] == 'primary.female', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
                        df.loc[df['Name'] == 'primary.female', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington',
                    showarrow=False,
                    font=dict(family='Raleway')
                )
            ]
        )

    fig = go.Figure(data=[trace1,trace2], layout=layout)
    
    return fig

    
def generate_educational_attainment_by_gender_bar_chart(selected_country,title_text):
    """
    This function generates the educational attainment by gender bar chart the gender dashboard.

    :param selected_country: selected country from dropdown
    :return: educational attainment by gender bar chart
    
    """
    ## Create and style traces
    primary_f = getCountryData(selected_country, 'primary.female')
    primary_m = getCountryData(selected_country, 'primary.male')
    lower_secondary_f = getCountryData(selected_country, 'lower.secondary.female')
    lower_secondary_m = getCountryData(selected_country, 'lower.secondary.male')
    upper_secondary_f = getCountryData(selected_country, 'upper.secondary.female')
    upper_secondary_m = getCountryData(selected_country, 'upper.secondary.male')
    bachelors_f = getCountryData(selected_country, 'bachelors.female')
    bachelors_m = getCountryData(selected_country, 'bachelors.male')

    src_text = 'Source: ' + df.loc[df['Name'] == 'primary.female', 'Source'].tail(1).tolist()[0] + ' (' + str(int(
        df.loc[df['Name'] == 'primary.female', 'db_year'].tail(1).tolist()[0])) + ')<br>Technology & Social Change Group, University of Washington'

    # Create the graph with subplots

    fig = tools.make_subplots(rows=1, cols=primary_m.shape[0], shared_yaxes=True, horizontal_spacing=0.025,
                              subplot_titles=primary_m['Year'].tolist())
    i = 0
    year = int(primary_m['Year'].iloc[i])
    trace1 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                    y=[primary_m.loc[primary_m['Year'] == year, 'value'].tolist()[0],
                       primary_f.loc[primary_f['Year'] == year, 'value'].tolist()[0]],
                    name='Primary',
                    opacity=0.6,
                    marker=dict(
                        color='lightblue'
                    ))
    trace2 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                    y=[lower_secondary_m.loc[lower_secondary_m['Year'] == year, 'value'].tolist()[0],
                       lower_secondary_f.loc[lower_secondary_f['Year'] == year, 'value'].tolist()[0]],
                    name='Lower Secondary',
                    opacity=0.6,
                    marker=dict(
                        color='green'
                    ))
    trace3 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                    y=[upper_secondary_m.loc[upper_secondary_m['Year'] == year, 'value'].tolist()[0],
                       upper_secondary_f.loc[upper_secondary_f['Year'] == year, 'value'].tolist()[0]],
                    name='Upper Secondary',
                    marker=dict(
                        color='grey'
                    ))
    trace4 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                    y=[bachelors_m.loc[bachelors_m['Year'] == year, 'value'].tolist()[0],
                       bachelors_f.loc[bachelors_f['Year'] == year, 'value'].tolist()[0]],
                    name='Bachelors',
                    marker=dict(
                        color='red'
                    ))
    fig.append_trace(trace1, 1, i + 1)
    fig.append_trace(trace2, 1, i + 1)
    fig.append_trace(trace3, 1, i + 1)
    fig.append_trace(trace4, 1, i + 1)

    for i in range(1, primary_m.shape[0] - 1):
        year = int(primary_m['Year'].iloc[i])
        trace1 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                        y=[primary_m.loc[primary_m['Year'] == year, 'value'].tolist()[0],
                           primary_f.loc[primary_f['Year'] == year, 'value'].tolist()[0]],
                        name='Primary',
                        opacity=0.6,
                        marker=dict(
                            color='lightblue'
                        ),
                        showlegend=False)
        trace2 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                        y=[lower_secondary_m.loc[lower_secondary_m['Year'] == year, 'value'].tolist()[0],
                           lower_secondary_f.loc[lower_secondary_f['Year'] == year, 'value'].tolist()[0]],
                        name='Lower Secondary',
                        opacity=0.6,
                        marker=dict(
                            color='green'
                        ),
                        showlegend=False)
        trace3 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                        y=[upper_secondary_m.loc[upper_secondary_m['Year'] == year, 'value'].tolist()[0],
                           upper_secondary_f.loc[upper_secondary_f['Year'] == year, 'value'].tolist()[0]],
                        name='Upper Secondary',
                        marker=dict(
                            color='grey'
                        ),
                        showlegend=False)
        trace4 = go.Bar(x=['Men '+str(year), 'Women '+str(year)],
                        y=[bachelors_m.loc[bachelors_m['Year'] == year, 'value'].tolist()[0],
                           bachelors_f.loc[bachelors_f['Year'] == year, 'value'].tolist()[0]],
                        name='Bachelors',
                        marker=dict(
                            color='red'
                        ),
                        showlegend=False)
        fig.append_trace(trace1, 1, i + 1)
        fig.append_trace(trace2, 1, i + 1)
        fig.append_trace(trace3, 1, i + 1)
        fig.append_trace(trace4, 1, i + 1)
        
        fig['layout']['xaxis'+ str(i)].update(tickangle=45)
        if i == primary_m.shape[0] - 2:
            fig['layout']['xaxis'+ str(i+1)].update(tickangle=45)
            

        ## fig.append_trace(trace3, 1, 3)
    fig['layout']['yaxis'].update(title='Percent', range=[0, 100])
    fig['layout'].update(height=450,showlegend=True, barmode='stack')
    fig['layout'].update(title=title_text,font=dict(family='Raleway',size=14))
    fig['layout'].update(legend=dict(x=1,y=1,orientation='v'))
    fig['layout']['annotationdefaults'].update(font=dict(size=14,family='Raleway'))
    fig['layout'].update(annotations=[dict(x=0.0, y=-.31, text=src_text,
                                           xanchor='left',opacity=0.4,showarrow=False,font=dict(size=14,family='Raleway'))])
    fig['layout']['title'].update(font=dict(size=20,color=PLOT_COLORS['title']))
    
    return fig


def generate_3g_mobile_coverage_bar_and_line_chart(selected_country, indicator, title, ylabel):
    ## Create and style traces
    filtered_df = getCountryData(selected_country, indicator)

    ## Compute regional average weighted by country population
    rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
    regional = weightedAverage(rgn, indicator)
    return {
        'data': [
            html.Div(children=""),
            go.Bar(
                x=filtered_df['Year'],
                y=filtered_df['value'],
                orientation='v',
                # text = filtered_df['Country'],
                textposition='auto',
                name=selected_country,
                width=0.5,
                marker=dict(
                    color=(PLOT_COLORS["country"]),
                    line=dict(
                        color=(PLOT_COLORS["country"]),
                        width=0.0,

                    )
                )),
            go.Scatter(  # Regional average
                x=regional['Year'],
                y=regional['w_avg'],
                text=rgn,
                name=rgn,

                line=dict(
                    color=(PLOT_COLORS["region"]),
                    width=4),
                marker=dict(
                    size=MARKER_SIZE
                )
            )
        ],

        ## Edit the layout
        'layout': go.Layout(
            title=title, titlefont=dict(size=20, color='#38C0E1', family='Raleway'),
            xaxis=dict(title='',
                       range=[2005.5, 2018.5],
                       tick0=2006,
                       dtick=1),
            yaxis=dict(title=ylabel,
                       range=[0, 100]),
            showlegend = True,
            legend=dict(x=0.05,
                        y=1),
            autosize=True,
            font=dict(family='Raleway', size=13),
            width= 500,
            annotations=[
                dict(
                    x=2005.5,
                    y=-.3,
                    xref='x',
                    axref='x',
                    yref='paper',
                    ayref='pixel',
                    xanchor='left',
                    align='left',
text='Source: ' + df.loc[df['Name'] == 'at.least.3G.coverage', 'Source'].tail(1).tolist()[
                        0] + ' (' + str(int(
                        df.loc[df['Name'] == 'at.least.3G.coverage', 'db_year'].tail(1).tolist()[0])) + ') <br>Technology & Social Change Group, University of Washington',
                    showarrow=False,font=dict(family='Raleway')
                )
            ]
        ),
        
    }
