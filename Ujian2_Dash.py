import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import seaborn as sns
import dash_table
from dash.dependencies import Input, Output, State

def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
    )

tips = pd.read_csv('TSA_Samples.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1('Ujian Modul 2 Dashboard TSA'),
        html.Div(children='''
        Created by: Wiko
    '''),
        dcc.Tabs(
            children=[
                 dcc.Tab(value='Tab1',
                        label='Data Frame Tips',
                        children=[
                            html.Div(children=[
                                html.Div([
                                    html.P('Claim Site'),
                                    dcc.Dropdown(value='',
                                                 id='filter-smoker',
                                                 options=[{'label': 'Checked Baggage','value': 'Checked Baggage'}, 
                                                 {'label': 'Checkpoint','value': 'Checkpoint'},
                                                 {'label': 'Other','value': 'Other'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3'),
                                
                                html.Div([
                                    html.P('Sex'),
                                    dcc.Dropdown(value='',
                                                 id='filter-sex',
                                                 options=[{'label': 'Female','value': 'Female'}, 
                                                 {'label': 'Male','value': 'Male'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3'),
                                
                                html.Div([
                                    html.P('Day'),
                                    dcc.Dropdown(value='',
                                                 id='filter-day',
                                                 options=[{'label': 'Thur','value': 'Thur'}, 
                                                 {'label': 'Fri','value': 'Fri'},                     
                                                 {'label': 'Sat','value': 'Sat'},
                                                 {'label': 'Sun','value': 'Sun'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3'),
                                html.Div([
                                    html.P('Time'),
                                    dcc.Dropdown(value='',
                                                 id='filter-time',
                                                 options=[{'label': 'Lunch','value': 'Lunch'}, 
                                                 {'label': 'Dinner','value': 'Dinner'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3')

                            ],
                                     className='row'),
                            html.Br(),
                            html.Div([
                                html.P('Max Rows:'),
                                dcc.Input(id ='filter-row',
                                          type = 'number', 
                                          value = 10)
                            ], className = 'row col-3'),

                            html.Div(children =[
                                    html.Button('search',id = 'filter')
                             ],className = 'row col-4'),
                             
                            html.Div(id='div-table',
                                     children=[generate_table(tips)])
                        ]),
                dcc.Tab(
                    value='Tab2',
                    label='Scatter chart',
                    children=[
                        html.Div(children=dcc.Graph(
                            id='graph-scatter',
                            figure={
                                'data': [
                                    go.Scatter(x=tips[tips['NewClaimAmount'] == i]['NewClaimAmount'],
                                               y=tips[tips['NewCloseAmount'] == i]
                                               ['NewCloseAmount'],
                                               mode='markers',
                                               name='Day {}'.format(i))
                                    for i in tips['Status'].unique()
                                ],
                                'layout':
                                go.Layout(
                                    xaxis={'title': 'Tip'},
                                    yaxis={'title': ' Total Bill'},
                                    title='Tips Dash Scatter Visualization',
                                    hovermode='closest')
                            }))
                    ]),
                dcc.Tab(
                    value='Tab3',
                    label='Scatter chart',
                    children=[
                        html.Div(children = dcc.Graph(
        id = 'pie chart',
        figure = {
            'data':[
        go.Pie(labels = [i for i in tips['sex'].unique()], 
        values= [tips[tips['sex'] == i]['tip'].mean() for i in tips['sex'].unique()]
        )],
        'layout': go.Layout(title = 'Tip mean divided by Sex')}
    ), className = 'col-3')

    ], className = 'row')
]),
               
            ],
            ## Tabs Content Style
            content_style={
                'fontFamily': 'Arial',
                'borderBottom': '1px solid #d6d6d6',
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'padding': '44px'
            })
    ],
    #Div Paling luar Style
    style={
        'maxWidth': '1200px',
        'margin': '0 auto'
    })

@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'), 
    State(component_id = 'filter-smoker', component_property = 'value'),
    State(component_id = 'filter-sex', component_property = 'value'),
    State(component_id = 'filter-day', component_property = 'value'),
    State(component_id = 'filter-time', component_property = 'value')]
)
def update_table(n_clicks,row, smoker, sex, day, time):
    tips = pd.read_csv('TSA_Samples.csv')
    # if smoker == '' and sex == '' and day == '' and time == '':
    #     children = [generate_table(tips, page_size = row)]
    # elif smoker == '' and sex == '' and day == '' and time != '':
    #     children = [generate_table(tips[tips['time'] == time], page_size = row)]
    # elif smoker == '' and sex == '' and day != '' and time == '':
    #     children = [generate_table(tips[tips['day'] == day], page_size = row)]
    # elif smoker == '' and sex != '' and day == '' and time == '':
    #     children = [generate_table(tips[tips['sex'] == sex], page_size = row)]
    # elif smoker != '' and sex == '' and day == '' and time == '':
    #     children = [generate_table(tips[tips['smoker'] == smoker], page_size = row)]              
    # elif smoker == '' and sex == '' and day != '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['day'] == day)], page_size = row)]
    # elif smoker == '' and sex != '' and day == '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['sex'] == sex)], page_size = row)]
    # elif smoker != '' and sex == '' and day == '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker == '' and sex != '' and day != '' and time== '':
    #     children = [generate_table(tips[(tips['day'] == day) & (tips['sex'] == sex)], page_size = row)]
    # elif smoker != '' and sex == '' and day != '' and time== '':
    #     children = [generate_table(tips[(tips['day'] == day) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker != '' and sex != '' and day == '' and time == '':
    #     children = [generate_table(tips[(tips['smoker'] == smoker) & (tips['sex'] == sex)], page_size = row)]                  
    # elif smoker == '' and sex != '' and day != '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['day'] == day) & (tips['sex'] == sex)], page_size = row)]
    # elif smoker != '' and sex == '' and day != '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['day'] == day) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker != '' and sex != '' and day == '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['sex'] == sex) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker != '' and sex != '' and day != '' and time == '':
    #     children = [generate_table(tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['smoker'] == smoker)], page_size = row)]                               
    # else:
    #     children = [generate_table(tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['smoker'] == smoker) & (tips['time'] == time)], page_size = row)]               
    # return children 
    # if smoker != '':
    #     tips = tips[tips['smoker'] == smoker]
    # if sex != '':
    #     tips = tips[tips['sex'] == sex]
    # if day != '':
    #     tips = tips[tips['day'] == day]
    # if time != '':
    #     tips = tips[tips['time'] == time]
    # children = [generate_table(tips, page_size = row)]
    # return children
    
if __name__ == '__main__':
    app.run_server(debug=True)