# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import dash

from app import app
from app import df
import utils
from apps import navbar

layout = html.Div(
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
                                             dashboard="gender", sections=4)
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
                                          ),
                                          html.P(
                                              children=[
                                                  html.Br(),
                                                  html.Span(
                                                      children="Dashboard development and support by  "
                                                  ),
                                                  html.A(
                                                      rel="license", 
                                                      href="https://danielrekshan.com",
                                                      children="Daniel Rekshan"
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
                                                           html.A(children='Github repo', target='_blank', href="https://github.com/tascha/DA2I-Dashboards"),
                                                           html.Span(' for acknowledgements and technical resources and the '),
                                                           html.A(children='dashboard FAQs', target='_blank', href="https://tascha.uw.edu/2020/07/tascha-launches-development-and-access-to-information-dashboards/"),
                                                           html.Span('.'),
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
                                              children="Gender Dashboard",
                                              style={'paddingTop': '30px'}
                                          ),

                                          html.P(
                                              className="dashboard-description",
                                              children="The Gender Dashboard explores the social context of meaningful access to information tracking the progress of countries in providing equitable access and fair opportunities in technology use, skills, education, employment, and political participation for women and men."
                                          ),
                                          # ----- story one -----
                                          html.Div(

                                              # use bootstrap container class to center and provide horizontal padding
                                              className="container story-container",
                                              children=[
                                                  html.H2(
                                                      className="story-title",
                                                      children="Gender Inequality"
                                                  ),
                                                  html.P(
                                                      className="story-description",
                                                      children="The index measures gender inequalities in key aspects of human development: reproductive health, labor participation, and political representation. It measures the human development costs of gender inequality. Thus, the higher the GII value the more disparities between women and men and the more loss to human development."
                                                  ),

                                                  # ----- story one indicator section -----

                                                  html.Div(
                                                      className="row",
                                                      children=[
                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[
                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      id="aggregate-gender-index-most-recent-rating"
                                                                  ),


                                                                  # ----- aggregate freedom chart -----
                                                                  html.Div(
                                                                      className='',
                                                                      children=dcc.Graph(
                                                                          id='aggregate-gender-index-sparklines-bar-slider-chart')
                                                                  ),

                                                              ]
                                                          ),


                                                          html.Div(
                                                              className='indicator-chart',
                                                              children=dcc.Graph(
                                                                  id='aggregate-gender-index-sparklines-bar-chart')
                                                          ),


                                                          html.Div(
                                                              className='indicator-table',
                                                              id='inequality-over-years-table'
                                                          ),
                                                      ]),

                                              ]
                                          ),
                                          # ----- story one part 2 -----
                                          html.Div(

                                              # use bootstrap container class to center and provide horizontal padding
                                              className="container story-container",
                                              children=[
                                                  html.H2(
                                                      className="gender-title-section",
                                                      children="Technology use and skills"
                                                  ),
                                                  html.P(
                                                      className="story-description",
                                                      children="Women and girls still remain behind in technology access, use, and the skills necessary to meaningfully use technology tools to improve their lives and those of their communities."
                                                  ),

                                                  # ----- story one part 2 indicator section -----
                                                  html.Div(
                                                      className="row",
                                                      children=[

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[

                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      children=dcc.Graph(
                                                                          id='technology-use-chart')
                                                                  ),
                                                                  html.Div(
                                                                      className='indicator-table moveup',
                                                                      children=''  # utils.generate_dummy_table()
                                                                  )
                                                              ]
                                                          ),
                                                          

                                                          html.Div(
                                                              id="technology-use-table",
                                                              className="indicator-table",
                                                              children=[""]
                                                          ),

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[

                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      children=dcc.Graph(id='ict-skills-chart'
                                                                                         )
                                                                  )
                                                              ]
                                                          ),

                                                          html.Div(
                                                              className="indicator-table moveup",
                                                              id="ict-skills-table",
                                                              children=[""]
                                                          )
                                                      ]
                                                  ),
                                              ]
                                          ),

                                          # ----- story two -----
                                        #   html.Div(

                                        #       # use bootstrap container class to center and provide horizontal padding
                                        #       className="container story-container",
                                        #       children=[
                                        #           html.H2(
                                        #               className="gender-title-section",
                                        #               children="Educational opportunities"
                                        #           ),
                                        #           html.P(
                                        #               className="story-description",
                                        #               children="Providing equitable education for girls and women is a key ingredient that empowers their agency "
                                        #               "and enables them to access better employment opportunities, nourishes their self-esteem, and strengthens "
                                        #               "their role within their families and communities."
                                        #           ),

                                        #           # ----- story two indicator section -----


                                        #         #   html.Div(
                                        #         #       className="row",
                                        #         #       children=[

                                        #         #           html.Div(
                                        #         #               className="indicator-chart",
                                        #         #               children=dcc.Graph(id='educational-attainment-by-gender-bar-chart'
                                        #         #                                  )
                                        #         #           ),
                                        #         #           html.Div(
                                        #         #               className='indicator-table',
                                        #         #               children=''  # utils.generate_dummy_table()
                                        #         #           )
                                        #         #       ]
                                        #         #   ),

                                        #       ]
                                        #   ),
                                          # ]
                                          # ),
                                          # ----- story three -----
                                          html.Div(

                                              # use bootstrap container class to center and provide horizontal padding
                                              className="container story-container",
                                              children=[
                                                  html.H2(
                                                      className="story-title",
                                                      children="Economic opportunities"
                                                  ),
                                                  html.P(
                                                      className="story-description",
                                                      children="Creating an enabling environment where women and men have an equal standing in the labor "
                                                      "market directly impacts the potential for economic growth, combats different forms of inequality, "
                                                      "and allows for a more equitable social development in the countries. "
                                                  ),

                                                  # ----- story three indicator section -----
                                                  html.Div(
                                                      className="row",
                                                      children=[

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[

                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      children=dcc.Graph(
                                                                          id='neet-chart')
                                                                  ),
                                                                  html.Div(
                                                                      id='neet-table',
                                                                      className='indicator-table',
                                                                      children=''  # utils.generate_dummy_table()
                                                                  )
                                                              ]
                                                          ),

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[

                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      children=dcc.Graph(
                                                                          id='unemployment-chart')
                                                                  ),
                                                                  html.Div(
                                                                      className='indicator-table',
                                                                      id='unemployment-table',
                                                                      children=''  # utils.generate_dummy_table()
                                                                  )
                                                              ]
                                                          )
                                                      ]
                                                  ),
                                              ]
                                          ),

                                          # ----- story four -----
                                          html.Div(

                                              # use bootstrap container class to center and provide horizontal padding
                                              className="container story-container",
                                              children=[
                                                  html.H2(
                                                      className="story-title",
                                                      children="Women in Leadership"
                                                  ),
                                                  html.P(
                                                      className="story-description",
                                                      children="The diversity of voices that shape the different social, political, and scientific spheres is a foundation for a more inclusive and participatory society. Assessing women’s leadership roles in politics and science is a step towards assessing this diversity."
                                                  ),

                                                  # ----- story for indicator section -----
                                                  html.Div(
                                                      className="row",
                                                      children=[

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[

                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      children=dcc.Graph(
                                                                          id='women-in-parliament-line-chart'
                                                                      )
                                                                  ),
                                                                  html.Div(
                                                                      id='women-in-parliament-table',
                                                                      className='indicator-table',
                                                                      children=''  
                                                                  )
                                                              ]
                                                          ),

                                                          html.Div(
                                                              className="col-xs-6",
                                                              children=[

                                                                  html.Div(
                                                                      className="indicator-chart",
                                                                      children=dcc.Graph(id='women-in-stem-line-chart'
                                                                                         )
                                                                  ),
                                                                  html.Div(
                                                                      id="women-in-stem-table",
                                                                      className='indicator-table',
                                                                      children='' 
                                                                  )
                                                              ]
                                                          )
                                                      ]
                                                  ),
                                              ]
                                          ),

                                          html.Div(className="footer")
                                      ])

                              ]),
                 ])


    ])


# ----- quick look section callbacks -----

@app.callback(
    dash.dependencies.Output('gender-quick-look-section-1', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_1(selected_country):
    # filtered data
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == "GII"]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    value = df_filtered['value'].tail(
        1).tolist()[0] if len(df_filtered) != 0 else 'NA'
    # years = int(df_filtered['Year'].tail(1).tolist()[0]) if len(df_filtered) != 0 else 'NA'

    return html.Table(
        # Header

        [html.Tr([html.Th('Gender Inequality Index:', style={'textAlign': 'left'}),
                  html.Th(round(value, 3),
                          style={'marginLeft': 'auto', 'textAlign': 'right'})],
                 style={'borderTop': '1px solid light-grey',
                        'fontSize': '16px',
                        'color': 'white'})],
        style={'width': '100%'}
    )


@app.callback(
    dash.dependencies.Output('gender-quick-look-section-2', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_2(selected_country):
    # filtered data
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == "NEET.Female"]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    women = str(df_filtered['value'].tail(
        1).tolist()[0]) + "%" if len(df_filtered) != 0 else 'NA'

    # filtered data
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == "NEET.Male"]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    men = str(df_filtered['value'].tail(
        1).tolist()[0]) + '%' if len(df_filtered) != 0 else 'NA'


    return html.Table(
        # Header
        html.Tbody(
            [html.Tr([html.Th('Youth NEET', colSpan='2', style={'textAlign': 'left'})],
                     style={'borderTop': '1px solid light-grey',
                            'fontSize': '16px',
                            'colspan': '2',
                            'color': 'white',
                            'width': '100%'})] +

            [html.Tr([html.Th('Women:', style={'textAlign': 'left'}),
                      html.Th(women,
                              style={'marginLeft': 'auto', 'textAlign': 'right'})],
                     style={'borderTop': '1px solid light-grey',
                            'fontSize': '15px',
                            'color': 'white',
                            'width': '100%'})] +
            [html.Tr([html.Th('Men:', style={'textAlign': 'left'}),
                      html.Th(men,
                              style={'marginLeft': 'auto', 'textAlign': 'right'})],
                     style={'borderTop': '1px solid light-grey',
                            'fontSize': '15px',
                            'color': 'white',
                            'width': '100%'})],
        ),

        style={'width': '100%'})


@app.callback(
    dash.dependencies.Output('gender-quick-look-section-3', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_update_quick_look_section_3(selected_country):
    # filtered data
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == "Unemp.Female"]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    women = str(df_filtered['value'].tail(
        1).tolist()[0]) + '%' if len(df_filtered) != 0 else 'NA'

    # filtered data
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == "Unemp.Male"]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    men = str(df_filtered['value'].tail(
        1).tolist()[0]) + "%" if len(df_filtered) != 0 else 'NA'


    return html.Table(
        # Header
        [html.Tr([html.Th('Unemployment', colSpan='2', style={'textAlign': 'left'})],
                 style={'borderTop': '1px solid light-grey',
                        'fontSize': '16px',
                        'color': 'white',
                        'colspan': '2',
                        'width': '100%'})] +

        [html.Tr([html.Th('Women:', style={'textAlign': 'left'}),
                  html.Th(women,
                          style={'marginLeft': 'auto', 'textAlign': 'right'})],
                 style={'borderTop': '1px solid light-grey',
                        'fontSize': '15px',
                        'color': 'white',
                        'width': '100%'})] +
        [html.Tr([html.Th('Men:', style={'textAlign': 'left'}),
                  html.Th(men,
                          style={'marginLeft': 'auto', 'textAlign': 'right'})],
                 style={'borderTop': '1px solid light-grey',
                        'fontSize': '15px',
                        'color': 'white',
                        'width': '100%'})],
        style={'width': '100%'})


@app.callback(
    dash.dependencies.Output('gender-quick-look-section-4', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_quick_look_section_4(selected_country):
    # filtered data
    df_filtered = df[df["Country"] == selected_country]
    # filtered by selected country and indicator
    df_filtered = df_filtered[df_filtered["Name"] == "women.in.stem"]
    # drop rows with missing indicator values
    df_filtered = df_filtered.dropna(axis="index", subset=["value"])

    df_filtered.sort_values('Year', inplace=True)
    women_in_stem = str(round(df_filtered['value'].tail(1), 1).tolist()[
        0]) + '%' if len(df_filtered) != 0 else 'NA'

    return html.Table(
        # Header

        html.Tbody([html.Tr([html.Th('Women in STEM:', style={'textAlign': 'left'}),
                             html.Th(women_in_stem,
                                     style={'marginLeft': 'auto', 'textAlign': 'right'})],
                            style={'borderTop': '1px solid light-grey',
                                   'fontSize': '16px',
                                   'color': 'white'})]),

        style={'width': '100%'}
    )


# ----- gender callbacks -----

# ----- aggregate gender index most recent rating -----
@app.callback(
    dash.dependencies.Output(
        "aggregate-gender-index-most-recent-rating", "children"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def calculate_gender_rating(selected_country):
    indicator = "GII"
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
        if score > 0.6:
            rating = ""
            color = '#FF8A5B'
        elif score > 0.3:
            rating = ""
            color = '#FF8A5B'
        else:
            rating = ""
            color = '#FF8A5B'
    else:
        rating = "NO DATA"
        color = "#000000"

    return html.Table(
        # Header

        html.Tbody([html.Tr([html.Th('Gender Inequality Index' + ' (' + year + '):', style={'fontSize': '18px', 'textAlign': 'left', 'color': '#38C0E1'}),
                             html.Td(round(score, 3),
                                     style={'fontSize': '22px', 'textAlign': 'left', 'color': '#FF8A5B'})],
                            style={'fontFamily': 'Raleway'})]),
        style={'width': '90%'}
    )

# ----- aggregate freedom sparklines slider chart -----


@app.callback(
    dash.dependencies.Output(
        "aggregate-gender-index-sparklines-bar-slider-chart", "figure"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def update_aggrete_gender_sparklines_slider_bar_chart(selected_country):
    indicator_name = "GII"
    return utils.generate_sparklines_slider_bar_chart(selected_country=selected_country,
                                                      indicator=indicator_name,
                                                      title="")
# ----- aggregate freedom sparklines bar chart -----


@app.callback(
    dash.dependencies.Output(
        "aggregate-gender-index-sparklines-bar-chart", "figure"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def update_aggregate_gender_sparklines_bar_chart(selected_country):
    indicator_name = "GII"
    categories = [
        {
            "name": "",
            "range": [0, 0.3],
            "color": "#FF8A5B"
        },
        {
            "name": "",
            "range": [0.3, 0.6],
            "color": "#FF8A5B",
        },
        {
            "name": "",
            "range": [0.6, 1],
            "color": "#FF8A5B"
        }
    ]
    return utils.generate_sparklines_bar_chart(selected_country=selected_country,
                                               indicator=indicator_name,
                                               title="Gender Inequality Index Over the Years",
                                               categories=categories)

@app.callback(
    dash.dependencies.Output('inequality-over-years-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_inequality_over_years_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="GII",
                                                  indicator_name="Gender Inequality Index")
# ----- technology use -----
@app.callback(
    dash.dependencies.Output('technology-use-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_technology_use_chart(selected_country):
    return utils.generate_technology_use_chart(selected_country,
                                               title_text='What technologies do women and men use?')

# ----- ICT skills -----


@app.callback(
    dash.dependencies.Output('ict-skills-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_ict_skills_chart(selected_country):
    return utils.generate_ict_skills_chart(selected_country,
                                           title_text='What technology skills women and men have?')

@app.callback(
    dash.dependencies.Output('ict-skills-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_ict_skils_table(selected_country):
    return utils.generate_ict_skills_table(selected_country,
                                           title_text='What technology skills women and men have?')


@app.callback(
    dash.dependencies.Output('technology-use-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_technology_use_table(selected_country):
    return utils.generate_technology_use_table(selected_country,
                                           title_text='What technologies do men and women use?')



# ----- neet -----
@app.callback(
    dash.dependencies.Output('neet-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_neet_chart(selected_country):
    return utils.generate_neet_chart(selected_country,
                                     title_text='What percentage of young people don’t participate in <br>education, training, or employment?')


@app.callback(
    dash.dependencies.Output('neet-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_neet_table(selected_country):
    return [utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="NEET.Female",
                                                  indicator_name="Young women not in employment, education, or training"),utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="NEET.Male",
                                                  indicator_name="Young men not in employment, education, or training")]
# ----- unemployment -----


@app.callback(
    dash.dependencies.Output('unemployment-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_unemployment_chart(selected_country):
    return utils.generate_unemployment_chart(selected_country,
                                             title_text='What percentage of women and men <br>are unemployed?')

@app.callback(
    dash.dependencies.Output('unemployment-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_unemployment_table(selected_country):
    return [utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="Unemp.Female",
                                                  indicator_name="Women Unemployed"),utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="Unemp.Male",
                                                  indicator_name="Men Unemployed")]

# ----- gender inequality choropleth -----


@app.callback(
    dash.dependencies.Output(
        'gender-inequality-index-choropleth-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_gender_inequality_index_choropleth_chart(selected_country):
    return utils.generate_gender_inequality_choropleth()


# ----- gender inequality vs internet use -----
@app.callback(
    dash.dependencies.Output(
        'gender-inequality-vs-internet-use-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_gender_inequality_vs_internet_use_chart(selected_country):
    return utils.generate_gender_inequality_vs_internet_use_chart(selected_country)


# ----- women in parliament -----
@app.callback(
    dash.dependencies.Output('women-in-parliament-line-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_women_in_parliament_line_chart(selected_country):
    return utils.generate_women_in_parliament_line_chart(selected_country,
                                                         title_text='What percentage of women participate <br>in politics?')


@app.callback(
    dash.dependencies.Output('women-in-parliament-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_women_in_parliament_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="SG.GEN.PARL.ZS",
                                                  indicator_name="Women in politics")

# ----- women in stem -----


@app.callback(
    dash.dependencies.Output('women-in-stem-line-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_women_in_stem_line_chart(selected_country):
    return utils.generate_women_in_stem_line_chart(selected_country,
                                                   title_text='What percentage of women graduated from <br>STEM-related careers? ')

@app.callback(
    dash.dependencies.Output('women-in-stem-table', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_women_in_stem_table(selected_country):
    return utils.generate_most_recent_value_table(selected_country=selected_country,
                                                  indicator="women.in.stem",
                                                  indicator_name="Women in Stem")

# ----- educational attainment -----
# educational-attainment-basic-level-by-gender-bar-chart
# @app.callback(
#     dash.dependencies.Output(
#         'educational-attainment-basic-level-by-gender-bar-chart', 'figure'),
#     [dash.dependencies.Input('country-dropdown', 'value')])
# def update_educational_attainment_basic_level_by_gender_bar_chart(selected_country):
#     return utils.generate_educational_attainment_basic_level_by_gender_bar_chart(selected_country,
#                                                                                  title_text='What is the highest level of education completed <br>by women '
#                                                                                  'and men?')

# educationa-attainment-by-gender-bar-chart


# @app.callback(
#     dash.dependencies.Output(
#         'educational-attainment-by-gender-bar-chart', 'figure'),
#     [dash.dependencies.Input('country-dropdown', 'value')])
# def update_educational_attainment_by_gender_bar_chart(selected_country):
#     return utils.generate_educational_attainment_by_gender_bar_chart(selected_country,
#                                                                      title_text='What is the highest level of education <br>completed by women and men?')
