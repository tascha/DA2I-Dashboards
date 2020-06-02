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
                 children="TESTING")
    ])