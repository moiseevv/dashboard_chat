import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

# Load data
url = "https://raw.githubusercontent.com/tatyskya/dataset_for_ChatGPT/main/2018.csv"
df = pd.read_csv(url)

# Get top 10 countries
top_10 = df.sort_values(by='Score', ascending=False).head(10)

# Create app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    # Dropdown filter for country
    dcc.Dropdown(
        id='country-filter',
        options=[{'label': c, 'value': c} for c in df['Country or region'].unique()],
        multi=True,
        value=top_10['Country or region'].tolist()
    ),
    # Choropleth map
    dcc.Graph(id='choropleth-map'),
    # Bar chart
    dcc.Graph(id='bar-chart'),
    # Table
    dash_table.DataTable(
        id='table',
        columns=[{'name': c, 'id': c} for c in df.columns],
        data=top_10.to_dict('records')
    )
])


# Define callbacks
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('country-filter', 'value')
)
def update_choropleth_map(selected_countries):
    if selected_countries:
        filtered_df = df[df['Country or region'].isin(selected_countries)]
    else:
        filtered_df = top_10

    fig = px.choropleth(filtered_df, locations='Country or region', locationmode='country names', color='Score',
                        hover_name='Country or region', range_color=[0, 10], color_continuous_scale='Blues')
    fig.update_layout(title_text='Happiness Score by Country')
    return fig


@app.callback(
    Output('bar-chart', 'figure'),
    Input('country-filter', 'value')
)
def update_bar_chart(selected_countries):
    if selected_countries:
        filtered_df = df[df['Country or region'].isin(selected_countries)]
    else:
        filtered_df = top_10

    fig = px.bar(filtered_df, x='Score', y='Country or region', orientation='h')
    fig.update_layout(title_text='Top 10 Countries by Happiness Score')
    return fig


@app.callback(
    Output('table', 'data'),
    Input('country-filter', 'value')
)
def update_table(selected_countries):
    if selected_countries:
        filtered_df = df[df['Country or region'].isin(selected_countries)]
        filtered_df = filtered_df.sort_values(by='Score', ascending=False).head(10)
    else:
        filtered_df = top_10

    return filtered_df.to_dict('records')


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)