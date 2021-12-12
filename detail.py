import dash_core_components as dcc
import dash_html_components as html


# def detail_header():
#     return html.Div(id='header', children=[
#         html.Div([html.H3('Project Detail', style={'text-align': 'center'})],
#                  className="ten columns"),
#     ], className="row")


def detail_page():
    """
    Returns cotents on about page
    """
    return html.Div(children=[dcc.Markdown('''
        ### Project Summary
        The website is witten by Python Dash to visualize our insights and analysis and deployed by Google Cloud Platform with Cron jobs to update the website everyday at ??? time EST.
        The big idea of this project is to summarize and analyze the potential impact of covid 19 for each community in the United States.        
        The project is consisting of:
        1. Collecting stock price information from open source covid API.     
        2. Exploring relationships among different important metrics to help researchers and residents better understand current/historical trends.    
        3. Summarize the data in a new and useful to extract insights based on different metrics and needs.    
        In this website, we show three daily updated graph visualizations and one interactive summarized data table. The purpose of these visualizations is to help individuals better evaluate the possibilities and risks of their residential regions. 
        The interactive map allows users to sort, select and delete significant distributions of the 7-day average metrics based on their interests, such as new covid cases today, in the county level. 7-day average metrics both tell the recent stories about the Covid and reduce variations compared to the daily values. For example, some counties would have many cases due to one public event in a day but the overall current risk levels in other blocks are still low.
        The infection rate (Rt) line chart shows the dynamic infection ratios in the state level so that users could evaluate the possibilities of infection by comparing it to other states. The Rt which is greater than one means high risk or probability of infection, while Rt which is lower than one means low risk or probability of infection. 
        The interactive area chart shows the first dose of vaccination ratio, which is calculated by the number of vaccination/population by state. The first dose may vary by type of vaccine, but for Moderna and Pfizer this indicates the number of people vaccinated with the first dose.   

        ### Team members.   
        Haoda Song: haoda_song@brown.edu
        Siyuan Li: siyuan_li2@brown.edu         

        ### Datasets
        The COVID Daily Updated Data is from CovidActNow API: https://apidocs.covidactnow.org/data-definitions. 
        Two main datasets are used in the analysis: historical data and new daily updated data. 
        Historical data would be updated once the data in the current date is updated. 
        For example, yesterday's data would be automatically recorded as the historical cumulative data and today's data would be updated as the new data.

        ### Data Handling 
        The raw-data is obtained by the online free API, CovidActNow. After cleaning and transforming the  
        into our desied form, we build a dataset based on them. We set up our database on MongoDB cluster and a update data_scraper 
        function has been implemented to enable the database to update every day. For data analysis and building model in this project, 
        we connect the mongo client to our MongoDB and obtain our desired data.   

        ### EDA & ETL: 
        https://colab.research.google.com/drive/1GPI1WR2FX_gJCzlFE11BvZ5h0Uu-UVMy?usp=sharing
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")