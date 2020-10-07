import fcast_app
import texts

import dash_fcast.distributions as dist
import numpy as np
from hemlock import Branch, Dashboard, Embedded, Label, Navigate as N, Page, Submit as S, route
from hemlock.tools import comprehension_check
from hemlock_berlin import berlin
from hemlock_crt import crt
from hemlock_demographics import demographics

from random import choice, shuffle

# possible number of bins to display to participants
N_BINS = [3, 4, 5, 8]

# @route('/survey')
def start():
    return Branch(
        Page(Label(texts.consent_label)),
        demographics('age_bins', 'gender', 'race', 'education', page=True),
        *crt(page=True),
        berlin(),
        navigate=N.comprehension()
    )

@route('/survey')
@N.register
def comprehension(origin=None):
    lb, ub = fcast_app.correct_bins[0], fcast_app.correct_bins[-1]
    init_bins = list((np.array(fcast_app.correct_bins)-lb)/(ub-lb))
    init_prob = [1./(len(init_bins)-1)] * (len(init_bins)-1)
    return Branch(
        *comprehension_check(
            instructions=Page(
                Label('<p>Instructions here.</p>')
            ),
            checks=Page(
                gen_dashboard(
                    src='/fcast-instr/',
                    bins=init_bins, prob=init_prob,
                    var='CompCheck', 
                    data_rows=-1, 
                    submit=S.verify_fcast()
                ),
                back=True
            ),
        ),
        navigate=N.fcast()
    )

def gen_dashboard(
        src, label='', n_bins=None, bins=None, prob=None, **kwargs
    ):
    if n_bins is not None:
        bins = list(np.round(np.linspace(0, 1, num=n_bins+1), 2))
        prob = list(np.diff(bins))
    aspect_ratio = (21, 9) if len(bins) <= 6 and src=='/fcast/' else (16, 9)
    return Dashboard(
        label,
        src=src, 
        aspect_ratio=aspect_ratio,
        g={'bins': bins, 'prob': prob}, 
        **kwargs
    )

@S.register
def verify_fcast(dashboard):
    distribution = dist.Table.load(dashboard.response)
    bins = list(np.round(distribution.bins, 2))
    dashboard.data = int(
        bins == fcast_app.correct_bins 
        and distribution.prob == fcast_app.correct_prob
    )

@N.register
def fcast(origin=None):
    questions = texts.fcast_questions.copy()
    n_bins_list = [choice(N_BINS) for q in questions]
    fcast_pages = [
        Page(
            gen_dashboard(
                '/fcast/', 
                label=label,
                n_bins=n_bins, 
                var='Forecast', 
                record_order=True
            ), 
            timer='ForecastTimer',
            embedded=[Embedded('Variable', var), Embedded('NBins', n_bins)]
        )
        for (var, label), n_bins in zip(questions, n_bins_list)
    ]
    shuffle(fcast_pages)
    return Branch(
        *fcast_pages,
        Page(
            Label('<p>The end.</p>'), 
            terminal=True
        )
    )