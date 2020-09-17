import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_fcast as fcast
import dash_fcast.distributions as dist
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from hemlock import Dashboard

def create_fcast_app(server=None):
    if server is None:
        app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
    else:
        app = dash.Dash(
            server=server,
            routes_pathname_prefix='/fcast/',
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='record-response'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Enter your forecast here'),
                    dbc.CardBody([
                        dist.Moments('Forecast')
                    ])
                ], className='h-100')
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Your forecast in bins'),
                    dbc.CardBody([
                        fcast.Table(
                            'Table',
                            datatable={
                                'editable': True, 'row_deletable': True
                            },
                            row_addable=True
                        )
                    ])
                ], className='h-100')
                    
            ])
        ]),
        html.Div(id='graphs')
    ], className='container')

    dist.Moments.register_callbacks(app)
    fcast.Table.register_callbacks(app)

    @app.callback(
        Output('record-response', 'children'),
        [Input(dist.Moments.get_id('Forecast', 'update'), 'n_clicks')],
        [
            State('url', 'search'),
            State(dist.Moments.get_id('Forecast', 'lb'), 'value'),
            State(dist.Moments.get_id('Forecast', 'ub'), 'value'),
            State(dist.Moments.get_id('Forecast', 'mean'), 'value'),
            State(dist.Moments.get_id('Forecast', 'std'), 'value')
        ]
    )
    def record_response(_, search, lb, ub, mean, std):
        try:
            Dashboard.record_response(search, [lb, ub, mean, std])
        except:
            print('WARNING Unable to record response')

    @app.callback(
        Output('graphs', 'children'),
        [
            Input(dist.Moments.get_id('Forecast'), 'children'),
            Input(fcast.Table.get_id('Table'), 'children')
        ]
    )
    def update_graphs(dist_state, table_state):
        distribution = dist.Moments.load(dist_state)
        table = fcast.Table.load(table_state)
        pdf = go.Figure([
            distribution.pdf_plot(), table.bar_plot('Forecast', opacity=.4)
        ])
        pdf.update_layout(
            transition_duration=500,
            title='Probability',
            showlegend=False
        )
        cdf = go.Figure([distribution.cdf_plot()])
        cdf.update_layout(
            transition_duration=500,
            title='Cumulative probability'
        )
        return [
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=pdf)
                ]),
                dbc.Col([
                    dcc.Graph(figure=cdf)
                ])
            ])
        ]

    return app

if __name__ == '__main__':
    app = create_fcast_app()
    app.run_server(debug=True)