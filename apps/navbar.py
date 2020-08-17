import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import urllib
import base64
from app import app
from app import countries
from app import encoded_image, encoded_image3, encoded_image4, encoded_image7
from urllib.parse import unquote

all_countries = [ct for ct in countries]


def countryParam(country):
    if len(country) > 0:
        return "/"+urllib.parse.quote_plus(country)
    else:
        return ""


def generateCountryDropdown(country):

    return [
        html.Div(id='country-dropdown-label',
                 children='Select a Country:'),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{'label': ct, 'value': ct}
                     for ct in countries],
            value=country,

        ),
    ]


def generatePathname(pathname):
    if (len(pathname) < 5):
        return "/connectivity/Afghanistan"
    else:
        return pathname


def generateNavButtons(country):
    if len(country) < 3:
        return ""
    else:
        return [

            # ----- connectivity navbar button -----
            html.Div(
                className='navbar-button',
                children=[
                    html.Img(
                        src='data:image/png;base64,{}'.format(
                            encoded_image.decode())
                    ),
                    html.A(
                        children='Connectivity',
                        href='/connectivity'+countryParam(country)
                    )
                ]
            ),

            # ----- freedom navbar button -----
            html.Div(
                className='navbar-button',
                children=[
                    html.Img(
                        src='data:image/png;base64,{}'.format(
                            encoded_image4.decode())
                    ),
                    html.A('Freedom', href='/freedom'+countryParam(country))
                ]
            ),

            # ----- gender navbar button -----
            html.Div(
                className='navbar-button',
                children=[
                    html.Img(
                        src='data:image/png;base64,{}'.format(
                            encoded_image3.decode())
                    ),
                    html.A('Gender', href='/gender'+countryParam(country))
                ]
            )
        ]


layout = html.Div(
    id="navbar",
    className='navbar custom-navbar',
    children=[
        html.A(
            id='da2i-logo',
            href="/",
            children=[
                html.Img(src='data:image/png;base64,{}'.format(encoded_image7.decode()), style={'width': '75px'})]
        ),
        html.Div(
            id="country-dropdown-div",
            className="",
            children=generateCountryDropdown(countries[0]),
        ),
        html.Div(
            id="navbar-buttons",
            className=" dashboard-buttons",
            children=generateNavButtons(''),
        ),
        html.Div(
            id="pathnameWrap",
            children=generatePathname(''),
        ),
        html.Div(
            id="countrynameWrap",
            children='',
        ),
        html.Div(
            id="cookies-eu-banner",
            style={'display': 'none'},
            children=[
                html.Span(
                    id="banner-text", children="By clicking accept, you accept the use of cookies by Google Analytics for statistical purposes."),
                html.Span(
                    children=[
                        html.Button(id="cookies-eu-reject", children="Reject"),
                        html.Button(id="cookies-eu-accept", children="Accept"),
                    ]
                )

            ]
        )

    ]
)


@app.callback(
    dash.dependencies.Output('navbar-buttons', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value'), Input('url', 'pathname')])
def update_navbar(selected_country, pathname):
    return generateNavButtons(selected_country)

@app.callback(Output('pathnameWrap', 'children'),
              [Input('url', 'pathname')])
def update_pathname_wrap(pathname):
    return pathname

@app.callback(Output('countrynameWrap', 'children'),
              [Input('country-dropdown', 'value')])
def update_countryname_wrap(value):
    return value

@app.callback(Output('country-dropdown-div', 'children'),
              [Input('url', 'pathname')])
def update_country_dropdown(pathname):
    if (len(pathname.split('/')) < 3):
        country = countries[0]
    else:
        country_name = unquote(pathname.split('/')[2].replace("+", " "))
        if (country_name and country_name in countries):
            country = country_name
    return generateCountryDropdown(country)
