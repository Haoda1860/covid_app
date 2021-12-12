import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import page_1
import detail

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
page_1.register_callbacks(app)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

index_page = html.Div(
    style={'background-image': 'url("https://images.idgesg.net/images/article/2020/04/hand_holding_face_mask_surrounded_by_virus_morphology_covid-19_coronavirus_pandemic_by_rawpixel_wan_id_2317454_cc0_2400x1600-100839292-large.jpg?auto=webp&quality=85,70")',
    'verticalAlign':'middle','position':'fixed','width':'100%','height':'100%','top':'0px','left':'0px','z-index':'1000'},
    children=[
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H1("COVID Impact on Hospitals and Communities (USA)", style={'text-align': 'center','color':'#60a7e0'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Link('Detail', href='/detail', style={'font-size': '30px', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                              'justify-content': 'center', 'display': 'flex','color':'#60a7e0'}),
    html.Br(),
    dcc.Link('Insights', href='/page_1', style={'font-size': '30px', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                              'justify-content': 'center', 'display': 'flex','color':'#60a7e0'}),
    html.Br(),
    html.Br(),
    #html.A(style={'textAlign': 'center'}, children=[html.Span('Haoda Song', style={'textAlign': 'center'})], className="row", href='https://www.linkedin.com/in/haoda-song/'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H3("Authors: Haoda Song | Siyuan Li", style={'text-align': 'center','color':'#60a7e0'})
])


page_1_layout = page_1.layout


detail_layout = html.Div([detail.detail_header(), detail.detail_page()])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page_1':
        return page_1_layout
    elif pathname == '/detail':
        return detail_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=False)