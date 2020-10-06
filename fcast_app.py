import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_fcast as fcast
import dash_fcast.distributions as dist
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Scheme
from hemlock import Dashboard

import json

DASHBOARD_SRC = '/fcast/'

def create_fcast_app(server=None):
    if server is None:
        app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
    else:
        app = dash.Dash(
            server=server,
            routes_pathname_prefix=DASHBOARD_SRC,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Enter your forecast here'),
                    dbc.CardBody(id='elicitation')
                ], className='h-100')
            ]),
            dbc.Col([
                html.Div([
                    html.P('Loading graph. This may take several seconds.') 
                ], id='graphs')
            ])
        ])
    ], className='container')

    Table.register_callbacks(app)

    @app.callback(
        Output('elicitation', 'children'),
        [Input('url', 'search')]
    )
    def update_elicitation(search):
        try:
            dashboard = Dashboard.get(search)
            bins = dashboard.g['bins']
            prob = dashboard.g['prob']
        except:
            print('Cannot find dashboard')
            bins = [0, .25, .5, .75, 1]
            prob = [1./(len(bins)-1)] * (len(bins)-1)
        return Table(
            'Forecast', bins, prob, 
            editable_cols=['pdf', 'cdf'], scalable=True, smoother=True
        )

    @app.callback(
        Output('graphs', 'children'),
        [Input('url', 'search'), Input(Table.get_id('Forecast'), 'children')]
    )
    def update_graphs(search, dist_state):
        distribution = Table.load(dist_state)
        try:
            Dashboard.record_response(search, distribution.dump())
        except:
            print('Unable to record forecast')
        pdf = go.Figure([
            distribution.pdf_plot(), distribution.bar_plot(opacity=.4)
        ])
        pdf.update_layout(
            transition_duration=500,
            title='Probability',
            showlegend=False
        )
        return [dcc.Graph(figure=pdf)]

    return app


class Table(dist.Table):
    def get_columns(self, *args, **kwargs):
        cols = super().get_columns(*args, **kwargs)
        for col in cols:
            if col['id'] in ('bin-start', 'bin-end'):
                col['format'] = Format(scheme=Scheme.fixed, precision=2)
        return cols

if __name__ == '__main__':
    app = create_fcast_app()
    app.run_server(debug=True)