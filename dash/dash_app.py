import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# local imports
from src.pages.page1 import layout_page1


# CSS proposition
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Instantiation
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
# if an error occurs in callback, this argument avoids error and app continues (should be 'True') : suppress_callback_exceptions=True

# Definition of a variable for the header section
header_section = html.Div([
    html.H1('Lufthansa group flights dashboard', style={
            'color': 'mediumturquoise', 'textAlign': 'center'}),
    html.Br(),
    html.Button(dcc.Link('Weather alerts and global aviation statistics',
                         href='/weather-data')),
    dcc.Link('Aviation Stats',
                         href='https://aviation-safety.net/database/2022-analysis')
], style={'display': 'flex',
          'flexDirection': 'column',
          'alignItems': 'center',
          'padding': '8px',
          'background': '#0F576D'})

# Layout content creation
app.layout = html.Div([
    header_section,
    html.Div([
        # Have the path to the application
        dcc.Location(id='url', refresh=False),
        # Content of the page to be modified
        html.Div(id='page-content', children=[
            layout_page1,
        ])
    ])

])

# Index update
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])  
def display_page(pathname):
    if pathname == '/weather-data':
        from src.pages.page2 import layout_page2
        return layout_page2
    else:
        raise dash.exceptions.PreventUpdate  # nothing happens, the home page is the same


# to launch with Flask
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
