# -*- coding: utf-8 -*-

# Dash UI
import dash
import dash_core_components as dcc
import dash_html_components as html

# Global variables
from app import app
from app import df, Map

from apps import navbar

import functools
# Utility functions
import utils

# layout = html.Div(
#     id="testing-div",
#     children="this is just a test"
#     )

layout = html.Div(
    id="connectivity-dashboard",
    className='',
    children=[
        navbar.layout,

        html.Div(className="row main-container",
                 children=[
                     
                     html.Div(className="sidebar col col-md-4 col-lg-3 ",
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
                                              dashboard="connectivity", sections=4)
                                      ],
                                  ),  # ----- /sidebar -----

                                #   <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
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

                     html.Div(className="col col-md-8 col-lg-9 ",
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
                                          html.H1(
                                              className="dashboard-title",
                                              children="Connectivity Dashboard",
                                              style={'paddingTop': '30px'}
                                          ),

                                          html.P(
                                              className="dashboard-description",
                                              children="The Connectivity Dashboard explores the physical connectivity infrastructure "
                                              "available in the country, and how this infrastructure is used by the population. "
                                                       "It includes three categories of indicators: Access, Use, and Affordability"
                                          )
                                      ]
                                  ),

                                  # ----- access -----
                                  html.Div(

                                      # use bootstrap container class to center and provide horizontal padding
                                      className="container story-container",
                                      children=[
                                          html.H2(
                                              className="story-title",
                                              children="Access",
                                          ),

                                          html.P(
                                              className="story-description",
                                              children="The geographic coverage of wireless networks, as well as access to computers "
                                              "and internet connection at home are important indicators of the extent to which "
                                                       "a country’s population has been equipped with physical connectivity. "
                                                       "Without connectivity, a given population cannot derive the benefits of digital technologies."
                                          ),

                                          # ----- access indicator section -----

                                          html.Div(
                                              className="row",
                                              children=[

                                                  # ----- 3G mobile network coverage -----
                                                  html.Div(
                                                      className='indicator-chart',
                                                      children=dcc.Graph(
                                                          id='3g-mobile-network-coverage-chart',
                                                          className="full-width-chart")

                                                  ),
                                                  html.Div(
                                                      className='indicator-table', style={"wdith": "80%"},
                                                      id='3g-mobile-network-coverage-table'
                                                  ),
                                              ]
                                          ),

                                          # ----- households with internet -----

                                          html.Div(
                                              className='indicator-chart',
                                              children=dcc.Graph(
                                                  id='households-with-internet-chart',
                                                  className="full-width-chart"

                                              )
                                          ),
                                          html.Div(
                                              className='indicator-table',
                                              id='households-with-internet-table'
                                          ),


                                          # ----- households with computer -----


                                          html.Div(
                                              className='indicator-chart',
                                              children=dcc.Graph(
                                                  id='households-with-computer-chart',
                                                  className="full-width-chart")
                                          ),
                                          html.Div(
                                              className='indicator-table',
                                              id='households-with-computer-table'
                                          ),




                                      ]
                                  ),

                                  # ----- use -----
                                  html.Div(
                                      # use bootstrap container class to center and provide horizontal padding
                                      className="container story-container",
                                      children=[

                                          html.H2(
                                              className="story-title",
                                              children="Use"
                                          ),
                                          html.P(
                                              className="story-description",
                                              children=[
                                                  "In order to see whether physical connectivity is translating into actual use, "
                                                  "it is necessary to identify what types of people are using the infrastructure "
                                                  "and where they are located. Additionally, information on the type of internet "
                                                  "connection (mobile or fixed) people have provides insights into the quality of "
                                                  "the use-experience, which can affect usage patterns and associated outcomes. "
                                              ]),

                                          # ----- indicator section -----
                                          html.Div(
                                              className="row",
                                              children=[



                                                  html.Div(
                                                      className='indicator-chart',
                                                      children=dcc.Graph(
                                                          id='internet-population-chart',
                                                          className="full-width-chart")
                                                  ),
                                                  html.Div(
                                                      className='indicator-table',
                                                      id='internet-population-table'
                                                  ),


                                                  # ----- internet user gender gap -----

                                                  html.Div(
                                                      className='indicator-chart',
                                                      children=dcc.Graph(
                                                          id='internet-user-gender-gap-chart',
                                                          className="full-width-chart")
                                                  ),
                                                  html.Div(
                                                      className='indicator-table',
                                                      id='internet-user-gender-gap-table'
                                                  ),

                                              ]
                                          ),

                                          html.Div(
                                              className="row",
                                              children=[

                                                  # ----- mobile broadband subscription -----

                                                  html.Div(
                                                      className='indicator-chart',
                                                      children=dcc.Graph(
                                                          id='mobile-broadband-subscription-chart',
                                                          className="full-width-chart")
                                                  ),
                                                  html.Div(
                                                      className='indicator-table',
                                                      id='mobile-broadband-subscription-table'
                                                  ),


                                                  # ----- fixed broadband subscription -----

                                                  html.Div(
                                                      className='indicator-chart',
                                                      children=dcc.Graph(
                                                          id='fixed-broadband-subscription-chart',
                                                          className="full-width-chart")
                                                  ),
                                                  html.Div(
                                                      className='indicator-table',
                                                      id='fixed-broadband-subscription-table'
                                                  ),

                                              ]
                                          )
                                      ]
                                  ),

                                  # ----- affordability -----
                                  html.Div(

                                      # use bootstrap container class to center and provide horizontal padding
                                      className="container story-container",
                                      children=[
                                          html.H2(
                                              className="story-title",
                                              children="Affordability"
                                          ),
                                          html.P(
                                              className="story-description",
                                              children="The ability of people to make use of this infrastructure is determined by different social factors in the country — factors that afford some people the resources to use it while hindering meaningful access for others."
                                          ),

                                          # ----- affordability indicator section -----
                                          html.Div(
                                              className="row",
                                              children=[
                                                  html.Div(
                                                      className="col-xs-2"
                                                  ),
                                                  # ----- mobile broadband cost -----
                                                  html.Div(
                                                      className="col-xs-8",
                                                      children=[
                                                          html.Div(
                                                              className='indicator-chart',
                                                              children=dcc.Graph(
                                                                  id='mobile-broadband-cost-chart',
                                                                  className="full-width-chart")
                                                          ),
                                                          html.Div(
                                                              className='indicator-table',
                                                              id='mobile-broadband-cost-table'
                                                          ),
                                                      ]
                                                  )
                                              ]
                                          )
                                      ]),

                                  html.Div(className="footer")
                              ])

                 ])
    ])


# ----- country profile callbacks -----

@app.callback(
    dash.dependencies.Output('country-icon', 'src'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country_icon(selected_country):
    Map1 = Map[Map['Country'] == selected_country].iloc[0, 4]

    return (Map1)


@app.callback(
    dash.dependencies.Output('country-population-value', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country_population(selected_country):
    pop = df.loc[(df.Country == selected_country) & (df.Name == 'population')]
    pop.sort_values('Year', inplace=True)
    return ("{0:,.0f}".format(pop['value'].iloc[-1]))


@app.callback(
    dash.dependencies.Output('country-income-group', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country_income_group(selected_country):
    income_grp = df.loc[(df.Country == selected_country)]
    income_grp.sort_values('Year', inplace=True)

    return (income_grp['Income.group'].iloc[-1])


@app.callback(
    dash.dependencies.Output('country-sub-region', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country_sub_region(selected_country):
    region = df.loc[(df.Country == selected_country)]
    region.sort_values('Year', inplace=True)

    return (region['Region'].iloc[-1])


@app.callback(
    dash.dependencies.Output('sub-region-list', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country_profile_section(selected_country):
    region_df = df.loc[(df.Country == selected_country)]
    selected_region = region_df['Region'].iloc[-1]

    list_countries = df.loc[(df.Region == selected_region),
                            'Country'].unique().tolist()
    list_countries = [' {}'.format(x) for x in list_countries]
    list_countries = [' {}'.format(x) for x in list_countries]
    m = [x.replace(",", "") for x in list_countries]

    return utils.generate_country_profile(m)

# ----- quick look section callbacks -----


@app.callback(
    dash.dependencies.Output('connectivity-quick-look-section-1', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_1(selected_country):
    ind_internet = df.loc[(df.Country == selected_country)
                          & (df.Name == 'ind.internet')]
    ind_internet.sort_values('Year', inplace=True)
    ind_internet_latest_val = str(int(round(
        ind_internet['value'].iloc[-1], 0))) + '%' if len(ind_internet) != 0 else 'NA'
    fdf = df.loc[(df.Country == selected_country) & (
        df['Name'].isin(['ind.internet.female', 'ind.internet.male']))]
    fdf.sort_values('Year', inplace=True)

    # safely pull data, planning for lots of missing
    x1 = [str(int(round(fdf.loc[fdf['Name'] == 'ind.internet.male', 'value'].iloc[-1]))) + '%' if (fdf.shape[
        0] > 0) & (
        'ind.internet.male' in
        fdf[
            'Name'].unique()) else 'NA',
        str(int(round(fdf.loc[fdf['Name'] == 'ind.internet.female', 'value'].iloc[-1]))) + '%' if (fdf.shape[
            0] > 0) & (
        'ind.internet.female' in
        fdf[
            'Name'].unique()) else 'NA']

    return html.Table(
        # Header
        [html.Tbody([html.Tr([html.Th('Internet Users:', style={'textAlign': 'left'}),
                              html.Th(ind_internet_latest_val,
                                      style={'marginLeft': 'auto', 'textAlign': 'right'})],
                             style={'borderTop': '1px solid light-grey',
                                    'fontSize': '16px',
                                    'color': 'white',
                                    'width': '100%'})] +
                    [html.Tr([html.Th('Women:', style={'textAlign': 'left'}),
                              html.Th(x1[1],
                                      style={'marginLeft': 'auto', 'textAlign': 'right'})],
                             style={'borderTop': '1px solid light-grey',
                                    'fontSize': '15px',
                                    'color': 'white',
                                    'width': '100%'})] +
                    [html.Tr([html.Th('Men:', style={'textAlign': 'left'}),
                              html.Th(x1[0],
                                      style={'marginLeft': 'auto', 'textAlign': 'right'})],
                             style={'borderTop': '1px solid light-grey',
                                    'fontSize': '15px',
                                    'color': 'white',
                                    'width': '100%'})],
                    style={'width': '100%'})]

    )


# Body
# [html.Tr([html.Td('Women: ' + x1[1],
# style={'textAlign': 'left', 'fontSize': '16px'}),
# html.Td('Men: ' + x1[0],
# style={'textAlign': 'right', 'fontSize': '16px'})],
# style={'borderTop': '1px solid light-grey',
# 'border-bottom': '1px solid light-grey',
# 'color': 'white'})],
##        style={'width': '100%'}
# )


@app.callback(
    dash.dependencies.Output('connectivity-quick-look-section-2', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_2(selected_country):
    ind_internet = df.loc[(df.Country == selected_country)
                          & (df.Name == 'at.least.3G.coverage')]
    ind_internet.sort_values('Year', inplace=True)
    ind_internet = str(int(round(ind_internet['value'].tail(1).tolist()[
                       0]))) + '%' if (ind_internet.shape[0] > 0) else 'NA'
    # ind_internet = str(int(ind_internet['value'].tail(1).tolist()[0])) + '%'
    return html.Table(
        [html.Tbody([html.Tr([html.Th('3G Network Coverage:', style={'textAlign': 'left'}),
                              html.Th(ind_internet,
                                      style={'marginLeft': 'auto', 'textAlign': 'right'})],
                             style={'borderTop': '1px solid light-grey',
                                    'fontSize': '16px',
                                    'color': 'white'})])],
        style={'width': '100%'}
    )


@app.callback(
    dash.dependencies.Output('connectivity-quick-look-section-3', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_3(selected_country):
    ind_internet = df.loc[(df.Country == selected_country)
                          & (df.Name == 'hh.internet')]
    ind_internet.sort_values('Year', inplace=True)

    ind_internet = str(int(round(ind_internet['value'].tail(1).tolist()[0]))) + '%' if (
        ind_internet.shape[0] > 0) else 'NA'

    return html.Table(
        [html.Tbody([html.Tr([html.Th('Homes with Internet:', style={'textAlign': 'left'}),
                              html.Th(ind_internet,
                                      style={'marginLeft': 'auto', 'textAlign': 'right'})],
                             style={'borderTop': '1px solid light-grey',
                                    'fontSize': '16px',
                                    'color': 'white'})])],

        style={'width': '100%'}
    )


@app.callback(
    dash.dependencies.Output('connectivity-quick-look-section-4', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_update_quick_look_section_4(selected_country):
    cost = df.loc[(df.Country == selected_country) &
                  (df.Name == 'mobile.broadband.cost')]
    cost.sort_values('Year', inplace=True)
    cost = str(int(round(cost['value'].iloc[-1], 0))
               ) + '%' if len(cost) != 0 else 'NA'

    return html.Table(
        [html.Tbody([html.Tr([html.Th('Mobile Cost as portion of Income:', style={'textAlign': 'left'}),
                              html.Th(cost,
                                      style={'marginLeft': 'auto', 'textAlign': 'right'})],
                             style={'borderTop': '1px solid light-grey',
                                    'fontSize': '16px',
                                    'color': 'white'})])],


        style={'width': '100%'}
    )


# ----- indicator section callbacks -----

# ----- internet population -----

@app.callback(
    dash.dependencies.Output('internet-population-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_internet_population_chart(selected_country):
    return utils.generate_time_series_line_chart(selected_country=selected_country,
                                                 indicator="ind.internet",
                                                 title="What percentage of population is using Internet?",
                                                 ylabel="Internet Access (%)")


@app.callback(
    dash.dependencies.Output('internet-population-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_internet_population_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="ind.internet",
                                                  indicator_name="Internet Population")


# ----- households with internet -----

@app.callback(
    dash.dependencies.Output('households-with-internet-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_households_with_internet_chart(selected_country):
    return utils.generate_time_series_line_chart(selected_country=selected_country,
                                                 indicator="hh.internet",
                                                 title="How many homes have Internet access?",
                                                 ylabel="Homes with Internet (%)")


@app.callback(
    dash.dependencies.Output('households-with-internet-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_households_with_internet_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="hh.internet",
                                                  indicator_name="Homes with Internet")


# ----- households with computer -----

@app.callback(
    dash.dependencies.Output('households-with-computer-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_households_with_computer_chart(selected_country):
    return utils.generate_time_series_line_chart(selected_country=selected_country,
                                                 indicator="hh.computer",
                                                 title="How many homes have a computer?",
                                                 ylabel="Homes with Computer (%)")


@app.callback(
    dash.dependencies.Output('households-with-computer-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_households_with_computer_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="hh.computer",
                                                  indicator_name="Homes with computer")


# ----- 3G mobile coverage -----

@app.callback(
    dash.dependencies.Output('3g-mobile-network-coverage-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_3g_mobile_coverage_chart(selected_country):
    return utils.generate_3g_mobile_coverage_bar_and_line_chart(selected_country=selected_country,
                                                                indicator="at.least.3G.coverage",
                                                                title="What percentage of the population <br> is covered by at least a 3G Network?",
                                                                ylabel="3G Mobile Network Coverage (%)")


@app.callback(
    dash.dependencies.Output('3g-mobile-network-coverage-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_3g_mobile_network_coverage_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="at.least.3G.coverage",
                                                  indicator_name="3G Mobile Network Coverage")


# ----- mobile broadband cost -----

@app.callback(
    dash.dependencies.Output('mobile-broadband-cost-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_pie(selected_country):
    return utils.generate_mobile_broadband_cost_pie_chart(selected_country=selected_country)


@app.callback(
    dash.dependencies.Output('mobile-broadband-cost-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_mobile_broadband_cost_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="mobile.broadband.cost",
                                                  indicator_name="Mobile Broadband cost as percent of GNI per capita")


# ----- mobile broadband subscription -----

@app.callback(
    dash.dependencies.Output('mobile-broadband-subscription-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_mobile_broadband_subscription_chart(selected_country):
    return utils.generate_time_series_line_chart(selected_country=selected_country,
                                                 indicator="mobile.broadband.per.100",
                                                 title="Mobile broadband subscriptions",
                                                 ylabel="Per 100 inhabitants")


@app.callback(
    dash.dependencies.Output(
        'mobile-broadband-subscription-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_mobile_broadband_subscription_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="mobile.broadband.per.100",
                                                  indicator_name="Mobile broadband subscription",
                                                  format_as_rate=True)


# ----- fixed broadband subscription -----

@app.callback(
    dash.dependencies.Output('fixed-broadband-subscription-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_fixed_broadband_subscription_chart(selected_country):
    return utils.generate_time_series_line_chart(selected_country=selected_country,
                                                 indicator="fixed.broadband.100",
                                                 title="Fixed broadband subscriptions",
                                                 ylabel="Per 100 inhabitants")


@app.callback(
    dash.dependencies.Output('fixed-broadband-subscription-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_fixed_broadband_subscription_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="fixed.broadband.100",
                                                  indicator_name="Fixed broadband subscription",
                                                  format_as_rate=True)

# ----- internet user gender gap -----


@app.callback(
    dash.dependencies.Output('internet-user-gender-gap-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_internet_user_gender_gap_chart(selected_country):
    return utils.generate_internet_user_gender_gap_chart(selected_country=selected_country)


@app.callback(
    dash.dependencies.Output('internet-user-gender-gap-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_internet_user_gender_gap_table(selected_country):
    return utils.generate_gender_gap_table(selected_country)
