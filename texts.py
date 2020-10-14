import numpy as np

consent_label = '''
<p>Hello! We are researchers at the University of Pennsylvania and are interested how you look forward to predict the future. We will show you some questions about the future and ask you to make a series of judgments. Please read the information below and if you wish to participate, indicate your consent.</p>

<p><b>Note.</b> This study is not compatible with mobile devices.</p>

<p><b>Purpose.</b> The purpose of this study is to explore how people think about the future.</p> 

<p><b>Procedure.</b> You will be asked to complete a survey that will take approximately 30 minutes.</p> 

<p><b>Benefits & Compensation.</b> If you complete the survey, we will pay you $5. In addition, you will receive a bonus of $25 if you are the most accurate participants in the study.</p> 

<p><b>Risks.</b> There are no known risks or discomforts associated with participating in this study.</p> 

<p>Participation in this research is completely voluntary. You can decline to participate or withdraw at any point in this study without penalty though you will not be paid.</p> 

<p><b>Confidentiality.</b> Every effort will be made to protect your confidentiality. Your personal identifying information will not be connected to the answers that you put into this survey, so we will have no way of identifying you. We will retain anonymized data for up to 5 years after the results of the study are published, to comply with American Psychological Association data-retention rules.</p> 

<p><b>Questions</b> Please contact the experimenters if you have concerns or questions: mellers@wharton.upenn.edu. You may also contact the office of the University of Pennsylvania’s Committee for the Protection of Human Subjects, at 215.573.2540 or via email at irb@pobox.upenn.edu.</p>
'''

# questions the participant should forecast
fcast_questions = [
    (
        'S&P', 
        '<p>Please spend up to five minutes answering the following question: What will the end-of-day value of the S&P 500 Index be on October 16? <a href="https://www.bloomberg.com/quote/SPX:IND" target="_blank">Click here to view historical values of S&P 500 Index.</a></p>'
    ),
    (
        'Temperature', 
        '<p>Please spend up to five minutes answering the following question: What will the maximum daily temperature in Central Park, New York City be on October 16?  <a href="https://w2.weather.gov/climate/index.php?wfo=okx" target="_blank">Click here to view the historical daily temperatures in Central Park.</a></p>'
    ),
    (
        'COVID_Cases', 
        '<p>Please spend up to five minutes answering the following question: How many new cases of Coronavirus Disease 2019 (COVID-19) will be confirmed in the city of New York on October 16? <a href="https://www1.nyc.gov/site/doh/covid/covid-19-data.page" target="_blank">Click here to view the historical daily case counts for New York City.</a></p>'
    ),
    (
        'COVID_Deaths', 
        '<p>Please spend up to five minutes answering the following question: How many new deaths of Coronavirus Disease 2019 (COVID-19) will be confirmed in the state of New York on October 16? <a href="https://www1.nyc.gov/site/doh/covid/covid-19-data.page" target="_blank">Click here to view the historical daily death counts for New York state.</a></p>'
    ),
    (
        'Oil', 
        '<p>Please spend up to five minutes answering the following question: What will the daily price of Brent crude oil be on October 16? <a href="https://www.bloomberg.com/quote/CO1:COM" target="_blank">Click here to view historical oil price information.</a></p>'
    )
]

completion = '''
<p>Thank you for completing the study! <b>Your completion code is hlk235.</b>
</p>
'''