import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
# Create a Dash app
app = dash.Dash(__name__)
# Define the latitude and longitude for the airplane's location
latitude = 48.866667
longitude = 2.333333
# Create a Plotly scattermapbox graph
fig = go.Figure(go.Scattermapbox(
    lat=[latitude],
    lon=[longitude],
    mode='markers',
    marker=dict(
        size=14,
        color='rgb(255, 0, 0)',
        symbol='airport',
        opacity=0.8
    ),
    text=['<b>Location</b><br>Airplane Information</b><br>Flight: XYZ123<br>'],
))
# Update the map layout
fig.update_layout(
    mapbox=dict(
        accesstoken='pk.eyJ1Ijoiemhhbm5hLTI3IiwiYSI6ImNsaXhwaXl6MDBhNDAzcW8xcGphbWpjZjcifQ.VFeWpKtMClATXytM5q_U5g',
        bearing=0,
        center=dict(
            lat=latitude,
            lon=longitude
        ),
        zoom=10
    ),
    showlegend=False
)
# Create the Dash layout
app.layout = html.Div([
    dcc.Graph(
        id='airplane-map',
        figure=fig
    )
])
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
