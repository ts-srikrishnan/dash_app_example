
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# 
# The dashboard will have two graphs: 
# 
#     The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
#     The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 
# 

# In[1]:


# Import all required libraries

import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# In[2]:


# Create dataset of Eurostat data

euro_data = pd.read_csv("nama_10_gdp_1_Data.csv")

#euro_data.head()

indicators = euro_data['NA_ITEM'].unique()
indicators.sort()

countries = euro_data['GEO'].unique()
countries.sort()


# ## Dashboards and Inputs

# In[3]:


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

euro_data1 = euro_data[euro_data['UNIT'] == 'Current prices, million euro']

#Layout of inputs
app.layout = html.Div([
    html.Div([

        #Input 1 (for Dashboard 1) - Dropdown with values of Indicators from dataset
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in indicators],
                placeholder="Select x-axis"
            )
        ],
        style={'width': '40%', 'display': 'inline-block'}),

        #Input 2 (for Dashboard 1) - Dropdown with values of Indicators from dataset
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in indicators],
                placeholder="Select y-axis"
            )
        ],style={'width': '40%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='dashboard1'), #Empty graph (for Dashboard 1)

    #Input 3 (for Dashboard 1) - Slider with values of years from dataset
    html.Div(dcc.Slider( 
        id='year--slider',
        min=euro_data['TIME'].min(),
        max=euro_data['TIME'].max(),
        value=euro_data['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in euro_data['TIME'].unique()},
    ), style={'marginRight': 50, 'marginLeft': 110},),
    
    html.Div([

        #Input 1 (for Dashboard 2)  - Dropdown with values of Indicators from dataset
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in indicators],
                placeholder="Select y-axis"
            )
        ],
        style={'width': '40%', 'marginTop': 45, 'display': 'inline-block'}),

        #Input 2 (for Dashboard 2)  - Dropdown with values of Countries from dataset
        html.Div([
            dcc.Dropdown( 
                id='country-dropdown',
                options=[{'label': i, 'value': i} for i in countries],
                placeholder="Select country"
            )
        ],style={'width': '40%', 'marginTop': 45, 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='dashboard2'), #Empty graph (for Dashboard 2)
    
])


#Callback function to create the required dashboard 1 based on the inputs
@app.callback(
    dash.dependencies.Output('dashboard1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    
    euro_data_yearly = euro_data[euro_data['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            #X-Axis based on column selected from filter
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['Value'],
            #Y-Axis based on column selected from filter
            mode='markers',
            marker={
                'size': 12,
                'opacity': 0.8,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 100, 'b': 50, 't': 25, 'r': 50},
            hovermode='closest'
        )
    }


#Callback function to create the required dashboard 2 based on the inputs
@app.callback(
    dash.dependencies.Output('dashboard2', 'figure'),
    [dash.dependencies.Input('yaxis-column2', 'value'),
     dash.dependencies.Input('country-dropdown', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name):
    
    euro_data_yearly = euro_data1[euro_data1['GEO'] == yaxis_column_name]
        
    return {
        'data': [go.Scatter(
            x=euro_data_yearly['TIME'].unique(),
            #X-Axis based on Year data in source data
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            #Y-Axis based on column selected from filter
            mode='lines',
            marker={
                'size': 12,
                'opacity': 0.8,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'type': 'linear'
            },
            yaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 100, 'b': 50, 't': 25, 'r': 50},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

