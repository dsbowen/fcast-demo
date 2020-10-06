import texts
from fcast_app import DASHBOARD_SRC

import dash_fcast.distributions as dist
import numpy as np
from hemlock import Branch, Dashboard, Embedded, Label, Navigate as N, Page, Submit as S, route
from hemlock.tools import comprehension_check
from hemlock_berlin import berlin
from hemlock_crt import crt
from hemlock_demographics import basic_demographics

from random import choice, shuffle

# possible number of bins to display to participants
N_BINS = [3, 4, 5, 8]

@route('/survey')
def start():
    return Branch(
        Page(Label(texts.consent_label)),
        basic_demographics(page=True),
        *crt(page=True),
        berlin(),
        navigate=N.comprehension()
    )

@N.register
def comprehension(origin=None):
    return Branch(
        *comprehension_check(
            instructions=Page(
                Label('<p>Instructions here.</p>')
            ),
            checks=Page(
                gen_dashboard(
                    texts.comp_check_label,
                    bins=texts.init_bins, prob=texts.init_prob,
                    var='CompCheck', data_rows=-1, submit=S.verify_fcast()
                )
            ),
            attempts=3
        ),
        navigate=N.fcast()
    )

def gen_dashboard(label, n_bins=None, bins=None, prob=None, **kwargs):
    if n_bins is not None:
        bins = list(np.round(np.linspace(0, 1, num=n_bins+1), 2))
        prob = list(np.diff(bins))
    return Dashboard(
        label, 
        src=DASHBOARD_SRC, 
        aspect_ratio=(21, 9) if len(bins)-1 < 6 else (16, 9),
        g={'bins': bins, 'prob': prob}, 
        **kwargs
    )

@S.register
def verify_fcast(dashboard):
    distribution = dist.Table.load(dashboard.response)
    bins = list(np.round(distribution.bins, 2))
    dashboard.data = int(
        bins == texts.correct_bins and distribution.prob == texts.correct_prob
    )

@N.register
def fcast(origin=None):
    questions = texts.fcast_questions.copy()
    n_bins_list = [choice(N_BINS) for q in questions]
    fcast_pages = [
        Page(
            gen_dashboard(
                label, n_bins=n_bins, var='Forecast', record_order=True
            ), 
            timer='ForecastTimer',
            embedded=[Embedded('Variable', var), Embedded('NBins', n_bins)]
        )
        for (var, label), n_bins in zip(questions, n_bins_list)
    ]
    shuffle(fcast_pages)
    return Branch(
        Page(Label(texts.comp_check_success)),
        *fcast_pages,
        Page(
            Label('<p>The end.</p>'), 
            terminal=True
        )
    )