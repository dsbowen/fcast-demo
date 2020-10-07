import numpy as np

consent_label = '''
<p>
    This is a consent page. By continuing with the survey, you consent to 
    transfer ownership of your first-born child to the Tetlock lab.
</p>
'''

# questions the participant should forecast
fcast_questions = [
    (
        'S&P', 
        '<p>Please spend up to five minutes answering the following question: What will the end-of-day value of the S&P 500 Index be on October 31?  The historical values of S&P 500 Index can be viewed here: https://www.bloomberg.com/quote/SPX:IND. </p>'
    ),
    (
        'Temperature', 
        '<p>Please spend up to five minutes answering the following question: What will the maximum daily temperature in Central Park, New York City be on October 31?  The historical daily temperatures in Central Park, NY can be viewed here: https://w2.weather.gov/climate/index.php?wfo=okx .</p>'
    ),
    (
        'COVID_Cases', 
        '<p>Please spend up to five minutes answering the following question: How many new cases of Coronavirus Disease 2019 (COVID-19) will be confirmed in the city of New York on October 31? The historical daily case counts for New York City can be viewed here: https://www1.nyc.gov/site/doh/covid/covid-19-data.page .</p>'
    ),
    (
        'COVID_Deaths', 
        '<p>Please spend up to five minutes answering the following question: How many new deaths of Coronavirus Disease 2019 (COVID-19) will be confirmed in the state of New York on October 31? The historical daily death counts for New York state can be viewed here: https://www1.nyc.gov/site/doh/covid/covid-19-data.page .</p>'
    ),
    (
        'Oil', 
        '<p>Please spend up to five minutes answering the following question: What will the daily price of Brent crude oil be on October 31? Historical oil price information can be viewed here: https://www.bloomberg.com/quote/CO1:COM .</p>'
    )
]