import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import connectivity, freedom, gender, about

application = app.server


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    pagename = pathname.split('/')[1]
    if pagename == '/' or pagename == '':
        return connectivity.layout
    elif pagename == 'connectivity':
        return connectivity.layout
    elif pagename == 'freedom':
        return freedom.layout
    elif pagename == 'gender':
        return gender.layout
    elif pagename == 'about':
        return about.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
