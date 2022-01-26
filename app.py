import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output

data = pd.read_csv('data/serve_statistics.csv')

external_stylesheets = [

    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },

]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "Tennis Serve Analytics: A breakdown of serve statistics at the 2021 Australian Open"

app.layout = html.Div(
    children=[
            html.Div(
                children=[
                    html.P(children="🎾", className="header-emoji"),
                    html.H1(children="Tennis Serve Analytics", className="header-title"),
                    html.P(children="Analyse the serving performances"
                    " of all male players at the 2021 Australian Open",
                    className="header-description",
                    ),
                ],
                className='header',
            ),
            html.Div(children=[
                html.Div(
                    children=[
                        html.Div(children="Category", className="menu-title"),
                        dcc.Dropdown(
                            id="cat-filter",
                            options=[
                                {"label": category, "value": category}
                                for category in data.columns
                            ],
                            value="ace",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Sort", className="menu-title"),
                        dcc.RadioItems(
                            id="sort-selector",
                            options=[
                                {'label': 'Ascending', 'value': 'True'},
                                {'label': 'Descending', 'value': 'False'}
                            ],
                            value='Ascending',
                            labelStyle={'display': 'flex'}
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="# Players", className="menu-title"),
                        dcc.RangeSlider(
                            id='disp-number-slider',
                            min=5,
                            max=100,
                            step=5,
                            value=[20]
                        ),
                        html.Div(id="output-disp-number-slider")
                    ]
                )
            ],
            className="menu"
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="cat-chart",
                    ),
                    className="card"
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.H1("Individual Statistics"),
                html.P("Since the Australian Open is a knockout based tournament, the most relevant statistics are those which are normalised."),
            ],
            className='desc'
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Name", className="menu-title"),
                        dcc.Dropdown(
                            id="name-filter",
                            options=[
                                {"label": name, "value": name}
                                for name in np.sort(data.name.unique())
                            ],
                            value="Adrian Mannarino",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu body-menu"
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="perc-chart",
                    ),
                    className='card center'
                ),
            ]
        )
    ]
)

@app.callback(
    Output("output-disp-number-slider", "children"),
    [Input("disp-number-slider", "value")]
)
def update_output(value):
    return f"You have selected to display {value[0]} players"

@app.callback(
    [
        Output("cat-chart", "figure"),
        Output("perc-chart", "figure"),
    ],
    [
        Input("name-filter", "value"),
        Input("sort-selector", "value"),
        Input("disp-number-slider", "value"),
        Input("cat-filter", "value")
    ]
)
def update_charts(name, sort, slider, cat):

    sort = True if sort=='True' else False

    cat_chart = px.bar(data.sort_values(by=cat, ascending=sort)[:slider[0]], x='name', y=cat)

    perc_data = data[data['name'] == name].T.reset_index()
    perc_data.columns = ['cats', name]

    perc_chart = px.bar(perc_data[1:-1], x='cats', y=name)
    
    return cat_chart, perc_chart


if __name__ == "__main__":
    app.run_server(debug=True)