import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_fcast as fcast
import dash_fcast.distributions as dist
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Scheme
from flask_login import current_user
from hemlock import Dashboard, Embedded

import json
from functools import partial

def create_fcast_app(server=None, src=None, instructions=False):
    if server is None:
        app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
    else:
        app = dash.Dash(
            server=server,
            routes_pathname_prefix=src,
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
            bins = [0, 1/3., 2/3., 1]
            prob = [1/3., 1/3., 1/3.]
        table = Table(
            'Forecast', bins, prob, 
            editable_cols=['pdf', 'cdf'], scalable=True, smoother=True
        )
        return table.fit()

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

    if instructions:
        add_instructions(app)

    return app

correct_bins = [60, 67, 74, 81]
correct_prob = [.2, .6, .2]

rescale_step = (
    '''
    Imagine the high temperature in Philadelphia tomorrow will definitely 
    be between {lb} and {ub} degrees. To indicate this, enter {lb} as the 
    lower bound and {ub} as the upper bound, then click 'Rescale'.
    '''.format(lb=correct_bins[0], ub=correct_bins[-1]),
    lambda distribution: (
        distribution.bins[0] == correct_bins[0] 
        and distribution.bins[-1] == correct_bins[-1]
    )
)

def verify_fcast(distribution, i):
    return distribution.prob[i] == correct_prob[i]

prob_steps = [
    (
        '''
        Imagine there is a {} in 100 chance that the high temperature in 
        Philadelphia tomorrow will be between {} and {} degrees. Enter this 
        prediction in the Probability column.
        '''.format(
            round(100*correct_prob[i]), correct_bins[i], correct_bins[i+1]
        ),
        partial(verify_fcast, i=i)
    )
    for i in range(len(correct_prob))
]
steps = [rescale_step] + prob_steps

success_txt = '''
Congratulations! You completed the comprehension check. Click >> to continue.
'''

def add_instructions(app):
    app.layout.children = [
        html.Div(
            json.dumps([0, 0, True]), 
            id='step_idx', style={'display': 'none'}
        ),
        html.Div(id='instructions')
    ] + app.layout.children

    @app.callback(
        [Output('step_idx', 'children'), Output('instructions', 'children')],
        [Input(Table.get_id('Forecast'), 'children')],
        [State('step_idx', 'children')]
    )
    def alert_success(dist_state, step_idx):
        step_idx, attempt, first_callback = json.loads(step_idx)
        distribution = Table.load(dist_state)
        instructions_txt, test = steps[step_idx]
        if first_callback:
            alert = html.Div()
            step_idx, attempt, first_callback = 0, 0, False
        elif test(distribution):
            alert = dbc.Alert(
                'Step {} complete'.format(step_idx+1), 
                color='success', style={'text-align': 'center'}
            )
            step_idx, attempt = step_idx+1, 0
            instructions_txt = (
                success_txt if step_idx == len(steps)
                else steps[step_idx][0]
            )
        else:
            alert = dbc.Alert(
                'Please reread the instructions and try again.', 
                color='danger', style={'text-align': 'center'}
            )
            step_idx, attempt = step_idx, attempt+1
        return (
            json.dumps([step_idx, attempt, first_callback]), 
            [
                alert, 
                html.P([
                    html.B('Step {}.'.format(step_idx+1)),
                    instructions_txt
                ])
            ]
        )


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