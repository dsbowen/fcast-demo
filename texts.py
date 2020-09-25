import numpy as np

consent_label = '''
<p>
    This is a consent page. By continuing with the survey, you consent to 
    transfer ownership of your first-born child to the Tetlock lab.
</p>
'''

# these are the correct bins and probabilities the participant should enter to
# indicate they've understood how to use the dashboard
correct_bins = [60, 67, 74, 81]
correct_prob = [.2, .6, .2]

# these are the initial bins and probabilities displayed to the participant in
# the comprehension check
lb, ub = correct_bins[0], correct_bins[-1]
init_bins = list((np.array(correct_bins)-lb)/(ub-lb))
init_prob = [1./(len(init_bins)-1)] * (len(init_bins)-1)

def gen_beliefs(bins, prob):
    """
    Create a html list of beliefs implied by the correct bins and 
    probabilities of the comprehension check.
    """
    def gen_belief(bin_start, bin_end, pdf):
        return '''
        <li>There is a {} in 100 chance the high temperature will be between {} and {} degrees.</li>
        '''.format(100*round(pdf, 2), bin_start, bin_end)

    params = zip(bins[:-1], bins[1:], prob)
    return ''.join([gen_belief(*param) for param in params])

# label displayed to participants as comprehension check instructions
comp_check_label = '''
<p>
    Imagine you're forecasting the high temperature in Philadelphia, PA 
    tomorrow. Imagine you believe that:
    <ul>
        <li>The high temperature will definitely be between {lb} and {ub} degrees.</li>
        {beliefs}
    </ul>
    Enter this forecast in the dashboard below.
</p>
'''.format(lb=lb, ub=ub, beliefs=gen_beliefs(correct_bins, correct_prob))

comp_check_success = '''
<p>You successfully completed the comprehension check!</p>
'''

# questions the participant should forecast
fcast_questions = [
    ('variable name for forecast x', '<p>Please forecast x.</p>'),
    ('variable name for forecast y', '<p>Please forecast y.</p>'),
    # TODO fill in forecast questions
]