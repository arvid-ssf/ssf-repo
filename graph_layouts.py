import pandas as pd
#import modin.pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#dcc.graph instead of graph_objs
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State, MATCH, ALL, ALLSMALLER

colors = {
    'dark-blue' : '#004f67',
    'light-blue' : '#e0f1f8',
    'blue' : '#1db6eb',
    'transparent': 'rgba(0,0,0,0)',
    'background': '#004f67',
    'text': '#ee7203',
    'jumbotron' : '#1db6eb',
    'card' : '#ee7203',
}



#dcc.Loading(children=[
#], type='cube', fullscreen=True),


def graph_regular(n_clicks, df, width, dropdown_1, dropdown_2, value_1, value_2, dataset, graph_type):
    new_child = html.Div(
            id='new_child_regular',
            style={'width': width, 'height':'auto', 'display': 'inline-block', 'padding': '5px', 'margin-left' : '10px', 'margin-top' : '10px', 'margin-bottom' : '10px', 'backgroundColor': colors['dark-blue'], 'border-style':'none', 'border-color': colors['light-blue'], 'border-width':'2px', 'color':colors['light-blue']}, #'box-shadow': '5px 4px 8px black',
            className='resizeable',
            children=[
                #dbc.Card(
                #    id = 'card-regular-graph',
                #    style={'backgroundColor': colors['dark-blue'], 'margin-bottom':'10px', 'height':'120px', 'border-color':colors['blue'], 'border-width':'1px', 'box-shadow': '5px 2px 8px black', 'border-radius': '0'},
                #    className='light-blue-text',
                #    children=[
                        html.Div(
                            id={
                                'type': 'graph-data-set',
                                'index': n_clicks
                            },
                            children=dataset, 
                            style = {'text-align': 'center', 'margin-top':'10px'}), #, 'box-shadow': '3px 4px 6px black' 'text-transform' : 'uppercase',
                        html.Div(
                            id={
                                'type': 'graph-type-individual',
                                'index': n_clicks
                            },
                            children=graph_type, 
                            style = {'text-align': 'center'}), #, 'text-transform' : 'capitalize'
                        html.Hr(className="my-3"),
                        dbc.RadioItems(
                            id={
                                'type': 'dynamic-choice',
                                'index': n_clicks
                            },
                            style = {'text-align': 'center', 'margin':'5px'},
                            options=[{'label': 'Bar Chart', 'value': 'bar'},
                                     {'label': 'Line Chart', 'value': 'line'},
                                     {'label': 'Pie Chart', 'value': 'pie'},
                                     {'label': 'Sunburst Chart', 'value': 'sunburst'}],
                            value='bar',
                            labelStyle={'display': 'inline-block'},
                            inline = True
                        ),
                        html.Br(),
                        # dbc.RadioItems(
                        #     id={
                        #         'type': 'width-update',
                        #         'index': n_clicks
                        #     },
                        #     options=[{'label': '33%', 'value': '32.4%'},
                        #             {'label': '50%', 'value': '49%'},
                        #             {'label': '100%', 'value': '98.7%'}],
                        #     value='49%',
                        #     className='light-blue-text',
                        #     labelStyle={'display': 'inline-block'},
                        #     style = {'text-align':'center', 'margin-top': '20px'},
                        #     inline=True,
                        # ),




                #    ]
                #),
                #dcc.Loading(children=[
                                
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': n_clicks
                    },
                    style={'resize': 'both','overflow': 'auto', 'height':'600px'}, #https://community.plotly.com/t/cant-seem-to-change-default-height-on-graph/6742/2
                    #NOTE: 'figure' is a problem - not saved to json when saving dashboard
                    # figure = { 
                    #     'layout': dict(
                    #         hovermode = "closest", #
                    #         #height = 600, # 500 is a bit too big on a smartphone
                    #         legend = dict(
                    #             #font=dict(color='#7f7f7f'), 
                    #             orientation="h", # Looks much better horizontal than vertical
                    #             y=-0.15
                    #         ),
                    #     )
                    # },
                ),
                #], type='graph', fullscreen=False),
                html.Br(),
                #dbc.CardBody(
                #    children=[ 
                dcc.Slider(
			        id={
                        'type': 'dynamic-dpn-s',
                        'index': n_clicks
                    },
			        min=df['År'].min(),
			        max=df['År'].max(),
			        value=df['År'].max(), 
			        #marks={str(År): str(År) for År in df['År'].unique()},  #'style':{'color':colors['light-blue']} for h in range(0, 24)
                    marks={str(År) : {'label' : str(År), 'style':{'color':colors['light-blue']}} for År in df['År'].unique()},
                    className='opacity',
			        step=None,
			        disabled=False,
                    included=False,
			    ),
                #html.Br(),
                #For line graph
                # dcc.RangeSlider( 
                #         id={
                #         'type': 'dynamic-dpn-s',
                #         'index': n_clicks
                #         },
                #         min=df['År'].min(),
                #         max=df['År'].max(),
                #         step=None,
                #         marks={str(År): str(År) for År in df['År'].unique()}, #DO I NEED STR?
                #         #value=[df2['År'].min(), df2['År'].max()]
                #         value=[2019, df2['År'].max()] #TEST
                # ), 
                
                dbc.CardBody(
                    children=[
                        dbc.Row(
                            style={'color':colors['light-blue']},
                            className='justify-content-center',
                            justify='center',
                            align='center',
                            children=[
                                dbc.Col(html.Div(children='Region')),
                                dbc.Col(html.Div(children='KATEGORI',
                                    id={
                                        'type': 'title-1',
                                        'index': n_clicks
                                    },),),
                                dbc.Col(html.Div(children='SUB-KATEGORI',
                                    id={
                                        'type': 'title-2',
                                        'index': n_clicks
                                    },
                                ),)
                            ]
                        ),
                    #]
                #),
                
                #dbc.CardBody(
                    #children=[
                        dbc.Row(
                            justify='center',
                            align='end',
                            children=[
                                dbc.Col(dcc.Dropdown(
                                    id={
                                        'type': 'dynamic-dpn-reg',
                                        'index': n_clicks
                                    },
                                    style={'width': '100%', 'color' : colors['dark-blue'], 'border-radius':'0', 'cursor': 'pointer'},
                                    options=[{'label': r, 'value': r} for r in np.sort(df['Region'].unique())],
                                    value='Hela landet', 
                                    clearable=False,
                                    optionHeight=50,
                                    disabled=False,
                                    className='opacity hand',
                                ),),
                                dbc.Col(dcc.Dropdown(
                                    id={
                                        'type': 'dynamic-dpn-x',
                                        'index': n_clicks
                                    },
                                    style={'width': '100%', 'color' : colors['dark-blue'], 'border-radius':'0', 'cursor': 'pointer'},
                                    options=[{'label': c, 'value': c} for c in dropdown_1],
                                    value=value_1, #'ALLA BROTT',
                                    clearable=False,
                                    #persistence=True,
                                    #persistence_type = 'local'
                                    optionHeight=50,
                                    disabled=False,
                                    className='opacity hand',
                                )),
                                dbc.Col(dcc.Dropdown(
                                    id={
                                        'type': 'dynamic-dpn-col',
                                        'index': n_clicks
                                    },
                                    style={'width': '100%', 'color' : colors['dark-blue'], 'border-radius':'0', 'cursor': 'pointer'},
                                    options=[{'label': c, 'value': c} for c in dropdown_2], #INGEN SUB-KATEGORI
                                    value=value_2, #'INGEN SUB-KATEGORI',#['Region','BROTTSKATEGORI','BROTTSTYP','GEOGRAFISK ANKNYTNING','MÅLGRUPP'], #can have 'Region'
                                    clearable=False,
                                    optionHeight=50,
                                    disabled=False, 
                                    className='opacity hand',
                                )), 
                            ]
                        ),
                    ],
                ),
                html.Br(),
                #html.Hr(className="my-1", style={'height':'4px'}),
            ],
        )
            
        
    return new_child

def graph_periodicity(n_clicks,df, width, dropdown_1, dropdown_2, value_1, value_2, dataset):
	new_child = html.Div(
            style={'width': width, 'height':'auto', 'display': 'inline-block', 'padding': '5px', 'margin-left' : '10px', 'margin-top' : '10px', 'margin-bottom' : '10px', 'backgroundColor': colors['dark-blue'], 'border-style':'none', 'border-color': colors['light-blue'], 'border-width':'2px', 'color':colors['light-blue']}, #'box-shadow': '5px 4px 8px black',
            children=[
                html.Div(
                    id={
                        'type': 'graph-data-set_periodicity',
                        'index': n_clicks
                    },
                    children=dataset, #.capitalize() 
                    style = {'text-align': 'center','margin': 'auto'}),
                html.Div("Periodicitet", style = {'text-align': 'center','margin': 'auto'}),
                html.Hr(className="my-3"),
                dbc.RadioItems(
                    id={
                        'type': 'dynamic-choice-periodicity',
                        'index': n_clicks
                    },
                    style = {'text-align': 'center', 'margin':'5px'},
                    options=[{'label': 'Bar Chart', 'value': 'bar', 'disabled':'True'},
                             {'label': 'Scatter Chart', 'value': 'line'}, #Line
                             {'label': 'Pie Chart', 'value': 'pie', 'disabled':'True'},
                             {'label': 'Sunburst Chart', 'value': 'sunburst', 'disabled':'True'}],
                    value='line',
                    labelStyle={'display': 'inline-block'},
                    inline = True
                ),
                html.Br(),
                    
                
            
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph_periodicity',
                        'index': n_clicks
                    },
                    # figure = {
                    #     'layout': dict(
                    #         hovermode = "closest", #
                    #         #height = 600, # 500 is a bit too big on a smartphone
                    #         legend = dict(
                    #             #font=dict(color='#7f7f7f'), 
                    #             orientation="h", # Looks much better horizontal than vertical
                    #             y=-0.15
                    #         ),
                    #     )
                    # },
                    style={'resize': 'both','overflow': 'auto', 'height':'600px'},
                ),

                html.Br(),
                dcc.RangeSlider(
                		id={
                        'type': 'dynamic-dpn-rs_periodicity',
                        'index': n_clicks
                    	},
    					min=df['År'].min(),
			        	max=df['År'].max(),
					    step=None,
					    marks={str(År) : {'label' : str(År), 'style':{'color':colors['light-blue']}} for År in df['År'].unique()},
					    #value=[df2['År'].min(), df2['År'].max()]
                        className='opacity',
                        value=[2019, df['År'].max()], #TEST
                        #tooltip={'always_visible':False, 'placement':'bottom'}
				), 
                #html.Br(),
                dbc.CardBody(
                    children=[
                        html.Div(
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(html.Div(children='Region')),
                                        dbc.Col(html.Div(children='Category',
                                            id={
                                                'type': 'title-1.2',
                                                'index': n_clicks
                                            },
                                        ),),
                                        dbc.Col(html.Div(children='Sub-category',
                                            id={
                                                'type': 'title-2.2',
                                                'index': n_clicks
                                            },
                                        ),)
                                    ]
                                ),
                            ]
                        ),
                        
                        #dbc.Div(
                        #    children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(dcc.Dropdown(
                                            id={
                                                'type': 'dynamic-dpn-reg_periodicity',
                                                'index': n_clicks
                                            },
                                            style={'width': '100%', 'color' : colors['dark-blue'], 'border-radius':'0', 'cursor': 'pointer'},
                                            options=[{'label': r, 'value': r} for r in np.sort(df['Region'].unique())],
                                            value='Hela landet', 
                                            clearable=False,
                                            optionHeight=50,
                                            disabled=False,
                                            className='opacity hand',

                                        )),
                                        dbc.Col(dcc.Dropdown(
                                            id={
                                                'type': 'dynamic-dpn-x_periodicity',
                                                'index': n_clicks
                                            },
                                            style={'width': '100%', 'color' : colors['dark-blue'], 'border-radius':'0', 'cursor': 'pointer'},
                                            options=[{'label': c, 'value': c} for c in dropdown_1],#['ALLA BROTT', 'BROTTSKATEGORI','BROTTSTYP','GEOGRAFISK ANKNYTNING','MÅLGRUPP']],
                                            value= value_1,#'ALLA BROTT',
                                            clearable=False,
                                            optionHeight=50,
                                            disabled=False,
                                            className='opacity hand',
                                        ),),
                                        dbc.Col(dcc.Dropdown(
                                            id={
                                                'type': 'dynamic-dpn-col_periodicity',
                                                'index': n_clicks
                                            },
                                            style={'width': '100%', 'color' : colors['dark-blue'], 'border-radius':'0', 'cursor': 'pointer'},
                                            options=[{'label': c, 'value': c} for c in dropdown_2],# ['INGEN SUB-KATEGORI','BROTTSKATEGORI','BROTTSTYP','GEOGRAFISK ANKNYTNING','MÅLGRUPP']], #INGEN SUB-KATEGORI
                                            value=value_2,#'INGEN SUB-KATEGORI',#['Region','BROTTSKATEGORI','BROTTSTYP','GEOGRAFISK ANKNYTNING','MÅLGRUPP'], #can have 'Region'
                                            clearable=False, 
                                            optionHeight=50,
                                            disabled=False,
                                            className='opacity hand',
                                        ),),
                                    ]
                                ),
                            ],
                        ),
                        html.Br(),
                        #html.Hr(className="my-1", style={'height':'4px'}),
                    #],
                #),
            ]
        )
	return new_child







