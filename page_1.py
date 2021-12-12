import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output
import io
import pandas as pd
import numpy as np
import requests
from urllib.request import urlopen
import json
import plotly.express as px
import plotly.graph_objects as go
#Loading Data via RESTAPI
#county-level historical covid data in U.S.
hist_days = requests.get("https://api.covidactnow.org/v2/counties.timeseries.csv?apiKey=2f065bb0cf83461aab6c054646afc8cf").content
#county-level new covid data (daily updated) in U.S.
new_day = requests.get("https://api.covidactnow.org/v2/counties.csv?apiKey=2f065bb0cf83461aab6c054646afc8cf").content

#fips codebook
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


#data functions
def plot_data():
    #map data
    new_df = pd.read_csv(io.StringIO(new_day.decode('utf-8')))
    new_df['fips'] = new_df['fips'].apply(lambda x: str(0)+str(x) if len(str(x))<5 else x)
    map_us = new_df[['fips','county','state','actuals.newCases','actuals.newDeaths','riskLevels.overall','actuals.hospitalBeds.currentUsageTotal','actuals.hospitalBeds.capacity']]
    #rt data
    hist_df = pd.read_csv(io.StringIO(hist_days.decode('utf-8')))
    rt_us = hist_df.groupby(['state','date']).agg({'metrics.infectionRate':['mean']})['metrics.infectionRate'].reset_index(level=['state','date'])
    #vacc data
    hist_df["date"]=pd.to_datetime(hist_df["date"])
    vac_us = hist_df.groupby(['state','date']).agg({'metrics.vaccinationsInitiatedRatio':['mean'],'metrics.vaccinationsCompletedRatio':['mean']}).stack().reset_index(level=['state','date'])
    vac_us=vac_us[(vac_us["date"] > '2020-12-31')]
    ##Most Recent 7 days data
    cutoff_date = hist_df["date"].iloc[-1] - pd.Timedelta(days=7)
    df_7days = hist_df[hist_df['date'] > cutoff_date] 
    df_7days = df_7days[['date','county','state','metrics.caseDensity', 
                        'actuals.newCases','actuals.newDeaths',
                        'riskLevels.overall',
                        'metrics.vaccinationsInitiatedRatio',
                        'metrics.vaccinationsCompletedRatio']]
    df_7days = df_7days.groupby(['county','state'],as_index=False)[['metrics.caseDensity', 'actuals.newCases', 'actuals.newDeaths',
                                                                    'riskLevels.overall', 'metrics.vaccinationsInitiatedRatio','metrics.vaccinationsCompletedRatio']].mean().round(
                                                                        {'metrics.caseDensity':2,'actuals.newCases':0,'actuals.newDeaths':0,'riskLevels.overall':0,
                                                                        'riskLevels.overall':0,'metrics.vaccinationsInitiatedRatio':2, 'metrics.vaccinationsCompletedRatio':2})
    df_7days.rename(columns={'date':'Date','county':'County','state':'State','metrics.caseDensity':'Avg. Case Density', 
                        'actuals.newCases':'Avg. New Cases','actuals.newDeaths':'Avg. New Death',
                        'riskLevels.overall':'Avg. CDC Risk Level',
                        'metrics.vaccinationsInitiatedRatio':'Avg. First Dose Vacc',
                        'metrics.vaccinationsCompletedRatio':'Avg. Second Dose Vacc'}, inplace=True)
    return map_us, rt_us, vac_us, df_7days

map_us, rt_us, vac_us, df_7days = plot_data()
map_values = ['actuals.newCases','actuals.newDeaths','riskLevels.overall','actuals.hospitalBeds.currentUsageTotal','actuals.hospitalBeds.capacity']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
layout = html.Div(children=[
    html.Br(),
    html.Br(),

    html.Div([html.H1("COVID-19 Daily Impact")], style={'textAlign': "center", "padding-bottom": "30"}),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
    html.H2("7-Day Average Statistics"),
    dash_table.DataTable(
        id='datatable-row-ids',columns=[{'name': i, 'id': i, 'deletable': True} for i in df_7days.columns],
        data=df_7days.to_dict('records'),
        editable=True, filter_action="native", sort_action="native",sort_mode='multi', row_selectable='multi', row_deletable=True, selected_rows=[],
        page_action='native', page_current= 0, page_size= 10),
    dcc.Dropdown(id='test-dropdown', options=[{'label': i, 'value': i} for i in df_7days.columns], value=[i for i in df_7days.columns], multi=True)
    ]),    

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        html.H2(["Map Title"]),
        dcc.Dropdown(id='map_value', value='actuals.newCases',options=[{'label': "New Case Today", 'value': 'actuals.newCases'},
        {'label': "New Death Today", 'value': 'actuals.newDeaths'}, {'label': "Current Risk Level", 'value': 'riskLevels.overall'}, 
        {'label': "HospitalBeds Usage", 'value': 'actuals.hospitalBeds.currentUsageTotal'}, {'label': "HospitalBeds Capacity", 'value': 'actuals.hospitalBeds.capacity'}]),
        dcc.Graph(id='maps')]
        ),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        html.H2("Rt Title"),
        dcc.Dropdown(id='state_rt', value='state', options=[{'label': x, 'value': x} for x in rt_us['state'].unique()], multi=True),
        dcc.Graph(id='rt_lines')]
        ),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        html.H2("Vaccienation Area Chart Title"),
        dcc.Dropdown(id='state_vac', value='state', options=[{'label': x, 'value': x} for x in vac_us['state'].unique()], multi=True),
        dcc.Graph(id='vac_area')]
        ),

    html.Br(),
    html.Br()
])
def register_callbacks(app):
    #7-day avg table
    @app.callback(
    Output('datatable-row-ids', 'data'),
    Input('test-dropdown', 'value'))
    def update_table(input_data):
        return df_7days[input_data].to_dict('records')

    #map callback
    @app.callback(
        dash.dependencies.Output("maps", "figure"),
        [dash.dependencies.Input("map_value", "value")]
    )
    def make_map(values):
        fig = px.choropleth(map_us, geojson=counties, locations='fips',
                        color=values, color_continuous_scale=px.colors.diverging.Portland,
                        scope="usa", hover_name='county',hover_data={'fips':True,'state':True,'county':False,'actuals.newCases':True})
        fig.update_traces(marker_line_width=0, marker_opacity=0.8)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(showsubunits=True, subunitcolor="black")
        fig.update_layout(showlegend=False)
        return fig

    #Rt callback
    @app.callback(
        dash.dependencies.Output("rt_lines", "figure"),
        [dash.dependencies.Input("state_rt", "value")]
    )
    def make_rtline(values1):
        fig = go.Figure()
        for i,v in enumerate(values1):
            data = rt_us[rt_us['state'] == v]
            fig.add_trace(go.Scatter(
                x=data['date'], y=data['mean'],
                mode='lines',
                name=v))
        fig.update_layout()
        return fig

    #vac callback
    @app.callback(
        dash.dependencies.Output("vac_area", "figure"),
        [dash.dependencies.Input("state_vac", "value")]
    )
    def area_vac(values2):
        fig = go.Figure()
        for i, v in enumerate(values2):
            data = vac_us[vac_us['state'] == v]
            fig.add_trace(go.Scatter(
                x=data['date'], y=data['metrics.vaccinationsInitiatedRatio'],
                hoverinfo='x+y',
                mode='lines',
                name=v,
                stackgroup='one'))
        fig.update_layout()
        return fig
    
if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = layout
    register_callbacks(app)
    app.run_server(debug=True, port=8851)
