# -*- coding: cp1252 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash

from app import app
from app import df
import utils
from apps import navbar

layout = html.Div(
    id="freedom-dashboard",
    children=[
        navbar.layout,
        html.Div(className="row main-container",
                 children=[

                     html.Div(className="sidebar col col-md-4 col-lg-3",
                              style={},  # override bootstrap column padding
                              children=[
                                  html.Div(
                                      id="sidebar",
                                      className="quick-look",
                                      children=[
                                          # ----- country icon -----
                                          html.Img(
                                              id='country-icon', style={'width': '80%', 'marginLeft': '10%'}),
                                          html.Div(id="sub-region-list"),
                                          utils.generate_quick_look_layout(
                                              dashboard="freedom", sections=4)
                                      ],
                                  ),  # ----- /sidebar -----
                                   html.Div(
                                      id="ccInfo",
                                      children=(
                                          html.A(
                                              rel="license",
                                              href="http://creativecommons.org/licenses/by-nc/4.0/",
                                              children=[
                                                  html.Img(
                                                      alt="Creative Commons License",
                                                      src="https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-nc.svg"
                                                  )
                                              ]
                                          ),
                                          html.P(
                                              children=[
                                                  html.Span(
                                                      children="This work is licensed under a "
                                                  ),
                                                  html.A(
                                                      rel="license", 
                                                      href="http://creativecommons.org/licenses/by-nc/4.0/",
                                                      children="Creative Commons Attribution-NonCommercial 4.0 International License"
                                                  )
                                              ]
                                          )
                                      )
                                  )
                              ]),

                     html.Div(className="col col-md-8 col-lg-9",
                              children=[
                                  html.Div(
                                      className="container dashboard-container",
                                      children=[

                                                html.Div(className="jumbotron",
                                                   children=[
                                                       html.Div([
                                                           html.Strong("The Development and Access to Information (DA2i) dashboards"),
                                                           html.Span(" explore key indicators related to meaningful access and use of information in the context of the "),
                                                           html.A(href="https://sustainabledevelopment.un.org/sdgs", target="_blank", children="UN 2030 Agenda."),
                                                           html.Em(' Select a country'),
                                                           html.Span(" from the dropdown menu to explore its progress in three critical areas: Connectivity, Freedom and Gender Equity."),
                                                           html.Br(),
                                                           html.Br(),
                                                           html.Span("Hover over charts to reveal a menu for interactions such as download or zoom in the top right of the chart."),
                                                           html.Br(),
                                                           html.Br(),
                                                           html.Span("Visit the "),
                                                           html.A(children="DA2i website", target="_blank", href="https://da2i.ifla.org/"),
                                                           html.Span(' for more information on the project and its rights-based approach to meaningful access to information. '),
                                                           html.Span('Visit the open source '),
                                                           html.A(children='Github repo', target='_blank', href="https://github.com/tascha/DA2I-Dashboard"),
                                                           html.Span(' for acknowledgements and technical resources.'),
                                                           html.Br(),
                                                           html.Br(),
                                                           html.Span('The Dashboards, built by '),
                                                           html.A(target='_blank', href='https://tascha.uw.edu/', children="University of Washington's Technology & Social Change Group"),
                                                           html.Span(", are part of a larger initiative in collaboration with the "),
                                                           html.A(target='_blank', href='https://www.ifla.org/', children="International Federation of Library Associations and Institutions (IFLA)"),
                                                           html.Span("."),
                                                       ]),
                                                   ]),


                                          html.Div(
                                              className="container dashboard-container",
                                              children=[
                                                  html.H1(
                                                      className="dashboard-title",
                                                      children="Freedom Dashboard"
                                                  ),

                                                  html.P(
                                                      className="dashboard-description",
                                                      children="The Freedom Dashboard explores the legal context, policy environment and "
                                                      "the extent to which countries have implemented the kinds of rights-based goals and equitable "
                                                      "and participatory practices that support meaningful access to information. This includes guaranteeing "
                                                      "the rights of people to freedom of expression, association, political participation, civic action, "
                                                      "and online privacy and safety."
                                                  ),

                                              ]
                                          ),

                                          # ----- story one -----
                                          html.Div(

                                              # use bootstrap container class to center and provide horizontal padding
                                              className="container story-container",
                                              children=[
                                                  html.H2(
                                                      className="story-title",
                                                      children="Freedom in the country"
                                                  ),
                                                  html.Div(className="story-description",
                                                           children=[
                                                               html.P(
                                                                   className="story-description",
                                                                   children="Freedom House's Freedom in the World Index combines two separate ratings on political rights and civil liberties:"
                                                               ),
                                                               html.Ul([
                                                                   html.Div(html.Li([html.H1(['Political Rights Rating: '], style={'fontSize': '18px',
                                                                                                                                   'display': 'inline',
                                                                                                                                   'fontFamily': 'Raleway',
                                                                                                                                   'color': '#38C0E1'}),
                                                                                     "Assesses people's ability to participate in the electoral process, ensure political pluralism, and hold the government accountable."], style={'list-style-position': 'outside',
                                                                                                                                                             'marginLeft': '18px'})),
                                                                   html.Div(html.Li([html.H1(['Civil Liberties Rating: '], style={'fontSize': '18px',
                                                                                                                                  'display': 'inline',
                                                                                                                                  'fontFamily': 'Raleway',
                                                                                                                                  'color': '#38C0E1'}),
                                                                                     "Assesses the extent to which people can exercise freedom of expression and belief, whether they can freely associate and assemble, and whether there exists an equitable rule of law that protects social and economic freedoms."], style={'list-style-position': 'outside',
                                                                                                                                                   'marginLeft': '18px'}))

                                                               ]),
                                                           ]),
                                                  # dcc.Graph(id="aggregate-freedom-sparklines-bar-slider-chart"),
                                                  html.Div(
                                                      className="row",
                                                      children=[
                                                          html.Div(
                                                              className="",
                                                              children=[
                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      id="aggregate-freedom-most-recent-rating"
                                                                  ),


                                                                  # ----- aggregate freedom chart -----
                                                                  html.Div(
                                                                      className='',
                                                                      children=dcc.Graph(
                                                                          id='aggregate-freedom-sparklines-bar-slider-chart')
                                                                  ),

                                                              ]
                                                          ),

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[
                                                                  html.Div(
                                                                      className='indicator-chart',
                                                                      children=dcc.Graph(
                                                                          id='aggregate-freedom-sparklines-bar-chart')
                                                                  ),
                                                              ]
                                                          ),
                                                      ]),


                                                  # ----- story one indicator section -----
                                                  html.Div(
                                                      className="row",
                                                      children=[

                                                          # ----- political rights rating ------
                                                          html.Div(
                                                              className="political-civil-chart",
                                                              children=dcc.Graph(id='political-rights-rating-chart'
                                                                                 )
                                                          ),
                                                          html.Div(
                                                              className="pc-indicator-table",
                                                              id='political-rights-rating-table'
                                                          ),


                                                          # ----- civil liberties rating -----
                                                          html.Div(
                                                              className="political-civil-chart",
                                                              children=dcc.Graph(id="civil-liberties-rating-chart"
                                                                                 )
                                                          ),
                                                          html.Div(
                                                              className="pc-indicator-table",
                                                              id="civil-liberties-rating-table"
                                                          ),

                                                      ])
                                              ]
                                          ),


                                          # ----- story two -----
                                          html.Div(

                                              # use bootstrap container class to center and provide horizontal padding
                                              className="container story-container",
                                              children=[
                                                  html.H2(
                                                      className="story-title",
                                                      children="Freedom on the Net"
                                                  ),
                                                  html.P(
                                                      className="story-description",
                                                      children="Freedom on the Net rating tracks obstacles to internet access, limits on internet content, and violations of user rights in the country."
                                                  ),
                                                  # dcc.Graph(id="freedom-on-the-net-sparklines-bar-chart"),
                                                  html.Div(
                                                      className="row",
                                                      children=[
                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[
                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      id="aggregate-freedom-on-the-net-most-recent-rating"
                                                                  ),
                                                                  # -----freedom on the net chart -----
                                                                  html.Div(
                                                                      className='',
                                                                      children=dcc.Graph(
                                                                          id='freedom-on-the net-sparklines-bar-slider-chart')
                                                                  ),

                                                              ]
                                                          ),

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[
                                                                  html.Div(
                                                                      className='indicator-chart',
                                                                      children=dcc.Graph(
                                                                          id='freedom-on-the-net-sparklines-bar-chart')
                                                                  ),
                                                              ]
                                                          ),
                                                      ]),

                                                  # ----- story two indicator section -----
                                                  html.Div(
                                                      className="row",
                                                      children=[
                                                          html.Div(
                                                              className="row",
                                                              children=[

                                                                  # ----- regional comparison: percent using internet vs freedom on net chart -----
                                                                  html.Div(
                                                                      className="fotn-indicator-chart",
                                                                      children=dcc.Graph(id='percent-using-internet-vs-freedom-on-net-chart'
                                                                                         )
                                                                  ),
                                                                  html.Div(
                                                                      className="indicator-table",
                                                                      id='percent-using-internet-vs-freedom-on-net-table'
                                                                  ),
                                                              ]
                                                          ),
                                                      ]
                                                  ),

                                              ]
                                          ),

                                          html.Div(className="footer")
                                      ])
                              ])

                 ])
    ])


# ----- quick look section callbacks -----

@app.callback(
    dash.dependencies.Output('freedom-quick-look-section-1', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_1(selected_country):
    indicator = "FitW.total.aggregate.score"
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == indicator]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    score = int(df_filtered['value'].tail(1).tolist()[
                0]) if len(df_filtered) != 0 else 'NA'
    year = str(df_filtered['Year'].tail(1).tolist()[
               0]) if len(df_filtered) != 0 else 'NA'

    if score != "NA":
        if score > 60:
            rating = "Free"
            color = '#10C80A'
            score = str(score)+'/100'
        elif score > 30:
            rating = "Partly Free"
            color = '#FFC300'
            score = str(score)+'/100'
        else:
            rating = "Not Free"
            color = '#9370DB'
            score = str(score)+'/100'
    else:
        rating = "NO DATA"
        color = "#000000"

    return html.Table(
        # Header

        [html.Tr([html.Th('Freedom Score:', style={'textAlign': 'left', 'width': '80%'}),
                   html.Th(str(score),
                           style={'marginLeft': 'auto', 'textAlign': 'right', 'width': '20%'})],
                  style={'borderTop': '1px solid light-grey',
                         'fontSize': '16px',
                         'color': 'white',
                         'width': '100%'})] +


        [html.Tr([html.Th('Rating:', style={'textAlign': 'left', 'width': '80%'}),
                   html.Th(str(rating),
                           style={'marginLeft': 'auto', 'textAlign': 'right', 'width': '20%'})],
                  style={'borderTop': '1px solid light-grey',
                         'fontSize': '16px',
                         'color': 'white',
                         'width': '100%'})],
        
        style={'width': '100%'}
    )


@app.callback(
    dash.dependencies.Output('freedom-quick-look-section-2', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_2(selected_country):
    prr = df.loc[(df.Country == selected_country) & (
        df.Name == 'FitW.PRR.aggregate.score')]
    prr.sort_values('Year', inplace=True)
    if (prr.shape[0] > 0):
        value = str(int(prr['value'].tail(1).tolist()[0])) + '/40'
        max_year = prr['Year'].tail(1).tolist()[0]
        rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
        change = int(prr.iloc[-1, 2]) - int(prr.iloc[-2, 2])
    else:
        value = 'NA'
        max_year = 'NA'
        rank = 'NA'
        change = 'NA'

    return html.Table(
        # Header

        [html.Tr([html.Th('Political Rights:', style={'textAlign': 'left'}),
                  html.Th(value,
                          style={'marginLeft': 'auto', 'textAlign': 'right'})],
                 style={'borderTop': '1px solid light-grey',
                        'fontSize': '16px',
                        'color': 'white'})],

        style={'width': '100%'}
    )


@app.callback(
    dash.dependencies.Output('freedom-quick-look-section-3', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_3(selected_country):
    prr = df.loc[(df.Country == selected_country) & (
        df.Name == 'FitW.CLR.aggregate.score')]
    prr.sort_values('Year', inplace=True)
    if (prr.shape[0] > 0):
        value = str(int(prr['value'].tail(1).tolist()[0])) + '/60'
        max_year = prr['Year'].tail(1).tolist()[0]
        rgn = df.loc[df.Country == selected_country, 'Region'].tolist()[0]
        change = int(prr.iloc[-1, 2]) - int(prr.iloc[-2, 2])
    else:
        value = 'NA'
        max_year = 'NA'
        rank = 'NA'
        change = 'NA'

    return html.Table(
        # Header

        [html.Tr([html.Th('Civil Liberties:', style={'textAlign': 'left'}),
                  html.Th(value,
                          style={'marginLeft': 'auto', 'textAlign': 'right'})],
                 style={'borderTop': '1px solid light-grey',
                        'fontSize': '16px',
                        'color': 'white'})],

        style={'width': '100%'}
    )


@app.callback(
    dash.dependencies.Output('freedom-quick-look-section-4', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_4(selected_country):
    indicator = "FotN"

    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == indicator]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])
    df_filtered.sort_values('Year', inplace=True)

    score = int(df_filtered['value'].tail(1).tolist()[
                0]) if len(df_filtered) != 0 else 'NA'
    year = str(df_filtered['Year'].tail(1).tolist()[
               0]) if len(df_filtered) != 0 else 'NA'

    if score != "NA":
        if score > 70:
            rating = "Free"
            color = '#10C80A'
            score = str(score)+'/100'
        elif score > 40:
            rating = "Partly Free"
            color = '#FFC300'
            score = str(score)+'/100'
        else:
            rating = "Not Free"
            color = '#9370DB'
            score = str(score)+'/100'
    else:
        rating = "NA"
        color = "#000000"

    return html.Table(
        # Header

        [html.Tr([html.Th('Freedom Net:', style={'textAlign': 'left', 'width': '80%'}),
                   html.Th(str(score),
                           style={'marginLeft': 'auto', 'textAlign': 'right', 'width': '20%'})],
                  style={'borderTop': '1px solid light-grey',
                         'fontSize': '16px',
                         'color': 'white',
                         'width': '100%'})] +
                         
        [html.Tr([html.Th('Rating:', style={'textAlign': 'left', 'width': '80%'}),
                html.Th(str(rating),
                        style={'marginLeft': 'auto', 'textAlign': 'right', 'width': '20%'})],
                style={'borderTop': '1px solid light-grey',
                        'fontSize': '16px',
                        'color': 'white',
                        'width': '100%'})],
        style={'width': '100%'}
    )

# @app.callback(
##    dash.dependencies.Output('freedom-quick-look-section-4', 'children'),
# [dash.dependencies.Input('country-dropdown', 'value')])
# def update_quick_look_section_4(selected_country):
##    ind_internet = df.loc[(df.Country == selected_country) & (df.Name == 'hh.internet')]
##    ind_internet.sort_values('Year', inplace=True)
##
# ind_internet = str(int(round(ind_internet['value'].tail(1).tolist()[0]))) + '%' if (
# ind_internet.shape[0] > 0) else 'NA'
##
# return html.Table(
# Header
##
# [html.Tr([html.Th('Households with Internet:', style={'textAlign': 'left'}),
# html.Th(ind_internet,
# style={'marginLeft': 'auto', 'textAlign': 'right'})],
# style={'borderTop': '1px solid light-grey',
# 'fontSize': '16px',
# 'color': 'white'})],
##
##        style={'width': '100%'}
# )


# ----- freedom callbacks -----

# ----- aggregate freedom most recent rating -----
@app.callback(
    dash.dependencies.Output(
        "aggregate-freedom-most-recent-rating", "children"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def calculate_freedom_rating(selected_country):
    indicator = "FitW.total.aggregate.score"
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == indicator]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    score = df_filtered['value'].tail(1).tolist(
    )[0] if len(df_filtered) != 0 else 'NO DATA'
    year = str(int(df_filtered['Year'].tail(1).tolist()[0])) if len(
        df_filtered) != 0 else 'NA'

    if score != "NO DATA":
        if score > 70:
            rating = "Free"
            color = '#10C80A'
        elif score > 30:
            rating = "Partly Free"
            color = '#FFC300'
        else:
            rating = "Not Free"
            color = '#9370DB'
    else:
        rating = "NO DATA"
        color = "#000000"

    return html.Table(
        # Header

        # [html.Tr([html.Th('Freedom Rating and Score' + ' (' + year + '):', style={'colspan':'2','textAlign': 'left'})],
        # style={'fontSize': '18px', 'fontFamily':'Raleway',
        # 'color': '#38C0E1',
        # 'padding-bottom':'30px'})] +
        [html.Tr([html.Th('Freedom Rating' + ' (' + year + '):', style={'fontSize': '18px', 'textAlign': 'left', 'color': '#38C0E1'}),
                  html.Td(rating,
                          style={'fontSize': '22px', 'textAlign': 'left', 'color': color})],
                 style={'fontFamily': 'Raleway',
                        'color': '#38C0E1',
                        'padding-bottom': '10px'})] +
        [html.Tr([html.Th('Freedom Score' + ' (' + year + '):', style={'fontSize': '18px', 'textAlign': 'left', 'color': '#38C0E1'}),
                  html.Td(score,
                          style={'fontSize': '22px', 'textAlign': 'left', 'color': color})],
                 style={'fontFamily': 'Raleway'})],
        style={'width': '100%'}
    )

# ----- aggregate freedom sparklines slider chart -----


@app.callback(
    dash.dependencies.Output(
        "aggregate-freedom-sparklines-bar-slider-chart", "figure"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def update_aggrete_freedom_sparklines_slider_bar_chart(selected_country):
    indicator_name = "FitW.total.aggregate.score"
    return utils.generate_sparklines_slider_bar_chart(selected_country=selected_country,
                                                      indicator=indicator_name,
                                                      title="")
# ----- aggregate freedom sparklines bar chart -----


@app.callback(
    dash.dependencies.Output(
        "aggregate-freedom-sparklines-bar-chart", "figure"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def update_aggregate_freedom_sparklines_bar_chart(selected_country):
    indicator_name = "FitW.total.aggregate.score"
    categories = [
        {
            "name": "Not Free",
            "range": [0, 30],
            "color": "#9370DB"
        },
        {
            "name": "Partly Free",
            "range": [31, 70],
            "color": "#FFC300",
        },
        {
            "name": "Free",
            "range": [71, 100],
            "color": "#10C80A"
        }
    ]
    return utils.generate_sparklines_bar_chart(selected_country=selected_country,
                                               indicator=indicator_name,
                                               title="Freedom Score Over the Years",
                                               categories=categories)



# ----- freedom in the world political rights rating -----

@app.callback(
    dash.dependencies.Output('political-rights-rating-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_political_rights_rating_chart(selected_country):
    return utils.generate_political_rights_rating_chart(selected_country=selected_country)


@app.callback(
    dash.dependencies.Output('political-rights-rating-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_political_rights_rating_table(selected_country):
    return utils.generate_freedom_in_the_world_table(selected_country=selected_country,
                                                     indicator="FitW.PRR.aggregate.score",
                                                     max_values=40,
                                                     indicator_name="Political Rights Score")

##
# ----- freedom in the world civil liberties rating -----


@app.callback(
    dash.dependencies.Output('civil-liberties-rating-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_civil_liberties_rating_chart(selected_country):
    return utils.generate_civil_liberties_rating_chart(selected_country)


@app.callback(
    dash.dependencies.Output('civil-liberties-rating-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_civil_liberties_rating_table(selected_country):
    return utils.generate_freedom_in_the_world_table(selected_country=selected_country,
                                                     indicator="FitW.CLR.aggregate.score",
                                                     max_values=60,
                                                     indicator_name="Civil Liberties Score")

# ----- % using internet vs freedom on the net -----

# ----- freedom on the net most recent rating -----


@app.callback(
    dash.dependencies.Output(
        "aggregate-freedom-on-the-net-most-recent-rating", "children"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def calculate_freedom_on_the_net_rating(selected_country):
    indicator = "FotN"

    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == indicator]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])
    df_filtered.sort_values('Year', inplace=True)

    score = df_filtered['value'].tail(1).tolist(
    )[0] if len(df_filtered) != 0 else 'NO DATA'
    year = str(int(df_filtered['Year'].tail(1).tolist()[0])) if len(
        df_filtered) != 0 else 'NA'

    if score != "NO DATA":
        if score > 70:
            rating = "Free"
            color = '#10C80A'
        elif score > 40:
            rating = "Partly Free"
            color = '#FFC300'
        else:
            rating = "Not Free"
            color = '#9370DB'
    else:
        rating = "NO DATA"
        color = "#000000"

    return html.Table(
        # Header

        # [html.Tr([html.Th('Freedom Rating and Score' + ' (' + year + '):', style={'colspan':'2','textAlign': 'left'})],
        # style={'fontSize': '18px', 'fontFamily':'Raleway',
        # 'color': '#38C0E1',
        # 'padding-bottom':'30px'})] +
        [html.Tr([html.Th('Freedom on Net Rating' + ' (' + year + '):', style={'fontSize': '18px', 'textAlign': 'left', 'color': '#38C0E1'}),
                  html.Td(rating,
                          style={'fontSize': '22px', 'textAlign': 'left', 'color': color})],
                 style={'fontFamily': 'Raleway',
                        'color': '#38C0E1',
                        'padding-bottom': '10px'})] +
        [html.Tr([html.Th('Freedom on Net Score' + ' (' + year + '):', style={'fontSize': '18px', 'textAlign': 'left', 'color': '#38C0E1'}),
                  html.Td(score,
                          style={'fontSize': '22px', 'textAlign': 'left', 'color': color})],
                 style={'fontFamily': 'Raleway'})],
        style={'width': '90%'}
    )

# ----- aggregate freedom on Net sparklines slider chart -----


@app.callback(
    dash.dependencies.Output(
        "freedom-on-the net-sparklines-bar-slider-chart", "figure"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def update_freedom_on_the_net_sparklines_slider_bar_chart(selected_country):
    indicator_name = "FotN"
    return utils.generate_sparklines_slider_bar_chart(selected_country=selected_country,
                                                      indicator=indicator_name,
                                                      title="")

# ----- aggregate freedom sparklines bar chart -----


@app.callback(
    dash.dependencies.Output(
        "freedom-on-the-net-sparklines-bar-chart", "figure"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def update_freedom_on_the_net_sparklines_bar_chart(selected_country):
    indicator_name = "FotN"
    categories = [
        {
            "name": "Not Free",
            "range": [0, 40],
            "color": "#9370DB"
        },
        {
            "name": "Partly Free",
            "range": [41, 70],
            "color": "#FFC300",
        },
        {
            "name": "Free",
            "range": [71, 100],
            "color": "#10C80A"
        }
    ]
    return utils.generate_sparklines_bar_chart(selected_country=selected_country,
                                               indicator=indicator_name,
                                               title="Freedom on the Net Over the Years",
                                               categories=categories)


@app.callback(
    dash.dependencies.Output(
        'percent-using-internet-vs-freedom-on-net-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_percent_using_internet_vs_freedom_on_net_chart(selected_country):
    return utils.generate_percent_using_internet_vs_freedom_on_net_chart(selected_country)


@app.callback(
    dash.dependencies.Output(
        'percent-using-internet-vs-freedom-on-net-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_percent_using_internet_vs_freedom_on_net_table(selected_country):
    return utils.generate_percent_using_internet_vs_freedom_on_net_table(selected_country)


@app.callback(
    dash.dependencies.Output(
        'country_percent-using-internet-vs-freedom-on-net-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country_percent_using_internet_vs_freedom_on_net_chart(selected_country):
    return utils.generate_country_percent_using_internet_vs_freedom_on_net_chart(selected_country)


@app.callback(
    dash.dependencies.Output(
        'country_percent-using-internet-vs-freedom-on-net-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country_percent_using_internet_vs_freedom_on_net_table(selected_country):
    return utils.generate_country_percent_using_internet_vs_freedom_on_net_table(selected_country)
