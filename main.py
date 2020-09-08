#--------manipulate data--------

# - year is not always an integer (must be for slicer)
#dcc.Store
#hover options 
#displayed values (when saving to pdf)


#TO-DO
#callback n_clicks run dashboard
#Validate data
#convert excel to csv?
#save dashboard - how?
#label or color is often hidden i pie chart
#sunchart rounds digits - more decimals!
#periodicity line label
#4 kap att det är totalt är missvisande... alla kategorier ej inkl.
#ad month/whole year button to tables (to present all combinations)
#2020 prel. is an str in tables
#updated program - lose saved dashboards
#check book notes
#feather all dataframes?
#no col_value allowed (disable)
#If range[ÅR] iis not min, iniclude last month from year before
# line_group and dataseet for periodicity
#check sum() for all (min_count=1 necessary?)
#set right parameters under periiodicity figs (and other)
#labels on axes
#change dpn to chapters instead!

#NEXT 
#PREPARE PRESENTATION
#update_graphs: structure (repeating code)
#VALIDATE periodicity
#Variable names and text (en/sv)





import pandas as pd
#from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow

#import requests #new
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#dcc.graph instead of graph_objs
import dash_table
import plotly.express as px
#import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State, MATCH, ALL, ALLSMALLER
from dash import no_update
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.exceptions import PreventUpdate
from graph_layouts import *
from update_graphs import *
from structure_latest import *
import calendar
#import pickle
try:
   #import cPickle as pickle
   import _pickle as cPickle
except:
   import pickle
import json
import os
from operator import itemgetter
import base64
import glob
import shutil
import plotly.io as pio
from flask import Flask
#from platform import python_version
#print(python_version())


pd.options.plotting.backend = "plotly" 
#pd.set_option('use_inf_as_na', True)
                                                                        
#PICKLE 
#excel_file = "strukturerad_tabell.xlsx" 
# df1 = pd.read_excel(excel_file,sheet_name="Strukturerad_Helår") 
# df1.to_pickle("pickle/df1.pkl")
# df2 = pd.read_excel(excel_file,sheet_name="Strukturerad_Månader")
# df2.to_pickle("pickle/df2.pkl")
# #df3 = pd.read_excel(excel_file,sheet_name='Strukturerad_per_månad') #Wrong: JAN ends up under 'Helår' year 2020
# df4 = pd.read_excel(excel_file,sheet_name="Strukturerad_Helår_Total")
# df4.to_pickle("pickle/df4.pkl")
# df5 = pd.read_excel(excel_file,sheet_name="Strukturerad_Månader_Total")
# df5.to_pickle("pickle/df5.pkl")

#UNPICKLE
# import time
# s = time.time()
# df1 = pd.read_pickle("pickle/df1.pkl")
# df2 = pd.read_pickle("pickle/df2.pkl")
# df4 = pd.read_pickle("pickle/df4.pkl")
# df5 = pd.read_pickle("pickle/df5.pkl")
# e = time.time()
# print("Pandas Loading Time = {}".format(e-s))

#hdf5
#import time
#s = time.time()
#df1 = pd.read_hdf("hdf5/df1.h5", key='df')
#df2 = pd.read_hdf("hdf5/df2.h5", key='df')
#df4 = pd.read_hdf("hdf5/df4.h5", key='df')
#df5 = pd.read_hdf("hdf5/df5.h5", key='df')
#e = time.time()
#print("Pandas Loading Time = {}".format(e-s))



#comment FEATHER

#feather
#import time
#s = time.time()
df1 = pd.read_feather("feather/df1.feather")
df2 = pd.read_feather("feather/df2.feather")
df3 = pd.read_feather("feather/df3.feather")
df4 = pd.read_feather("feather/df4.feather")
df5 = pd.read_feather("feather/df5.feather")
#e = time.time()
#print("Pandas Loading Time = {}".format(e-s))

# df1 = pd.read_excel(excel_file,sheet_name="Fr. o. m. 2019 (helår)") 
# df2 = pd.read_excel(excel_file,sheet_name="Fr. o. m. 2019 (månader)")
# df3 = pd.read_excel(excel_file,sheet_name="Fr. o. m. 2019 (helår|månader)") #Wrong: JAN ends up under 'Helår' year 2020
# df4 = pd.read_excel(excel_file,sheet_name="Kapitel (helår)")
# df5 = pd.read_excel(excel_file,sheet_name="Kapitel (månader)")





print('START------------------------------------------------------------------------------------------------------------------------')


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]

#server = Flask(__name__)




app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #, server=server
server = app.server
app.title = 'SSF Dashboards'
#



# def get_kittens():
#     kittens = requests.get('https://cat-fact.herokuapp.com/facts')
#     json_data = kittens.json()
#     json_data = json_data['all']
#     df = pd.DataFrame(json_data)
#     with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#         #print(df['all'])
#         print(df.columns)
#     return ([
#             html.Table(
#                 className='table-weather',
#                 children=[
#                     html.Tr(
#                         children=[
#                             html.Td(
#                                 children=[
#                                     str(data)
#                                 ]
#                             )
#                         ]
#                     )
#             for data in df['text']
#         ])
#     ])



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

pio.templates["plotly_dark"].update({
#e.g. you want to change the background to transparent
'layout':{'paper_bgcolor': colors['dark-blue'],
'plot_bgcolor': colors['dark-blue'],'font_color':colors['light-blue']}
#'layout':{'paper_bgcolor': colors['blue'],
#'plot_bgcolor': colors['blue']},
})

pio.templates["plotly_white"].update({
#e.g. you want to change the background to transparent
'layout':{'paper_bgcolor': colors['light-blue'],
'plot_bgcolor': colors['light-blue']}
})





#FOR DAQ DARK
# theme = {
#     'dark': False,
#     'detail': '#007439',
#     'primary': '#00EA64', 
#     'secondary': '#6E6E6E'
# }

#write to HTML
#fig =px.scatter(x=range(10), y=range(10))
#fig.write_html("file.html")

#dcc.Interval!!!!!!!!!!!!!!!!!!!!!!!!!!!!
app.layout = html.Div(
    style={'backgroundColor': colors['dark-blue'], 'padding-bottom' : '100px','width':'100%', 'height':'100%'},  #'ff-dagny-web-pro,sans-serif' 'font-family':"SSF_font",
    id='all',
    children=[
        html.Header(),
        #dcc.Store(id="store"),
        dbc.Navbar(
            id='navbar',
            children =
                [
                    dbc.Row(
                        [
                            dbc.Col(html.A(html.Img(src='/assets/SSF-assets/SSF_text_vit.png', style={'width':'30%'}),
                                href="https://www.stoldskyddsforeningen.se/privat/",
                                ),
                                #width={"offset": 1}
                            ),

                            #dbc.Col(html.A(html.Img(src='/assets/bra_1.png', style={'width':'15%', 'text-align':'right'}),
                            #    href="http://statistik.bra.se/solwebb/action/index",
                            #    ),
                            #    width={"offset": 1},
                            #    style={'text-align':'right'}
                            #),
                        ],
                        #className="ml-auto flex-nowrap mt-3 mt-md-0",
                        align="center",
                        #no_gutters=True,
                    ),
                    
                
                
                
            ],
            color=colors['dark-blue'],
            dark=True,
            sticky='top'
        ),

        dbc.Jumbotron(
            id = 'jumbotron-header1',
            style={'height':'250px', 'backgroundColor': colors['dark-blue'], 'color':colors['light-blue'], 'margin-bottom': '0px'}, #'font-family':"'Lucida Console', Courier, monospace", 'font-family':"SSF_font",
            children=[
                html.H1("SSF Dashboards", id='header', className="display-3", style={'text-align': 'center', 'text-shadow': '3px 4px 6px black'}),
                #html.Hr(className="my-2"),
            ]
        ),

        
        html.Div(
            className="accordion",
            children = [
                dbc.Card(
                    children=[
                        dbc.CardHeader(
                            html.H2(
                                children=[
                                    html.Img(src='/assets/SSF-assets/PNG/23.png', style={'width':'4%'}),
                                    dbc.Button(
                                        "Dashboards",
                                        #style={'margin-left':'10px'},
                                        color=colors['dark-blue'],
                                        className='dark-blue-text opacity-inverse',
                                        size='lg',
                                        id="group-1-toggle",
                                        #outline=True,
                                    ),

                                ]
                            ),
                            style={'backgroundColor': colors['light-blue']},
                        ),
                        dbc.Collapse(
                            dbc.CardBody(
                                style={'margin-bottom' : '150px'},
                                children=[
                                html.P(
                                    children=[
                                        dbc.Alert(
                                            "Successfully saved dashboard!",
                                            id='save-output-right',
                                            is_open=False,
                                            fade=True,
                                            dismissable=True,
                                            duration=4000,
                                        ),
                                        dbc.Alert(
                                            "You must provide a dashboard name!",
                                            id='save-output-wrong',
                                            is_open=False,
                                            fade=True,
                                            color='danger',
                                            dismissable=True,
                                            duration=8000,
                                        ),
                                        dbc.Alert(
                                            "Successfully updated dashboard!",
                                            id='override-success',
                                            is_open=False,
                                            fade=True,
                                            dismissable=True,
                                            duration=4000,
                                        ), 
                                        #daq.ToggleSwitch(
                                        #    id='daq-light-dark-theme',
                                        #    label=['Light', 'Dark'],
                                        #    color=colors['light-blue'],
                                        #    style={'width': '150px', 'padding':'5px', 'margin-left': '620px'},
                                        #    size=30,
                                        #    #label='Background', 
                                        #    value=True
                                        #   ),
                                        #     html.Div(
                                        #     id='dark-theme-component-demo',
                                        #     children=[
                                        #         daq.DarkThemeProvider(theme=theme)
                                        #     ],
                                        #     style={'display': 'block', 'margin-left': 'calc(50% - 110px)'}
                                        # ),
                                    ]
                                ),

                                
                               
                                dbc.Card(
                                    id = 'card-header',
                                    style={'height':'230px', 'box-shadow': '5px 2px 8px black'}, #'border-color':colors['light-blue'], 'border-width':'2px'
                                    className='tab-dark-blue',
                                    children=[ 
                                        
                                                #html.Div('Data:',
                                                #    style={'float': 'left','margin-left': '20px', 'margin-top': '10px', 'margin-right': '10px'},
                                                #),
                                                
                                        dbc.CardHeader(
                                            children=[
                                                #html.Div('DATA', style={'float':'right','color':colors['light-blue'], 'margin':'auto'}),
                                                dbc.Tabs(
                                                    [   
                                                        dbc.Tab(label="Kapitel och paragrafer", tab_id='Kapitel och paragrafer', style={'backgroundColor':colors['blue']}, labelClassName='tab-text', tabClassName="tab-box"),
                                                        dbc.Tab(label="Brottskoder (fr. o. m. 2019)", tab_id='Brottskoder (fr. o. m. 2019)', labelClassName='tab-text', tabClassName="tab-box"), #, label_style={"color": colors['dark-blue']}
                                                    ],
                                                    id="data-set",
                                                    card=True, #if tab in cardHeader
                                                    active_tab="Kapitel och paragrafer",
                                                    style={'margin-left':'0px'},

                                                ),

                                            ],
                                            style={"backgroundColor": colors['dark-blue'], 'border-radius': '0', 'border-style':'solid', 'border-color':colors['light-blue'], 'border-width':'2px'},
                                            #className='tab-dark-blue',
                                        ),
                                        
                                        dbc.CardBody(
                                            style={"backgroundColor": colors['light-blue'], 'border-radius': '0'},
                                            children=[
                                                # dbc.Tabs(
                                                #     [   
                                                #         dbc.Tab(label="Enskild region (inkl. hela landet)", tab_id='helår', style={'backgroundColor':colors['blue']}, labelClassName='tab-text', tabClassName="tab-box"),
                                                #         dbc.Tab(label="Alla regioner", tab_id='regioner', labelClassName='tab-text', tabClassName="tab-box"), #, label_style={"color": colors['dark-blue']}
                                                #         dbc.Tab(label="Periodicitet", tab_id='periodicitet', labelClassName='tab-text', tabClassName="tab-box"),
                                                #     ],
                                                #     id="data-sub-set",
                                                #     card=False, #if tab in cardHeader
                                                #     active_tab="helår",
                                                #     style={'margin-left':'0px'},

                                                # ),
                                                #html.Br(),
                                                #dbc.Tabs(
                                                #    [
                                                #        dbc.Tab(label="Ensklid region (inkl. hela landet)", labelClassName='dark-blue-text'), #tabClassName="ml-auto"
                                                #        dbc.Tab(label="Alla regioner", labelClassName='dark-blue-text'),
                                                #        dbc.Tab(label="Periodicitet", labelClassName='dark-blue-text'),
                                                #    ]
                                                #),
                                                # dbc.RadioItems(
                                                #     id='data-set',
                                                #     options=[{'label': 'Kapitel', 'value': 'kapitel'},
                                                #     {'label': 'Fr. o. m. 2019', 'value': 'fr. o. m. 2019'}], #
                                                #     value= 'kapitel', 
                                                #     labelStyle={'display': 'inline-block'},
                                                #     style = {'text-align': 'left','margin-left': '20px', 'margin-top': '10px'},
                                                #     inline=True,
                                                # ),
                                                
                                                #html.Hr(className="my-3"), #my-3
                                                daq.ToggleSwitch(
                                                  id='my-daq-booleanswitch',
                                                  value=True,
                                                  color=colors['blue'], #black
                                                  style = {'float': 'right','margin': '3px'},
                                                  size=30,
                                                  #label='Graph background'
                                                ), 
                                                dbc.RadioItems(
                                                    id='graph-type',
                                                    options=[{'label': 'Enskild region (inkl. hela landet)', 'value': 'Enskild region (inkl. hela landet)'}, #dbc.Popover
                                                            {'label': 'Alla regioner', 'value': 'Alla regioner'},
                                                            {'label': 'Periodicitet', 'value': 'Periodicitet'}],
                                                    value='Enskild region (inkl. hela landet)',
                                                    labelStyle={'display': 'inline-block'},
                                                    style = {'text-align': 'left','margin-left': '20px', 'margin-top': '20px'},
                                                ),                                             
                                                
                                                #html.Hr(className='my-3'),
                                                dbc.Row(
                                                    children=[
                                                        dbc.Col(
                                                            dbc.InputGroup(
                                                                children=[   
                                                                    dbc.InputGroupAddon(dcc.ConfirmDialogProvider(
                                                                                children=html.Div(dbc.Button('Spara dashboard', color="info", id='save-dash', size='md', className='btn-dark-blue', n_clicks=0, style = {'border-radius': '0'})),
                                                                                id='save-confirmation',
                                                                                message='Är du säker att du vill spara detta dashboard?',
                                                                                submit_n_clicks=0
                                                                            ),
                                                                            #addon_type='append',
                                                                    ),
                                                                    dbc.Input(id="json-file-name", placeholder="Namn på dashboard...", type="text", debounce=True, style = {'border-radius': '0'}, loading_state={'is_loading':True}), 
                                                                    

                                                                ],
                                                                #style={'width':'25%'},
                                                                size='md'
                                                            ),
                                                            width={"size": 4, 'offset':8}

                                                        ),
                                                    ],
                                                    align="center",
                                                    #style={'margin-bottom':'20px'}
                                                ),                                                        

                                                

                                                
                                                
                                                dcc.ConfirmDialog(
                                                    id='override',
                                                    message='Dashboard already exists! Do you wish to override the old dashboard?',
                                                    submit_n_clicks=0
                                                ),
                                            
                                            ]
                                        ),
                                                                                      
                                            
                                        
                                    ]

                                ),
                                
                                
                                dbc.RadioItems(
                                    id='width',
                                    options=[{'label': '33%', 'value': '32.4%'},
                                            {'label': '50%', 'value': '49%'},
                                            {'label': '100%', 'value': '98.7%'}],
                                    value='49%',
                                    className='light-blue-text',
                                    labelStyle={'display': 'inline-block'},
                                    style = {'text-align':'center', 'margin-top': '20px'},
                                    inline=True,
                                ),
                                #html.Br(),
                                dbc.Row(
                                    [   #colors['blue']
                                        dbc.Col(
                                            #dbc.ButtonGroup(
                                            #[
                                                dbc.Button('Lägg till graf', color='primary', id='add-chart', className='btn-blue', n_clicks=0, outline=False, style={'margin-left':'25px'}),
                                            #    dbc.DropdownMenu(
                                        #             [dbc.DropdownMenuItem("33%",), dbc.DropdownMenuItem("50%"), dbc.DropdownMenuItem("100%")],
                                        #             id='width-dpn',
                                        #             label="Bredd",
                                        #             className='blue-text',
                                        #             group=True,
                                        #             direction='down',
                                        #             color='info',
                                                    
                                        #         ),
                                        #     ]
                                        # )
                                        ), 



                                        dbc.Col(
                                                dbc.ButtonGroup(
                                                [dbc.Button('Radera senaste graf', color="danger", id='remove-chart', className='btn-dark-blue', n_clicks=0, size='sm'), #style={'border-radius':'0'}
                                                dbc.Button('Radera alla grafer', color="danger", id='delete-all-charts', className='btn-dark-blue', n_clicks=0, size='sm')],
                                                style={'margin-right':'25px'} 
                                            ),
                                            width={"offset": 1}
                                            ),
                                        
                                    ],
                                    align="end",
                                    #style={'margin-top':'20px'}
                                ),
                                 
  
                                #html.Hr(className="my-2"),
                                #dcc.Loading(children=[
                                html.Div(id='container', children=[]), #set size?
                                #], type='graph', fullscreen=False),
                            ]),
                        id="collapse-1",
                        style={'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},
                    ),
                    ],
                ),
                

                dbc.Card(
                    children=[
                        dbc.CardHeader(
                            html.H2(
                                children=[
                                    html.Img(src='/assets/SSF-assets/PNG/7.png', style={'width':'4%'}),
                                    dbc.Button(
                                        "Sparade dashboards",
                                        color=colors['dark-blue'],
                                        className='dark-blue-text opacity-inverse',
                                        size='lg',
                                        id="group-2-toggle",
                                        #outline=True,
                                    ),

                                ]
                            ),
                            style={'backgroundColor': colors['light-blue']},
                        ),
                        dbc.Collapse(
                            dbc.CardBody(
                                children=[
                                    dbc.Alert(
                                        "Successfully deleted dashboard!",
                                        id='delete-output-right',
                                        is_open=False,
                                        fade=True,
                                        dismissable=True,
                                        duration=4000,
                                    ),
                                    dbc.Alert(
                                        "Choose a dashboard to delete!",
                                        id='delete-output-wrong',
                                        is_open=False,
                                        fade=True,
                                        color='danger',
                                        dismissable=True,
                                        duration=8000,
                                    ),
                                    
                                    dbc.CardBody(
                                        id = 'jumbotron-header2',
                                        style={'backgroundColor': colors['dark-blue'], 'margin':'50px', 'border-radius': '0', 'height':'230px', 'box-shadow': '5px 2px 8px black', 'border-style':'solid', 'border-color':colors['light-blue'], 'border-width':'2px'},
                                        children=[
                                            dcc.Dropdown( #ListGroup
                                                id='json-dpn',
                                                style={'margin-top':'50px'},
                                                #options=[{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("json/*.json")], #name cant contain '.'
                                                options = [{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("dashboards/*")],
                                                #multi=True, #add several, indices clash, perhaps do copy of dash (new graphs)
                                                placeholder='Välj dashboard',
                                                #persistence=True,
                                                #value='BROTTSKATEGORI',
                                                #clearable=False,
                                            ),
                                            html.Br(),
                                            #dbc.Button('Run dashboard', color="info", id='run-dashboards', n_clicks=0, style = {'text-align': 'left','margin': 'auto'}),
                                            #dbc.Button('Delete dashboard', color="info", id='delete-dashboard', n_clicks=0, style = {'text-align': 'left','margin': 'auto'}),

                                            dbc.Row(
                                                children=[
                                                    dbc.Col(dbc.Button('Run dashboard', color="info", id='run-dashboards', className='btn-blue', n_clicks=0, style = {'text-align': 'left','margin': 'auto'})),
                                                    dbc.Col(dcc.ConfirmDialogProvider(
                                                                children=html.Div(dbc.Button('Delete dashboard', color="danger", id='delete-dashboard', className='btn-dark-blue', size='sm', n_clicks=0, style = {'margin': 'auto'})),
                                                                id='delete-confirmation',
                                                                message='Är du säker att du vill radera detta dashboard?',
                                                                submit_n_clicks=0
                                                            ),
                                                            width={"offset": 1},
                                                    ),
                                                ],       
                                                style={'margin-right':'25px'},
                                                align="center",
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            id="collapse-2",
                            style={'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},
                        ),
                    ]
                ),
                
                dbc.Card(
                    children=[
                        dbc.CardHeader(
                            html.H2(
                                children=[
                                    html.Img(src='/assets/SSF-assets/PNG/1.png', style={'width':'4%'}),
                                    dbc.Button(
                                        "Tabell",
                                        color=colors['dark-blue'],
                                        className='dark-blue-text opacity-inverse',
                                        size='lg',
                                        id="group-4-toggle",
                                        #outline=True,
                                    ),

                                ]
                            ),
                            style={'backgroundColor': colors['light-blue']},
                        ),
                        dbc.Collapse(
                            dbc.CardBody(
                                style={'margin-bottom' : '150px'},
                                children=[

                                    dbc.CardBody(
                                        id = 'card-header-table',
                                        style={'backgroundColor': colors['dark-blue'], 'margin':'50px', 'border-radius': '0', 'box-shadow': '5px 2px 8px black', 'border-style':'solid', 'border-color':colors['light-blue'], 'border-width':'2px'},
                                        children=[ 
                                            html.Div(
                                                style={'margin-bottom':'30px',},
                                                children=[
                                                    dbc.RadioItems(
                                                        id='table-sort',
                                                        options=[{'label': 'Fr. o. m. 2019 (helår)', 'value': 'Fr. o. m. 2019'},
                                                                {'label': 'Fr. o. m. 2019 (månader)', 'value': 'Fr. o. m. 2019_months'},
                                                                {'label': 'Fr. o. m. 2019 (helår/månader)', 'value': 'month_structure'},
                                                                {'label': 'Kaptiel (helår)', 'value': 'Kapitel'},
                                                                {'label': 'Kaptiel (månader)', 'value': 'Kapitel_months'}],                                                                
                                                        value='Fr. o. m. 2019',
                                                        labelStyle={'display': 'inline-block'},
                                                        style = {'text-align': 'left','margin-left': '20px', 'margin-top': '10px', 'color':colors['light-blue']},
                                                        inline=True,
                                                    ),
                                                    dbc.Button('Run table', color="info", outline=False, id='show-table', className='btn-blue', n_clicks=0, style = {'text-align': 'left', 'margin-left': '40px', 'margin-top' : '20px'}),  
                                                ]
                                            ),
                                        ]

                                    ),
                                    
                                    dcc.Loading(children=[
                                    dash_table.DataTable(
                                        id='table',
                                        page_action='native',
                                        sort_action='native',
                                        filter_action="native",
                                        #filtering_settings='',
                                        #filtering=True,
                                        #editable=True,
                                        #row_deletable=True,
                                        #hidden_columns=[],
                                        fixed_rows={'headers': True},
                                        #fixed_columns={'headers': True, 'data': 1,},
                                        style_table={'overflowY': 'auto', 'overflowX': 'auto', 'paddinig' : '20px'}, #'height': '300px', 'width' : width, 
                                        #style_cell={
                                        #    'whiteSpace': 'normal',
                                        #    'height': 'auto',
                                        #},
                                        style_cell={'textAlign': 'left', 'width': '150px', 'minWidth': '180px', 'maxWidth': '180px', 'whiteSpace': 'normal', 'height': 'auto', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                                        style_header= {'textAlign': 'right'},
                                        css=[{'selector': '.row', 'rule': 'margin: 0'}],
                                        #columns=[{"name": i, "id": i, "deletable": True,} for i in df.columns],
                                        #data=df.to_dict('records'),
                                        )
                                    ], type='cube', fullscreen=False),
                                ]
                            ),
                            id="collapse-4",
                            style={'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},
                        ),
                    ]
                ),
                



                

                dbc.Card(
                    children=[
                        dbc.CardHeader(
                            html.H2(
                                children=[
                                    html.Img(src='/assets/SSF-assets/PNG/27.png', style={'width':'4%'}),
                                    dbc.Button(
                                        "Läs in rådata",
                                        color=colors['dark-blue'],
                                        className='dark-blue-text opacity-inverse',
                                        size='lg',
                                        id="group-3-toggle",
                                        #outline=True,
                                    ),

                                ]
                            ),
                            style={'backgroundColor': colors['light-blue']},
                        ),
                        dbc.Collapse(
                            dbc.CardBody(
                                children=[
                                    #dbc.Jumbotron(
                                    #id = 'jumbotron-header3',
                                    #style={'backgroundColor': colors['dark-blue'], 'margin':'50px', 'border-style':'solid', 'border-color':colors['light-blue'], 'border-width':'1px'},
                                    #children=[ 
                                        html.Div(
                                            style={'margin':'50px'},
                                            children= [
                                                dcc.Upload(
                                                    id='upload-data',
                                                    className='opacity-inverse hand',
                                                    style={
                                                        'width': '100%',
                                                        'height': '60px',
                                                        'lineHeight': '60px',
                                                        'borderWidth': '2px',
                                                        'borderStyle': 'dashed',
                                                        'borderRadius': '3px',
                                                        'textAlign': 'center',
                                                        'border-color': colors['blue'],
                                                        'color':colors['light-blue'],
                                                        #'box-shadow': '1px 2px 3px black'
                                                    },
                                                    children=[
                                                        dcc.Loading(
                                                            id='loading-upload',
                                                            type="default", #'cube', 'graph'
                                                            #fullscreen=True,
                                                            children=
                                                                html.Div(
                                                                    id='loading-output',
                                                                    style={},
                                                                    children=[
                                                                        'Drag and Drop or ', html.A('Select File', href='#', style={'color':colors['blue']})
                                                                    ]
                                                                ), 
                                                        )


                                                    ]
                                                ),
                                                
                                            ]
                                        ),
                                    #]
                                    #)
                                ]
                            ),
                            id="collapse-3",
                            style={'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},
                        ),
                    ]
                ),

                dbc.Card(
                    children=[
                        dbc.CardHeader(
                            html.H2(
                                children=[
                                    html.Img(src='/assets/SSF-assets/PNG/29.png', style={'width':'4%'}),
                                    dbc.Button(
                                        "READ ME",
                                        color=colors['dark-blue'],
                                        className='dark-blue-text opacity-inverse',
                                        size='lg',
                                        id="group-5-toggle",
                                        #outline=True,
                                    ),

                                ]
                            ),
                            style={'backgroundColor': colors['light-blue']},
                        ),
                        dbc.Collapse(
                            dbc.CardBody(
                                children=[
                                    
                                    dbc.Jumbotron(
                                        id = 'jumbotron-header5',
                                        style={'backgroundColor': colors['light-blue'], 'margin':'20px'},
                                        children=[ 
                                            html.Img(src='/assets/SSF-assets/PNG/fragor2.png', style={'width':'15%', 'margin-left':'1100px'}),
                                            html.Ul(
                                                children=[
                                                    html.Li('"Analysverktyget" används för att visualisera data hämtad från Brå (Bråttsförebyggande rådet). Användaren kan välja att skapa nya diagram eller ladda ett tidigare skapat dashboard. När användaren lägger till grafer har denna valet att titta på frekvens eller periodicitet. Frekvensen visualiseras genom fyra olika grafer där olika avgränsningar kan göras (år, kategorier). Det är alltså möjligt att kolla på datan efter olika kategorier och sub-kategorier (ex alla brott uppdelade i sub-brott). Datan är registrerad för antal per helår. Om användaren lägger till en graf för periodicitet kan denna se huruvida vissa kategorier (brott) är mer benägna att minska/öka under vissa månader. Alla grafer är möjliga att presentera med tre olika storlekar. Om användaren sedan vill spara ett skapat dashboard har denna möjligheten till detta. För att andra ska kunna ta del av detta måste personen dela den mapp som heter "dashboards" (eftersom servern ligger lokalt på användarens dator). Användaren har möjlighet att arbeta vidare på andras dashboards och spara dessa som nya filer. Slutligen har användaren möjligheten att ta bort den sist skapade grafen eller alla grafer senast skapade.'),
                                                    html.Li('"Läs in rådata" används för att hämta ny data till analysverktyget (ex om tidsperiod behöver uppdateras). Det är viktigt att datan hämtad (som excel-fil) ligger i mappen "Brå_Python" och inkluderar alla kategorier som tidigare data innefattat (om det inte är första gångeen data läses in). Hur datan kan hämtas följer i följande punkt. Eftersom Brå begränsar sina excel-filer till max 10.000 celler måste data (om omfattande) hämtas i omgångar (ex över olika tidsinteervaller eller regioner). Datan, som innefattar samma kategorier (!), läggs i samma excel-fil men under olika flikar (sheets). Vad dessa flikar döps till spelar ingen roll. Användaren drar datan till figuren (eller väljer genom att klicka på den) och får ett meddelande som säger om uppladdningen var lyckad eller ej (RISK ATT FOLK GÖR FEL???).'), 
                                                    html.Ul(html.Li('Hur data ska hämtas - Länk http://statistik.bra.se/solwebb/action/index Klicka:Månads- och kvartalsvis - Land och län 1975-2014, land och region 2015-')),
                                                    html.Li('"Tabell" visar datan som analysverktyget använder sig av. Det går att se frekvenser över helår och månader. Kolumner kan filtreras och sorteras efter önskan.'),
                                                    html.Li('Under "Sparande dashboards" är det möjligt att ladda tidigare sparade dashboards. Dessa laddas då upp under fliken "Analysverktyg".'),

                                                ],
                                                style={'padding':'5px'},

                                            )

                                        ]
                                    ),


                                ]
                            ),
                            id="collapse-5",
                            style={'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},
                        ),
                    ]
                ),
            ]
        ),
        #html.Img(src='/assets/SSF-assets/Bagen.png', style={'width':'20%', 'position':'absolute', 'bottom':'0','right':'0'}),
        #html.Div(children=get_kittens())
    ],
)



#NEW DROPDOWN OPTION
# dbc.Card(
#     children=[
#         dbc.CardHeader(
#             html.H2(
#                 dbc.Button(
#                     "Collapsible group 5",
#                     color="link",
#                     id="group-5-toggle",
#                 )
#             )
#         ),
#         dbc.Collapse(
#             dbc.CardBody(
#                 children=[




#                 ]
#             ),
#             id="collapse-5",
#         ),
#     ]
# ),



#IF YOU WANT A DAQ OBJECT TO BECOME DARK
# @app.callback(
#     Output('dark-theme-component-demo', 'children'),
#     [Input('daq-light-dark-theme', 'value')]
# )
# def turn_dark(dark_theme): 
#     if(dark_theme):
#         theme.update(
#             dark=True
#         )
#     else:
#         theme.update(
#             dark=False
#         )
#     return daq.DarkThemeProvider(theme=theme)







# @app.callback(
#     #[Output(f"collapse-{i}", 'style') for i in range(1, 6)]
#     [Output("collapse-1", 'style'), Output("collapse-2", 'style'), Output("collapse-3", 'style'), Output("collapse-4", 'style'), Output("collapse-5", 'style')
#     ],
#     [Input('daq-light-dark-theme', 'value')],
# )

# def change_bg(dark_theme):
#     if(dark_theme):
#         return {'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['dark-blue'], 'color': colors['dark-blue'], 'overflowY': 'scroll'}
#     else:
#         return {'backgroundColor': colors['light-blue'], 'color': colors['light-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['light-blue'], 'color': colors['light-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['light-blue'], 'color': colors['light-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['light-blue'], 'color': colors['light-blue'], 'overflowY': 'scroll'},{'backgroundColor': colors['light-blue'], 'color': colors['light-blue'], 'overflowY': 'scroll'}

    



@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, 6)], #increase if you add one more dropdown option
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, 6)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 6)],
    #prevent_initial_call=True
)
def toggle_accordion(n1, n2, n3, n4, n5, is_open1, is_open2, is_open3, is_open4, is_open5):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, False, False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False, False, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3, False, False
    elif button_id == "group-4-toggle" and n4:
        return False, False, False, not is_open4, False
    elif button_id == "group-5-toggle" and n5:
        return False, False, False, False, not is_open5
    return False, False, False, False, False






@app.callback(
    Output('loading-output', 'children'),
    [Input('upload-data', 'filename')],
    prevent_initial_call=True
)

def path_upload(file_name):
    if file_name == None:
        raise PreventUpdate
    try:
        read_file(file_name)
        return "Successfully uploaded"
    except:
        return "Filen är ej kompatibel"




@app.callback(
    [Output('save-output-right', 'is_open'), 
    Output('save-output-wrong', 'is_open'),
    Output('delete-output-right', 'is_open'),
    Output('delete-output-wrong', 'is_open'),
    Output('override', 'displayed'),
    Output('override-success', 'is_open'),
    Output('json-file-name', 'value'),
    Output('json-dpn', 'options')],
    [Input('save-confirmation', 'submit_n_clicks'),
    Input('delete-confirmation', 'submit_n_clicks'),
    Input('override', 'submit_n_clicks')],
    [State('json-file-name', 'value'),
    State('json-dpn', 'value'),
    State('container', 'children')],
    #prevent_initial_call=True 
)

# def save_or_delete_dashboard(n, pickle_name, div_children):
#     if n and pickle_name != None:
#         path = 'dashboards/' + str(pickle_name) + '.pkl'
#         try:
#             pickle.dump(div_children, open(path,"wb")) 
#             #hej = pickle.load(open("dashboards/div_children.pkl","rb")) when you run it
#         except FileExistsError:
#             return False, True, no_update
#         return True, False, [{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("dashboards/*")] #will include .pkl

#override
        
def save_or_delete_dashboard(n, delete_dashboard, submit_override, folder_name, folder_name_to_delete, div_children): #wish to override? with Alert
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] 
    if delete_dashboard and trigger_id == 'delete-confirmation':
        try: 
            shutil.rmtree(folder_name_to_delete)
            return False, False, True, False, False, False, "", [{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("dashboards/*")] 
        except:
            return False, False, False, True, False, False, "", [{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("dashboards/*")]    
    elif n and folder_name != "":
        path = 'dashboards/' + str(folder_name) + '/'
        try:
            os.mkdir(path) # Create target Directory
            print(os.mkdir(path))
            print('os.mkdir(path)')
        except FileExistsError:
            if submit_override and trigger_id == 'override': 
                for file in glob.glob(path+"*.json"):
                    os.remove(file)
                save_dashboard_inner_function(div_children, path, folder_name)
                return False, False, False, False, False, True, "", no_update
            else:
                return False, False, False, False, True, False, "", no_update
        save_dashboard_inner_function(div_children, path, folder_name)
        return True, False, False, False, False, False, "", [{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("dashboards/*")] #only folders... error if not! 
    elif n and folder_name == "":
        print('asdf')
        print(folder_name)
        print('asdf') 
        return False, True, False, False, False, False, "", no_update 
    elif n == 0: #on load
        return False, False, False, False, False, False, "", [{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("dashboards/*")]
    #elif delete-dashboard == 0:
    #    return False, False, [{'label': c.split('/')[1].split('.')[0], 'value': c} for c in glob.glob("dashboards/*")]
    

def save_dashboard_inner_function(div_children, path, folder_name):
    counter = 0 
    for element in div_children:
        with open(path + folder_name + '_graph_' + str(counter) + '.json', 'w') as json_file: #both path and folder_name?
            json.dump(element, json_file)
            #fig.write_image("html/fig1.jpeg")
            #fig.write_html("html/file.html")
        counter +=1

# @app.callback(
#     Output('override-success', 'is_open'),
#     [Input('override', 'submit_n_clicks')],
#     [State('json-file-name', 'value')],
#     prevent_initial_call=True 
#     )

# def override(submit_override, folder_name_to_override):
#     ctx = dash.callback_context
#     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] 
#     if submit_override and trigger_id == 'override': 
#         path = 'dashboards/' + str(folder_name_to_override) + '/'
#         shutil.rmtree(path)
#         return True
#     else:
#         return False



@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks'),
    Input('run-dashboards', 'n_clicks'),
    Input('remove-chart', 'n_clicks'),
    Input('delete-all-charts', 'n_clicks')], 
    [State('json-dpn', 'value'),
    State('graph-type', 'value'),
    State('container', 'children'),
    State('data-set', 'active_tab'),
    State('width', 'value')], #'width', 'value'
    prevent_initial_call=True #want an initial graph to be displayed? if changed, must change other things too
)



def display_graphs(n_clicks, n_dashboard, remove_chart, delete_all, folder_name, graph_type, div_children, dataset, width):
    if n_clicks != len(div_children): #quickfix; instead of callback below (when loading saved dashboards)
        n_clicks = len(div_children) 
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] 
    if n_dashboard and trigger_id == 'run-dashboards': #if dropdown value empty - error (unless persistence=True)
        div_children = [] 
        file_list = glob.glob(folder_name+"/*.json")
        file_list.sort()
        for json_file in file_list:
            with open(json_file, 'r') as read_json:
                div_children.append(json.load(read_json))
        return div_children
    elif delete_all and trigger_id == 'delete-all-charts': #HERE
        div_children = [] #MUST RESET n_clicks
        #n_clicks = 0
        return div_children
    elif trigger_id == 'remove-chart' and len(div_children) > 0: #add to callback below: n_clicks-1
        div_children = div_children[:-1]
        return div_children
    elif trigger_id == 'remove-chart' and len(div_children) == 0: #add to callback below: n_clicks-1
        return div_children
    elif dataset == 'Kapitel och paragrafer': #kapitel
        value_1 = 'Alla kapitel'
        value_2 = 'Ingen sub-kategori'
        dropdown_1 = ["Alla kapitel", "4 kap. Brott mot frihet och frid", "9 kap. Bedrägeri och annan oredlighet"] #SAMTLIGA ist för ALLA BROTT
        dropdown_2 = ['Ingen sub-kategori', 'Paragraf']
        if graph_type == 'Enskild region (inkl. hela landet)' or graph_type == 'Alla regioner':
            new_child = graph_regular(n_clicks,df4, width, dropdown_1, dropdown_2, value_1, value_2, dataset, graph_type)
            div_children.append(new_child)
        elif graph_type == 'Periodicitet':
            new_child = graph_periodicity(n_clicks,df5, width, dropdown_1, dropdown_2, value_1, value_2, dataset) #graph_type
            div_children.append(new_child)
 
    elif dataset == 'Brottskoder (fr. o. m. 2019)':
        value_1 = 'Brottskategori'
        value_2 = 'Ingen sub-kategori'
        dropdown_1 = ['Brottskategori','Brottstyp','Geografisk anknytning','Målgrupp']
        dropdown_2 = ['Ingen sub-kategori','Brottskategori','Brottstyp','Geografisk anknytning','Målgrupp']
        
        if graph_type == 'Enskild region (inkl. hela landet)' or graph_type == 'Alla regioner':
            new_child = graph_regular(n_clicks,df1, width, dropdown_1, dropdown_2, value_1, value_2, dataset, graph_type)
            div_children.append(new_child)

            #print('START')
            #print(div_children)
            #print('END')
            
        elif graph_type == 'Periodicitet':
            new_child = graph_periodicity(n_clicks,df2, width, dropdown_1, dropdown_2, value_1, value_2, dataset) #graph_type
            div_children.append(new_child)
    return div_children


# #Will run laso trigger callback above, causing len to not correspond to the len of div_children after a saved dashboard has been added
# @app.callback(
#     Output('add-chart','n_clicks'),
#     [Input('run-dashboards', 'n_clicks')],
#     [State('container', 'children')],
#     prevent_initial_call=True
# )

# def update_index(n_dashboard, div_children):
#     print(len(div_children))
#     if len(div_children) > 0:
#         #last_element = div_children[-1]
#         #n_dashboard = last_element['props']['children'][0]['props']['id']['index']
#         n_dashboard = len(div_children)
#     else:
#         n_dashboard = 0
#     return n_dashboard






#PROBLEM: if you filter one table and move to the next, no rows will appear in the new table (fiilter must be cleared first)
@app.callback(
    [Output('table', 'columns'),
    Output('table', 'data'),
    #Output("table", "filtering_settings"),
    ],
    [Input("show-table", "n_clicks")],
    [State('table-sort', 'value')],
    prevent_initial_call=True
)

def table_update(n_clicks, table_type):
    if n_clicks and table_type == "Fr. o. m. 2019":
        return [{"name": i, "id": i, "deletable": True} for i in df1.columns], df1.to_dict('records')#, ""
    elif n_clicks and table_type == "Fr. o. m. 2019_months":
        return [{"name": i, "id": i, "deletable": True} for i in df2.columns], df2.to_dict('records')
    elif n_clicks and table_type == "Kapitel":
        return [{"name": i, "id": i, "deletable": True} for i in df4.columns], df4.to_dict('records')#, ""
    elif n_clicks and table_type == "month_structure":
        return [{"name": i, "id": i, "deletable": True} for i in df3.columns], df3.to_dict('records')
    elif n_clicks and table_type == "Kapitel_months":
        return [{"name": i, "id": i, "deletable": True} for i in df5.columns], df5.to_dict('records')
    else:
        raise PreventUpdate


@app.callback(
    Output({'type': 'dynamic-dpn-col', 'index': MATCH}, 'value'),
    [Input({'type': 'dynamic-dpn-x', 'index': MATCH}, 'value')],
    [State({'type': 'dynamic-dpn-col', 'index': MATCH}, 'value')]
    )

def update_dropdown(x_value, col_value):
    if x_value == col_value:
        return "Ingen sub-kategori" 
    else:
        return col_value


@app.callback(
    [Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
     Output({'type': 'dynamic-dpn-reg', 'index': MATCH}, 'options'),
     Output({'type': 'dynamic-dpn-x', 'index': MATCH}, 'options'),
     Output({'type': 'dynamic-dpn-col', 'index': MATCH}, 'options'),
     Output({'type': 'title-1', 'index': MATCH}, 'children'), 
     Output({'type': 'title-2', 'index': MATCH}, 'children'),
     Output({'type': 'dynamic-dpn-s', 'index': MATCH}, 'disabled'),
     Output({'type': 'dynamic-dpn-reg', 'index': MATCH}, 'disabled'),
     Output({'type': 'dynamic-dpn-x', 'index': MATCH}, 'disabled'),
     Output({'type': 'dynamic-dpn-col', 'index': MATCH}, 'disabled')],
    
    [Input(component_id={'type': 'dynamic-dpn-s', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-reg', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-x', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-col', 'index': MATCH}, component_property='value'),  
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value'),
     dash.dependencies.Input('my-daq-booleanswitch', 'value')],

     [State({'type': 'graph-type-individual', 'index': MATCH}, 'children'),
     State({'type': 'graph-data-set', 'index': MATCH}, 'children'),],
     prevent_initial_call=True
    )


def update_graph(s_value, reg_value, x_value, col_value, chart_choice, on, graph_type, dataset):
    #disable dropdowns
    x_dpn_boolean = False
    col_dpn_boolean = False
    if graph_type == "Alla regioner":
        region_boolean = True
    else:
        region_boolean = False

    if dataset == "Brottskoder (fr. o. m. 2019)":
        df = df1
    elif dataset == "Kapitel och paragrafer":
        df = df4

    fig, reg_list, x_list, col_list, string1, string2, slider_boolean, col_dpn_boolean = regular_graph(df, s_value, reg_value, x_value, col_value, chart_choice, dataset, graph_type, on)
    return fig, [{'label': c, 'value': c} for c in reg_list], [{'label': c, 'value': c} for c in x_list], [{'label': c, 'value': c} for c in col_list], string1, string2, slider_boolean, region_boolean, x_dpn_boolean, col_dpn_boolean
    
    

@app.callback(
    Output({'type': 'dynamic-dpn-col_periodicity', 'index': MATCH}, 'value'),
    [Input({'type': 'dynamic-dpn-x_periodicity', 'index': MATCH}, 'value')],
    [State({'type': 'dynamic-dpn-col_periodicity', 'index': MATCH}, 'value')]
    )

def update_dropdown(x_value, col_value):
    if x_value == col_value:
        return "Ingen sub-kategori"
    else:
        return col_value


@app.callback(
    [Output({'type': 'dynamic-graph_periodicity', 'index': MATCH}, 'figure'),
     Output({'type': 'dynamic-dpn-reg_periodicity', 'index': MATCH}, 'options'),
     Output({'type': 'dynamic-dpn-x_periodicity', 'index': MATCH}, 'options'), #to not match
     Output({'type': 'dynamic-dpn-col_periodicity', 'index': MATCH}, 'options'),
     #Output({'type': 'title-1', 'index': MATCH}, 'children'),
     #Output({'type': 'title-2', 'index': MATCH}, 'children'),
     #Output({'type': 'dynamic-dpn-rs_periodicity', 'index': MATCH}, 'disabled'),
     ],
    [Input(component_id={'type': 'dynamic-dpn-rs_periodicity', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-reg_periodicity', 'index': MATCH}, component_property='value'),
     
     Input(component_id={'type': 'dynamic-dpn-x_periodicity', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-col_periodicity', 'index': MATCH}, component_property='value'),
     dash.dependencies.Input('my-daq-booleanswitch', 'value')],

     #Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')], #only need line 
     [#State({'type': 'graph-type-individual_periodicity', 'index': MATCH}, 'children'), #only periodicity needed 
     State({'type': 'graph-data-set_periodicity', 'index': MATCH}, 'children')],
     prevent_initial_call=True

)


def update_graph2(rs_value, reg_value, x_value, col_value, on, dataset):
    if dataset == "Brottskoder (fr. o. m. 2019)":
        df = df2
    elif dataset == "Kapitel och paragrafer":
        df = df5 

    fig, reg_list, x_list, col_list = periodicity_graph(df, rs_value, reg_value, x_value, col_value, dataset, on)
    return fig, [{'label': c, 'value': c} for c in reg_list], [{'label': c, 'value': c} for c in x_list], [{'label': c, 'value': c} for c in col_list]



#PRINT TO PDF
#import pdfkit
#pdfkit.from_string('Shaurya GFG','GfG.pdf')

#import weasyprint
#import pdfgen

#from weasyprint import HTML
#HTML('http://weasyprint.org/').write_pdf('/tmp/weasyprint-website.pdf')


if __name__ == '__main__':
    app.run_server(debug=True) #, port=8051
    #app.server.run(port=8000, host='127.0.0.1')
    #app.server(host='0.0.0.0', port=8080, debug=True)
    #app.run_server(debug = True,host = ‘0.0.0.0’).

#Dash requires applications to be served from a Python server (so that the callbacks can be fired).

#WSGI server


