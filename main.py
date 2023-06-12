import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_table

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/tatyskya/dataset_for_ChatGPT/main/2018.csv')

# Create app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    # Dropdown to filter data by country or region
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in df['Country or region'].unique()],
        value=[],
        multi=True,
        placeholder='Select a country or region'
    ),
    # Choropleth map
    dcc.Graph(id='choropleth-map'),
    # Bar chart
    dcc.Graph(id='bar-chart'),
    # Table with top 10 countries
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.sort_values('Score', ascending=False).head(10).to_dict('records')
    )
])


# Define callbacks
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('table', 'data')],
    [Input('country-dropdown', 'value')]
)
def update_figures(selected_countries):
    # Filter data by selected countries
    if selected_countries:
        filtered_df = df[df['Country or region'].isin(selected_countries)]
    else:
        filtered_df = df

    # Choropleth map
    fig1 = px.choropleth(filtered_df, locations='Country or region', locationmode='country names', color='Score',
                         title='Happiness Score by Country or Region')

    # Bar chart
    fig2 = px.bar(filtered_df.sort_values('Score', ascending=False).head(10), x='Score', y='Country or region',
                  orientation='h', title='Top 10 Countries or Regions by Happiness Score')

    # Table with top 10 countries
    table_data = filtered_df.sort_values('Score', ascending=False).head(10).to_dict('records')

    return fig1, fig2, table_data


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)