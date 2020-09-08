import pandas as pd
#import modin.pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
import plotly.express as px
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State, MATCH, ALL, ALLSMALLER
from dash import no_update
import dash_bootstrap_components as dbc
from graph_layouts import *

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


def regular_graph(df, s_value, reg_value, x_value, col_value, chart_choice, dataset, graph_type, on): 
    if on == False:
        templates = 'plotly_white' #overries preset template - not the best solution
    elif on == True:
        templates = 'plotly_dark'
    
    reg_list = [r for r in np.sort(df['Region'].unique())] 
    if graph_type != "Alla regioner":
        dff = df[df['Region'].isin([reg_value])] 
    elif graph_type == "Alla regioner":
        dff = df[~df['Region'].isin(['Hela landet'])] #exclude 'Hela landet'
    
    if dataset == 'Kapitel och paragrafer' and x_value != 'Alla kapitel':
        dff = dff[dff['Kapitel'].isin([x_value])] #filter by chapter

    ctg_value = categories(x_value, col_value, graph_type, dataset)
    ctg_value = list(dict.fromkeys(ctg_value)) #unnessesary since callback prevents dropdown values from being the same

    if chart_choice == 'bar':
        dff = dff[dff['År'].isin([s_value])] #Cant have this under line chart since we want all years
        dff = dff.groupby(ctg_value)[['Antal']].sum()
        dff = add_columns(dff,ctg_value)
        main_title = 'KATEGORI' 
        if dataset == "Brottskoder (fr. o. m. 2019)":
            if graph_type == 'Enskild region (inkl. hela landet)':   
                if col_value == "Ingen sub-kategori":
                    fig = px.bar(dff, x=dff.loc[:,x_value], y=dff.Antal, text=dff.Antal, barmode="stack", template=templates)#, facet_col="REGION", ,animation_frame=dff.loc[:,"År"], animation_group=
                else:
                    fig = px.bar(dff, x=dff.loc[:,x_value], y=dff.Antal, color=dff.loc[:,col_value], hover_name=dff.loc[:,col_value], text=dff.Antal, barmode="stack", template=templates)#ctg_index refers to last column
            elif graph_type == 'Alla regioner':
                if col_value == "Ingen sub-kategori":
                    fig = px.bar(dff, x=dff.loc[:,"Region"], y=dff.Antal, color=dff.loc[:,x_value], hover_name=dff.loc[:,x_value], text=dff.Antal, barmode="stack", template=templates)
                else:
                    fig = px.bar(dff, x=dff.loc[:,"Region"], y=dff.Antal, color=dff.loc[:,x_value], hover_name=dff.loc[:,col_value], text=dff.Antal, barmode="stack", template=templates)
        elif dataset == "Kapitel och paragrafer":
            if graph_type == 'Enskild region (inkl. hela landet)':
                if col_value == "Ingen sub-kategori":
                    fig = px.bar(dff, x=dff.Kapitel, y=dff.Antal, color=dff.Kapitel, text=dff.Antal, barmode="stack", template=templates, color_continuous_scale='Cividis_r')
                elif col_value == "Paragraf":
                    fig = px.bar(dff, x=dff.Kapitel, y=dff.Antal, color=dff.loc[:,col_value], hover_name=dff.loc[:,col_value], text=dff.Antal, barmode="stack", template=templates)
            elif graph_type == 'Alla regioner': #same as above!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if col_value == "Ingen sub-kategori":
                    fig = px.bar(dff, x=dff.loc[:,"Region"], y=dff.Antal, color=dff.Kapitel, text=dff.Antal, barmode="stack", template=templates)
                elif col_value == 'Paragraf':
                    fig = px.bar(dff, x=dff.loc[:,"Region"], y=dff.Antal, color=dff.loc[:,col_value], hover_name=dff.loc[:,col_value], text=dff.Antal, barmode="stack", template=templates) #tror denna ej kan ha x_value
            main_title = 'KAPITEL'

        fig.update_layout(clickmode='event+select')
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        fig.update_layout(legend=dict(
               orientation="h",
               yanchor="bottom",
               y=1.02,
               xanchor="right",
               x=1,
               ))
        #fig.data[0].marker.line.width = 1
        #fig.data[0].marker.line.color = colors['light-blue']
        #fig.data[1].marker.line.width = 1
        #fig.data[1].marker.line.color = colors['light-blue']
        #fig.write_image("plots/fig1.pdf")
        #fig.write_html("plots/file.html")
        reg_list, x_list, col_list = dynamic_dropdown(reg_list, chart_choice,x_value,col_value, dataset, graph_type)
        return fig, reg_list, x_list, col_list, main_title, "SUB-KATEGORI", False, False

    elif chart_choice == 'line':    
        dff = dff.groupby(ctg_value)[['Antal']].sum() 
        dff = add_columns(dff,ctg_value)
        dff = dff.astype({'År': 'int'})
        #option: make slider act as RangeSlider
        #year_span = [year for year in df['År'].unique() if year >= s_value]
        #dff = dff[dff['År'].isin(year_span)]
        main_title = 'KATEGORI' 

        if dataset == "Brottskoder (fr. o. m. 2019)":
            if graph_type == 'Enskild region (inkl. hela landet)':
                if col_value == "Ingen sub-kategori":
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, line_group=dff.loc[:,x_value], color=dff.loc[:,x_value], hover_name=dff.loc[:,x_value], text=dff.Antal, template=templates)
                else:
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, line_group=dff.loc[:,x_value], color=dff.loc[:,col_value], hover_name=dff.loc[:,x_value], text=dff.Antal, template=templates) #https://plotly.com/python-api-reference/generated/plotly.express.line.html
            elif graph_type == 'Alla regioner':
                if col_value == "Ingen sub-kategori":
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, line_group=dff.loc[:,x_value], color=dff.loc[:,"Region"], hover_name=dff.loc[:,x_value], text=dff.Antal, template=templates)
                else:
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, line_group=dff.loc[:,x_value], color=dff.loc[:,"Region"], hover_name=dff.loc[:,col_value], text=dff.Antal, template=templates)
        elif dataset == "Kapitel och paragrafer":
            if graph_type == 'Enskild region (inkl. hela landet)':
                if col_value == "Ingen sub-kategori": #change
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, color=dff.Kapitel, text=dff.Antal, template=templates)
                elif col_value == "Paragraf":
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, color=dff.loc[:,col_value], hover_name=dff.loc[:,col_value], text=dff.Antal, template=templates) #line_group=dff.loc[:,x_value],
            elif graph_type == 'Alla regioner': #CHECK THISSSSSSS VALIDATE
                if col_value == "Ingen sub-kategori":
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, line_group=dff.Kapitel, color=dff.loc[:,"Region"], hover_name=dff.Kapitel, text=dff.Antal, template=templates)
                elif col_value == "Paragraf":
                    fig = px.line(dff, x=dff.loc[:,"År"], y=dff.Antal, line_group=dff.loc[:,col_value], color=dff.loc[:,"Region"], hover_name=dff.loc[:,col_value], text=dff.Antal, template=templates)
            main_title = 'KAPITEL' 
        #fig.update_traces(mode="markers+lines") 
        fig.update_layout(clickmode='event+select')
        fig.update_layout(xaxis=dict(tickvals=df['År'].unique())) 
        fig.update_layout(legend=dict(
               orientation="h",
               yanchor="bottom",
               y=1.02,
               xanchor="right",
               x=1
               ))

        slider_boolean = True #False if slider --> RangeSlider
        reg_list, x_list, col_list = dynamic_dropdown(reg_list, chart_choice, x_value,col_value, dataset, graph_type)
        return fig, reg_list, x_list, col_list, main_title, "SUB-KATEGORI", slider_boolean, False

    elif chart_choice == 'pie':
        dff = dff[dff['År'].isin([s_value])] #Cant have this under line chart since we want all years
        dff = dff.groupby(ctg_value)[['Antal']].sum() #, as_index=False
        dff = add_columns(dff,ctg_value)
        col_dpn_boolean = False
        main_title = 'KATEGORI' 

        if dataset == "Brottskoder (fr. o. m. 2019)":
            if graph_type == 'Enskild region (inkl. hela landet)':
                fig = px.pie(dff, names=dff.loc[:,x_value], values=dff.Antal)
                col_dpn_boolean = True
            elif graph_type == 'Alla regioner':
                fig = px.pie(dff, names=dff.loc[:,x_value], values=dff.Antal)
                col_dpn_boolean = True 

        elif dataset == "Kapitel och paragrafer":
            if graph_type == 'Enskild region (inkl. hela landet)':
                if col_value == "Ingen sub-kategori": #strange
                    fig = px.pie(dff, names=dff.Kapitel, values=dff.Antal)
                else:
                    fig = px.pie(dff, names=dff.loc[:,col_value], values=dff.Antal)
            elif graph_type == 'Alla regioner':
                fig = px.pie(dff, names=dff.loc[:,"Region"], values=dff.Antal)
                col_dpn_boolean = True
            main_title = 'KAPITEL' 

        fig.update_traces(textposition='auto', texttemplate = "%{percent}") #, textinfo='percent+label', texttemplate = "%{label}: %{value} <br>%{percent}") #, textinfo='percent+label'
        fig.update_layout(legend=dict(
               orientation="h",
               yanchor="bottom",
               y=1.02,
               xanchor="right",
               x=1
               ))
        if on == True:
            fig.update_layout(
            plot_bgcolor=colors['dark-blue'],
            paper_bgcolor=colors['dark-blue'],
            font_color=colors['light-blue']
            )
        elif on == False:
            fig.update_layout(
            plot_bgcolor=colors['light-blue'],
            paper_bgcolor=colors['light-blue'],
            #font_color=colors['light-blue']
            )

        reg_list, x_list, col_list = dynamic_dropdown(reg_list, chart_choice, x_value,col_value, dataset, graph_type)

        if dataset == "Brottskoder (fr. o. m. 2019)":
            return fig, reg_list, x_list, col_list, main_title, "SUB-KATEGORI", False, col_dpn_boolean
        elif dataset == "Kapitel och paragrafer":
            return fig, reg_list, x_list, col_list, main_title, "SUB-KATEGORI", False, col_dpn_boolean

    elif chart_choice == 'sunburst':
        dff = dff[dff['År'].isin([s_value])] 
        dff = dff.groupby(ctg_value)[['Antal']].sum() 
        dff = add_columns(dff,ctg_value)
        main_title = 'KATEGORI' 

        if dataset == "Brottskoder (fr. o. m. 2019)":
            if graph_type == 'Enskild region (inkl. hela landet)':
                if col_value == "Ingen sub-kategori":
                    fig = px.sunburst(dff, path=[x_value], values=dff.Antal, hover_name=dff.loc[:,x_value], branchvalues="total") #treemap #"The column label 'BROTTSKATEGORI' is not unique." if bot x and col is BROTTSKATEGORI
                else:
                    fig = px.sunburst(dff, path=[x_value, col_value], values=dff.Antal, hover_name=dff.loc[:,x_value], branchvalues="total") #"The column label 'BROTTSKATEGORI' is not unique." if bot x and col is BROTTSKATEGORI
            elif graph_type == 'Alla regioner':
                if col_value == "Ingen sub-kategori":
                    fig = px.sunburst(dff, path=["Region", x_value], values=dff.Antal, hover_name=dff.loc[:,x_value], branchvalues="total")
                else:
                    fig = px.sunburst(dff, path=["Region", x_value, col_value], values=dff.Antal, hover_name=dff.loc[:,x_value], branchvalues="total")
        elif dataset == "Kapitel och paragrafer":
            if graph_type == 'Enskild region (inkl. hela landet)':
                if col_value == "Ingen sub-kategori":
                    fig = px.sunburst(dff, path=["Kapitel"], values=dff.Antal, hover_name=dff.Kapitel, branchvalues="total")
                elif col_value == "Paragraf":
                    fig = px.sunburst(dff, path=["Kapitel", col_value], values=dff.Antal, hover_name=dff.loc[:,col_value], branchvalues="total") #added x_value
            elif graph_type == 'Alla regioner':
                if col_value == "Ingen sub-kategori":
                    fig = px.sunburst(dff, path=["Region","Kapitel"], values=dff.Antal, hover_name=dff.Kapitel, branchvalues="total")
                elif col_value == 'Paragraf':
                    fig = px.sunburst(dff, path=["Region", "Kapitel", col_value], values=dff.Antal, hover_name=dff.loc[:,col_value], branchvalues="total")
            main_title = 'KAPITEL' 
                

        fig.update_traces(textinfo='label+value+percent parent')#texttemplate = "%{label}: %{value} %{percent}")
        fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
        fig.update_layout(legend=dict(
               orientation="h",
               yanchor="bottom",
               y=1.02,
               xanchor="right",
               x=1
               ))
        if on == True:
            fig.update_layout(
            plot_bgcolor=colors['dark-blue'],
            paper_bgcolor=colors['dark-blue'],
            font_color=colors['light-blue']
            )
        elif on == False:
            fig.update_layout(
            plot_bgcolor=colors['light-blue'],
            paper_bgcolor=colors['light-blue'],
            #font_color=colors['light-blue']
            )

        reg_list, x_list, col_list = dynamic_dropdown(reg_list, chart_choice, x_value, col_value, dataset, graph_type)
        return fig, reg_list, x_list, col_list, main_title, "SUB-KATEGORI", False, False

def periodicity_graph(df, rs_value, reg_value, x_value, col_value, dataset, on): #månadsutveckling
    
    if on == False:
        templates = "plotly_white"
    elif on == True:
        templates = "plotly_dark"

    reg_list = [r for r in np.sort(df['Region'].unique())] 
    dff = df[df['Region'].isin([reg_value])]
    if rs_value[0] == dff['År'].min():
        dff = dff[dff['År'].isin(range(rs_value[0],rs_value[1]+1))] #rs_value[1]+1 because ends on last argument
    else:
        dff = dff[dff['År'].isin(range(rs_value[0]-1,rs_value[1]+1))] #rs_value[0]-1 since we want value from december in the year before rs_value[0]
        indexNames = dff[ (dff['År'] == rs_value[0]-1) & (dff['Tidsperiod'] < 12) ].index
        dff.drop(indexNames, inplace=True)

    
    if dataset == 'Brottskoder (fr. o. m. 2019)':
        if col_value == "Ingen sub-kategori":
            ctg_value = ['Region']+[x_value]+['År','Tidsperiod']
            dff = dff.groupby(ctg_value).Antal.sum(min_count=1).unstack(level=1)             
            dff_diff = dff.diff().unstack(level=-2).stack(level=0, dropna=False).abs()
            dff = dff.pct_change(fill_method=None).add(1).unstack(level=-2).stack(level=0, dropna=False)#unstack(level=1) År, stack x_val (bad name)
            dff['WEIGHTED_AVG'] = dff.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1) #absolutbelopp???
            #dff['MEDEL'] = dff.mean(axis=1)
            dff['STDAV'] = dff.std(axis=1)
            ctg_value = ['Region', 'Tidsperiod']+[x_value] 
            dff = add_columns(dff,ctg_value)
            fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, symbol=dff.loc[:,x_value], template=templates, color_continuous_scale=px.colors.sequential.Viridis_r) #line_group=dff.loc[:,x_value], color=dff.loc[:,col_value], hover_name=dff.loc[:,x_value
        else:
            ctg_value = ['Region']+[x_value, col_value]+['År','Tidsperiod']
            dff = dff.groupby(ctg_value).Antal.sum(min_count=1).unstack(level=[1,2])
            dff_diff = dff.diff().unstack(level=-2).stack(level=[0,1], dropna=False).abs()
            dff = dff.pct_change(fill_method=None).add(1).unstack(level=-2).stack(level=[0,1], dropna=False)#unstack(level=1) År, stack x_val (bad name)
            #dff['MEDEL'] = dff.mean(axis=1)
            dff['WEIGHTED_AVG'] = dff.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1) #absolutbelopp???
            dff['STDAV'] = dff.std(axis=1)
            ctg_value = ['Region', 'Tidsperiod']+[x_value, col_value] 
            dff = add_columns(dff,ctg_value)
            fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, symbol=dff.loc[:,x_value], hover_name=dff.loc[:,col_value], template=templates, color_continuous_scale=px.colors.sequential.Viridis_r)
            

    elif dataset == 'Kapitel och paragrafer':
        if x_value != 'Alla kapitel':
            dff = dff[dff['Kapitel'].isin([x_value])]
        if col_value == "Ingen sub-kategori":
            ctg_value = ['Region', 'Kapitel', 'År', 'Tidsperiod']
            dff = dff.groupby(ctg_value).Antal.sum(min_count=1).unstack(level=1)             
            dff_diff = dff.diff().unstack(level=-2).stack(level=0, dropna=False).abs()
            dff = dff.pct_change(fill_method=None).add(1).unstack(level=-2).stack(level=0, dropna=False)#unstack(level=1) År, stack x_val (bad name)
            dff['WEIGHTED_AVG'] = dff.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1) #absolutbelopp???
            #dff['MEDEL'] = dff.mean(axis=1)
            dff['STDAV'] = dff.std(axis=1)
            ctg_value = ['Region', 'Tidsperiod']+['Kapitel'] 
            dff = add_columns(dff,ctg_value)
            fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, symbol=dff.Kapitel, template=templates, color_continuous_scale=px.colors.sequential.Viridis_r) #, color_continuous_scale=["yellow", "green", "red", 'pink'], line_group=dff.loc[:,x_value], color=dff.loc[:,col_value], hover_name=dff.loc[:,x_value] , marginal_y="box"
        else:
            ctg_value = ['Region']+['Kapitel', col_value]+['År','Tidsperiod']
            dff = dff.groupby(ctg_value).Antal.sum(min_count=1).unstack(level=[1,2])
            dff_diff = dff.diff().unstack(level=-2).stack(level=[0,1], dropna=False).abs()
            dff = dff.pct_change(fill_method=None).add(1).unstack(level=-2).stack(level=[0,1], dropna=False)#unstack(level=1) År, stack x_val (bad name)
            #dff['MEDEL'] = dff.mean(axis=1)
            dff['WEIGHTED_AVG'] = dff.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1) #absolutbelopp???
            dff['STDAV'] = dff.std(axis=1)
            ctg_value = ['Region', 'Tidsperiod']+['Kapitel', col_value] 
            dff = add_columns(dff,ctg_value)
            fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, symbol=dff.loc[:,col_value], hover_name=dff.loc[:,col_value], template=templates, color_continuous_scale=px.colors.sequential.Viridis_r)
            #if x_value != 'ALLA KAPITEL':
            #    fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, symbol=dff.loc[:,col_value], hover_name=dff.loc[:,col_value], template=templates, color_continuous_scale=px.colors.sequential.Viridis_r)
            #elif x_value == 'ALLA KAPITEL':
            #    fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, symbol=dff.KAPITEL, hover_name=dff.loc[:,col_value], template=templates, color_continuous_scale=px.colors.sequential.Viridis_r)
            
            

    


        

    #if x_value == "ALLA BROTT" or x_value == "ALLA KAPITEL": #if dataframe == 'kapitel'
        # ctg_value = ['REGION', 'År', 'Tidsperiod']
        # dff = dff.groupby(ctg_value).Antal.sum(min_count=1)#.unstack(level=1)
        # dff_diff = dff.diff().unstack(level=1)
        # dff = dff.pct_change(fill_method=None).add(1).unstack(level=1)#unstack(level=1) År, stack x_val (bad name)
        # dff['WEIGHTED_AVG'] = dff.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1) #absolutbelopp???
        # dff['MEDEL'] = dff.mean(axis=1)
        # dff['STDAV'] = dff.std(axis=1)
        # ctg_value.remove('År')
        # dff = add_columns(dff,ctg_value)
        # fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, template=templates) #line_group=dff.loc[:,x_value], color=dff.loc[:,col_value], hover_name=dff.loc[:,x_value] , marginal_y="box"
        # fig.update_layout(xaxis=dict(tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
        # ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'])) 
        # fig.update_traces(mode="markers+lines")
        # fig.update_layout(legend=dict(
        #        orientation="h",
        #        yanchor="bottom",
        #        y=1.02,
        #        xanchor="right",
        #        x=1
        #        ))
        # fig.add_shape( # adds a horizontal "target" line
        # type="line", line_color="grey", line_width=2, opacity=1, line_dash="dot", #line_color='salmon'
        # x0=0, x1=1, xref="paper", y0=1, y1=1, yref="y")
    #elif x_value != "ALLA BROTT" and col_value == "INGEN SUB-KATEGORI" or x_value != "ALLA KAPITEL" and col_value == "INGEN SUB-KATEGORI":
    



    # elif x_value != "ALLA KAPITEL" and col_value == "INGEN SUB-KATEGORI":
    #     ctg_value = ['REGION']+[x_value]+['År','Tidsperiod']
    #     dff = dff.groupby(ctg_value).Antal.sum(min_count=1).unstack(level=1) 
    #     #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     #    print(dff)
        
    #     dff_diff = dff.diff().unstack(level=-2).stack(level=0, dropna=False)
    #     dff = dff.pct_change(fill_method=None).add(1).unstack(level=-2).stack(level=0, dropna=False)#unstack(level=1) År, stack x_val (bad name)
    #     dff['WEIGHTED_AVG'] = dff.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1) #absolutbelopp???
        
    #     #dff['MEDEL'] = dff.mean(axis=1)
    #     dff['STDAV'] = dff.std(axis=1)
    #     ctg_value = ['REGION', 'Tidsperiod']+[x_value] 
    #     dff = add_columns(dff,ctg_value)
    #     fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, template=templates) #line_group=dff.loc[:,x_value], color=dff.loc[:,col_value], hover_name=dff.loc[:,x_value]
    #     fig.update_layout(xaxis=dict(tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
    #     ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'])) 
    #     #fig.update_xaxes(rangeslider_visible=True)
    #     fig.update_traces(mode="markers+lines")
    #     #fig.update_layout(hovermode="x")
    #     fig.update_layout(legend=dict(
    #            orientation="h",
    #            yanchor="bottom",
    #            y=1.02,
    #            xanchor="right",
    #            x=1
    #            ))
    #     fig.add_shape( # add a horizontal "target" line
    #     type="line", line_color="grey", line_width=2, opacity=1, line_dash="dot",
    #     x0=0, x1=1, xref="paper", y0=1, y1=1, yref="y")
    # else: 
    #     #IS THIS UNESSESARY?
    #     #VISAS MED FÖRSTA DROPDOWNEN
    #     ctg_value = ['REGION']+[x_value, col_value]+['År','Tidsperiod']
    #     dff = dff.groupby(ctg_value).Antal.sum(min_count=1).unstack(level=[1,2])
    #     #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     #    print(dff)
    #     #print(dff.diff().unstack(level=-2).stack(level=[0,1]))
    #     #print(dff.pct_change(fill_method=None).add(1).unstack(level=-2).stack(level=[0,1]))
    #     dff_diff = dff.diff().unstack(level=-2).stack(level=[0,1], dropna=False)
    #     dff = dff.pct_change(fill_method=None).add(1).unstack(level=-2).stack(level=[0,1], dropna=False)#unstack(level=1) År, stack x_val (bad name)
    #     #aa = dff_pct.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1)
    #     #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     #    print(dff_diff)
    #     #    print(dff)
    #     #dff['MEDEL'] = dff.mean(axis=1)
    #     dff['WEIGHTED_AVG'] = dff.mul(dff_diff, axis=1).sum(min_count=1, axis=1)/dff_diff.sum(min_count=1, axis=1) #absolutbelopp???
    #     dff['STDAV'] = dff.std(axis=1)
    #     ctg_value = ['REGION', 'Tidsperiod']+[x_value, col_value] 
    #     dff = add_columns(dff,ctg_value)
    #     #if dataset == "fr. o. m. 2019":
    #     #    fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=[dff.WEIGHTED_AVG,dff.STDAV], color=dff.loc[:,x_value], hover_name=dff.loc[:,col_value], template=templates)
    #     #elif dataset == "kapitel": 
    #     #    fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=[dff.WEIGHTED_AVG,dff.STDAV], color=dff.loc[:,col_value], hover_name=dff.loc[:,x_value], template=templates) #line_group=dff.loc[:,x_value], color=dff.loc[:,col_value], hover_name=dff.loc[:,x_value]
    #     fig = px.scatter(dff, x=dff.loc[:,"Tidsperiod"], y=dff.WEIGHTED_AVG, color=dff.STDAV, hover_name=dff.loc[:,col_value], template=templates)
    #     fig.update_layout(xaxis=dict(tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
    #     ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'])) 
    #     #fig.update_xaxes(rangeslider_visible=True)
    #     fig.update_traces(mode="markers+lines")
    #     #fig.update_layout(hovermode="x")
    #     fig.update_layout(legend=dict(
    #            orientation="h",
    #            yanchor="bottom",
    #            y=1.02,
    #            xanchor="right",
    #            x=1
    #            ))
    #     fig.add_shape( # add a horizontal "target" line
    #     type="line", line_color="grey", line_width=2, opacity=1, line_dash="dot",
    #     x0=0, x1=1, xref="paper", y0=1, y1=1, yref="y")
    fig.update_traces(mode="markers") #+lines
    fig.update_layout(xaxis=dict(tickvals = [1,2,3,4,5,6,7,8,9,10,11,12], ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'])) 
    fig.update_layout(
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=0.6 #1
    ))
    fig.add_shape( # add a horizontal "target" line
    type="line", line_color=colors['blue'], line_width=2, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=1, y1=1, yref="y")
    fig.update_layout(clickmode='event+select')
    reg_list, x_list, col_list = dynamic_dropdown(reg_list, 'periodicity', x_value,col_value, dataset, None)
    return fig, reg_list, x_list, col_list #disable

def categories(x_value, col_value, graph_type, dataset): #kan kortas ner
    if graph_type == 'Enskild region (inkl. hela landet)':
        if dataset == "Brottskoder (fr. o. m. 2019)":
            if col_value == "Ingen sub-kategori":
                ctg_value = ['År','Region']+[x_value]
            #elif x_value == col_value:
            #    ctg_value = ['År','Region']+[x_value]
            #    col_value == "INGEN SUB-KATEGORI" 
            else:
                ctg_value = ['År','Region']+[x_value, col_value] #STRANGE IF x_value and col_value same
        elif dataset == "Kapitel och paragrafer":
            #if x_value == "ALLA KAPITEL":
            #    ctg_value = ['År','REGION']+['KAPITEL'] #hmmm same, shorten
            if col_value == "Ingen sub-kategori":
                ctg_value = ['År','Region']+['Kapitel'] #x_value
            elif col_value == "Paragraf": #or else
                ctg_value = ['År','Region']+['Kapitel', col_value] #x_value
    elif graph_type == 'Alla regioner':
        if dataset == "Brottskoder (fr. o. m. 2019)":
            if col_value == "Ingen sub-kategori":
                ctg_value = ['År','Region']+[x_value]
            else:
                ctg_value = ['År','Region']+[x_value, col_value]
        elif dataset == "Kapitel och paragrafer":
            #if x_value == "ALLA KAPITEL":
            #    ctg_value = ['År','REGION']
            if col_value == "Ingen sub-kategori": #same word... bad
                ctg_value = ['År','Region']+['Kapitel'] #x_value
            elif col_value == "Paragraf":
                ctg_value = ['År','Region']+['Kapitel', col_value] #x_value
    return ctg_value


def add_columns(dff,ctg_value):
    ctgs = [] #do function

    for ctg_index in range(len(ctg_value)): #reg brott tid
        ctgs.append([])
        for i in dff.index:
            ctgs[ctg_index].append(i[ctg_index])
        dff[ctg_value[ctg_index]] = ctgs[ctg_index]
    return dff

def dynamic_dropdown(reg_list, chart_choice, x_value,col_value, dataset, graph_type): #ta in graph_type?? ingen kat kommer för regular graph fast ändras inte om man trycker
    if dataset == "Kapitel och paragrafer":
        x_categories = ["Alla kapitel", "4 kap. Brott mot frihet och frid", "9 kap. Bedrägeri och annan oredlighet"]
        col_categories = ['Ingen sub-kategori', 'Paragraf']
    elif dataset == 'Brottskoder (fr. o. m. 2019)':
        x_categories = ['Brottskategori','Brottstyp','Geografisk anknytning','Målgrupp'] #lägg till ingenn kategori till regular graph?
        col_categories = ['Ingen sub-kategori', 'Brottskategori','Brottstyp','Geografisk anknytning','Målgrupp']
    if graph_type == 'Alla regioner':
        reg_list = []
    #IF DATASET == Alla regioner, THEN CANT HAVE COL_VALUES (SO MUST DIVIDE MORE IF-STATEMENTS)
    if chart_choice == 'pie' and graph_type != 'Enskild region (inkl. hela landet)' and dataset == 'Kapitel och paragrafer' or chart_choice == 'pie' and dataset == 'Brottskoder (fr. o. m. 2019)': 
        col_list = []
    else:
        col_list = [n for n in col_categories if n != x_value]
    return reg_list, x_categories, col_list