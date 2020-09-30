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
    ('variable name for forecast x', '<p>Please spend up to five minutes answering the following question: What will the end-of-day value of the S&P 500 Index be on October 31?  The historical values of S&P 500 Index can be viewed here: https://www.bloomberg.com/quote/SPX:IND. </p>'),
    ('variable name for forecast x', '<p>Please spend up to five minutes answering the following question: What will the maximum daily temperature in Central Park, New York City be on October 31?  The historical daily temperatures in Central Park, NY can be viewed here: https://w2.weather.gov/climate/index.php?wfo=okx .</p>'),
    ('variable name for forecast x', '<p>Please spend up to five minutes answering the following question: How many new cases of Coronavirus Disease 2019 (COVID-19) will be confirmed in the city of New York on October 31? The historical daily case counts for New York City can be viewed here: https://www1.nyc.gov/site/doh/covid/covid-19-data.page .</p>'),
    ('variable name for forecast x', '<p>Please spend up to five minutes answering the following question: How many new deaths of Coronavirus Disease 2019 (COVID-19) will be confirmed in the state of New York on October 31? The historical daily death counts for New York state can be viewed here: https://www1.nyc.gov/site/doh/covid/covid-19-data.page .</p>'),
    ('variable name for forecast x', '<p>Please spend up to five minutes answering the following question: What will the daily price of Brent crude oil be on October 31? Historical oil price information can be viewed here: https://www.bloomberg.com/quote/CO1:COM .</p>')
]