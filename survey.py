from hemlock import Branch, Dashboard, Label, Page, route

@route('/survey')
def start():
    return Branch(
        Page(
            Dashboard(
                '''
                <p>What is the daily high temperature going to be in 
                Philadelphia tomorrow?</p>
                ''',
                src='/fcast/', aspect_ratio=(4, 3), var='Forecast'
            )
        ),
        Page(
            Label('<p>The end.</p>'), 
            terminal=True
        )
    )