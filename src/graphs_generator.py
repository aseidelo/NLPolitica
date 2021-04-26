'''
Open-source libraries that are necessary for the application to function
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import bokeh
import re
import os
from matplotlib.colors import *
import matplotlib.image as mpimg
import matplotlib as mpl
import copy
import imageio
import math

'''
It clears some inconsistencies in the data, such as Parties of some classes of people invited in Parliamentary Sessions

Input:
    citations: Citations DataFrame

Output:
    Clean citations DataFrame
'''

def clean(citations):
    not_politicians = ['Presidente', 'Secretária', 'Secretário', 'Ministra', 'Ministro']
    for not_politician in not_politicians:
        citations.loc[citations['Person'].str.contains(not_politician), 'Party'] = np.nan
    citations.dropna(axis=0, inplace=True)
    citations.replace(to_replace='Partido Socialista', value='PS', inplace=True)
    citations.replace(to_replace='SD', value=np.nan, inplace=True)
    citations.replace(to_replace='N insc.', value=np.nan, inplace=True)    
    return citations

'''
Generates basic comparative graph of the people who most participated in discussions containing the keywords

Inputs:
    direct_citations: Dialogue dataset containing only rows with explicit citations to the keywords
    indirect_citations: Dialogue dataset containing only rows that are in the same subject of the explicit citation to the keywords

Optional:
    number: Maximum number of people that will be shown in the graph (default = 25)
    
Output:
    Bar graph showing which people participated directly and indirectly in discussions containing the keywords
'''

def persons_statistics(direct_citations, indirect_citations, number=25):
    fig, axs = plt.subplots(1, 2, constrained_layout=True, figsize=(14,5))
    fig.suptitle('Gráficos de Estatísticas básicas de Pessoas')
    axs[0].set_title('Participação direta de Pessoas')
    axs[1].set_title('Participação indireta de Pessoas')
    sns.countplot(ax=axs[0], x='Person', data= direct_citations, order=direct_citations['Person'].value_counts().index)
    sns.countplot(ax=axs[1], x='Person', data= indirect_citations[-(indirect_citations['Person'] == 'Presidente')],
                  order=indirect_citations['Person'].value_counts().iloc[:number].index)
    axs[0].tick_params(axis='x', rotation=90)
    axs[1].tick_params(axis='x', rotation=90)
    plt.show()

'''
Returns general information about Portuguese parties in a dictionary format

Input:
    No input is required

Optional:
    custom_info_dict: Custom dictionary with parties informations

Output:
    Dictionary with parties informations
'''

def load_infos(custom_info_dict=None):
    if custom_info_dict == None:
            infos = {
                'PS'     : {
                    'color' : '#FF66FF',
                    'orientation' : 'Esquerda',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido4_0.gif',
                    'coordinates' : (-2.5, 3.1),
                },
                'PSD'    : {
                    'color' : '#F68A21',
                    'orientation' : 'Direita',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido3_1.gif',
                    'coordinates' : (1.6, -1),
                },
                'BE'     : {
                    'color' : '#D21F1B',
                    'orientation' : 'Esquerda',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido14_0.gif',
                    'coordinates' : (-3.5, 0.5),
                },
                'PCP'    : {
                    'color' : '#FF0000',
                    'orientation' : 'Esquerda',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido1_0.gif',
                    'coordinates' : (-3.5, -4.7),
                },
                'CDS-PP' : {
                    'color' : '#0091DC',
                    'orientation' : 'Direita',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido2_0.gif',
                    'coordinates' : (2.5, -2.1),
                },
                'PAN'    : {
                    'color' : '#036A84',
                    'orientation' : 'Esquerda',
                    'url_image' : 'http://www.cne.pt/sites/default/files/pan_2014.jpg',
                    'coordinates' : (-3.4, 3.2),
                },
                'PEV'    : {
                    'color' : '#73BE43',
                    'orientation' : 'Esquerda',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido10_0.gif',
                    'coordinates' : (-2.1, -2.5),
                },
                'CH'     : {
                    'color' : '#333399',
                    'orientation' : 'Direita',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido_chega.png',
                    'coordinates' : (5, -3.6),
                },
                'IL'     : {
                    'color' : '#00AEEE',
                    'orientation' : 'Direita',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido_liberal.png',
                    'coordinates' : (1, 0.5) #???,
                },
                'JPP'    : {
                    'color' : '#0E766D',
                    'orientation' : 'Centro',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido_jpp.jpg',
                    'coordinates' : (0, 0) #???,
                },
                'PPM'    : {
                    'color' : '#014A94',
                    'orientation' : 'Direita',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido5_0.gif',
                    'coordinates' : (1.25, -2.1) #???,
                },
                'NC'     : {
                    'color' : '#FEAB19',
                    'orientation' : 'Direita',
                    'url_image' : 'http://www.cne.pt/sites/default/files/partido_nos_cidadaos.jpg',
                    'coordinates' : (0, 0.9) #???,
                },
                'L'      : {
                    'color' : '#98C75A',
                    'orientation' : 'Esquerda',
                    'url_image' : 'http://www.cne.pt/sites/default/files/livre.png',
                    'coordinates' : (-4.6, 2.7),
                },
            }
            return infos
    else:
        return custom_info_dict

'''
Generates basic comparative graph of the people who most participate in discussions that contain the keywords of a specific party

Inputs:
    direct_citations: Dialogue dataset containing only rows with explicit citations to the keywords
    indirect_citations: Dialogue dataset containing only rows that are in the same subject of the explicit citation to the keywords
    party: The Portuguese political party of interest

Optional:
    number: Maximum number of people that will be shown in the graph (default = 25)
    infos: Dictionary containg informations about the parties (default = built in method)
    
Output:
    Bar graph showing which people from a given political party participated directly and indirectly in discussions containing the keywords
''' 

def persons_byparty_statistics(direct_citations, indirect_citations, party, number=25, infos=load_infos()):
    direct_party = direct_citations.loc[direct_citations['Party'] == party]
    indirect_party = indirect_citations.loc[indirect_citations['Party'] == party]

    fig, axs = plt.subplots(1, 2, constrained_layout=True, figsize=(14,5))
    fig.suptitle('Gráficos de Estatísticas básicas das Pessoas do {}'.format(party))
    axs[0].set_title('Participação direta de Pessoas do {}'.format(party))
    axs[1].set_title('Participação indireta de Pessoas {}'.format(party))

    party_color = infos[party]['color']
    
    if len(direct_party) >= number:
        cmap = LinearSegmentedColormap.from_list('My_cmap', colors=['#E8E8E8', party_color], N=number)
        cmap = [rgb2hex(cmap(i)) for i in range(cmap.N)]
        cmap = cmap[::-1]
        sns.countplot(ax=axs[0], x='Person',
                data= direct_party,
                palette=cmap,
                order=direct_party['Person'].value_counts().iloc[:number].index)
    else:
        cmap = LinearSegmentedColormap.from_list('My_cmap', colors=['#E8E8E8', party_color], N=len(direct_party['Person'].unique()))
        cmap = [rgb2hex(cmap(i)) for i in range(cmap.N)]
        cmap = cmap[::-1]
        sns.countplot(ax=axs[0], x='Person',
                data= direct_party,
                palette=cmap,
                order=direct_party['Person'].value_counts().iloc[:number].index)
        
    if len(indirect_party) >= number:
        cmap = LinearSegmentedColormap.from_list('My_cmap', colors=['#E8E8E8', party_color], N=number)
        cmap = [rgb2hex(cmap(i)) for i in range(cmap.N)]
        cmap = cmap[::-1]
        sns.countplot(ax=axs[1], x='Person',
                data= indirect_party,
                palette=cmap,
                order=indirect_party['Person'].value_counts().iloc[:number].index)
    else:
        cmap = LinearSegmentedColormap.from_list('My_cmap', colors=['#E8E8E8', party_color], N=len(indirect_party['Person'].unique()))
        cmap = [rgb2hex(cmap(i)) for i in range(cmap.N)]
        cmap = cmap[::-1]
        sns.countplot(ax=axs[1], x='Person',
                data= indirect_party,
                palette=cmap,
                order=indirect_party['Person'].value_counts().iloc[:number].index)
    
    axs[0].tick_params(axis='x', rotation=90)
    axs[1].tick_params(axis='x', rotation=90)
    plt.show()

'''
Generates basic comparative graph of the parties who most participate in discussions that contain the keywords

Inputs:
    direct_citations: Dialogue dataset containing only rows with explicit citations to the keywords,
    indirect_citations: Dialogue dataset containing only rows that are in the same subject of the explicit citation to the keywords,

Optional:
    infos: Dictionary containg informations about the parties (default = built in method)
    
Output:
    Bar graph showing which political party participated directly and indirectly in discussions containing the keywords
'''

def parties_statistics(direct_citations, indirect_citations, infos=load_infos()):
    
    party_colors = {}
    for party in infos:
        party_colors[party] = infos[party]['color']
    
    fig, axs = plt.subplots(1, 2, constrained_layout=True, figsize=(14,5))
    fig.suptitle('Gráficos de Estatísticas básicas de Partidos')
    axs[0].set_title('Participação direta de Partidos')
    axs[1].set_title('Participação indireta de Partidos')

    sns.countplot(ax=axs[0], x='Party',
                  data= direct_citations, palette=party_colors,
                  order=direct_citations['Party'].value_counts().index)
    
    sns.countplot(ax=axs[1], x='Party', 
                  data= indirect_citations, palette=party_colors,
                  order=indirect_citations['Party'].value_counts().index)

    axs[0].tick_params(axis='x', rotation=90)
    axs[1].tick_params(axis='x', rotation=90)
    
    plt.show()

'''
Generates basic comparative graph of the parties who most participate in discussions that contain the keywords

Inputs:
    direct_citations: Dialogue dataset containing only rows with explicit citations to the keywords,
    indirect_citations: Dialogue dataset containing only rows that are in the same subject of the explicit citation to the keywords,

Optional:
    infos: Dictionary containg informations about the parties (default = built in method)
    
Output:
    Pie graph showing which political party participated directly and indirectly in discussions containing the keywords
'''

def parties_statistics_pie(direct_citations, indirect_citations, infos=load_infos()):
    
    party_colors = {}
    for party in infos:
        party_colors[party] = infos[party]['color']
    
    fig, axs = plt.subplots(1, 2, sharey=True, 
                            constrained_layout=True, 
                            figsize=(17,5))
    fig.suptitle('Gráficos de Estatísticas básicas de Partidos')
    axs[0].set_title('Participação direta de Partidos')
    axs[1].set_title('Participação indireta de Partidos')

    direct_parties = {
        'Parties' : [],
        '# Citations' : [],
    }
    indirect_parties = {
        'Parties' : [],
        '# Citations' : [],
    }

    for party in direct_citations['Party'].unique().tolist():
        if str(party) != str(np.nan):
            direct_parties['Parties'].append(party)
            direct_parties['# Citations'].append(len(direct_citations.loc[direct_citations['Party'] == party]))

    for party in indirect_citations['Party'].unique().tolist():
        if str(party) != str(np.nan):
            indirect_parties['Parties'].append(party)
            indirect_parties['# Citations'].append(len(indirect_citations.loc[indirect_citations['Party'] == party]))


    direct_parties = pd.DataFrame.from_dict(direct_parties).sort_values(by=['# Citations'], ascending=False)
    indirect_parties = pd.DataFrame.from_dict(indirect_parties).sort_values(by=['# Citations'], ascending=False)

    labels = direct_parties['Parties'].unique()

    axs[0].pie(x='# Citations', labels=labels,
               shadow=True, startangle=0, 
               explode=[0.1]+[0]*(len(direct_parties)-1), 
               data=direct_parties,
               colors=[party_colors[key] for key in labels])

    labels = indirect_parties['Parties'].unique()

    axs[1].pie(x='# Citations', labels=labels,
               shadow=True, startangle=0, 
               explode=[0.1]+[0]*(len(indirect_parties)-1), 
               data=indirect_parties,
               colors=[party_colors[key] for key in labels])

    plt.show()



'''
This is an auxiliary method to take the DataFrame of citations and convert it into a DataFrames dictionary with the date as the key, used to create the political-economic graph and as an intermediate step.

Input:
    citations: Citations DataFrame

Optional:
    infos: Dictionary containg informations about the parties (default = built in method)

Output:
    Ditionary of DataFrames with the date as the key
    List of dates in the DataFrames

'''

def create_dataframes(citations, infos=load_infos()):
    df_dict = {}
    dates = citations['Date'].unique().tolist()
    grouped = citations.groupby(citations['Date'])
    
    for i in range(len(dates)):

        group = grouped.get_group(citations['Date'].unique().tolist()[i])

        df_dict[str(dates[i])] = {            
            'Party' : [],
            'Count' : [],
            'Color' : [],
            'Orientation' : [],
            'Image' : [],
            'X_coordinate' : [],
            'Y_coordinate' : [],
        }
        
        for party in infos:
            
            df_dict[str(dates[i])]['Party'].append(party)
            df_dict[str(dates[i])]['Count'].append(len(group.loc[group['Party'] == party]))
            df_dict[str(dates[i])]['Color'].append(infos[party]['color'])
            df_dict[str(dates[i])]['Orientation'].append(infos[party]['orientation'])
            df_dict[str(dates[i])]['Image'].append(infos[party]['url_image'])
            df_dict[str(dates[i])]['X_coordinate'].append(infos[party]['coordinates'][0])
            df_dict[str(dates[i])]['Y_coordinate'].append(infos[party]['coordinates'][1])

        df_dict[str(dates[i])] = pd.DataFrame(df_dict[str(dates[i])])

    dates = [str(date) for date in dates]
    dates.sort()

    return df_dict, dates

'''
Creates a graph with the political and economic coordinates of the parties and has an additional variable, represented by the size of the point, which matches the number of times that a particular party participated in citations of the keywords

Input:
    df: A DataFrame of citations for a specific date
    date: The specific date to which the dataframe refers
    Note: The create_dataframes function will make a dictionary with the key = data and value = df, in the same way that it is used in this function

Optional:
    normalization: Tells the graph what is the minimum and maximum value for resizing the point values. The minimum value is usually 0 and the  maximum is the highest number of citations accumulated in the entire period. (default = (0, 405))

Output:
    Graph containing the number of mentions of keywords by party distributed according to their political-economic ideals
'''

def create_politic_economic_graph(df, date, normalization=(0, 405)):
    colors = {}

    for i in range(len(df)):
        colors[df['Party'][i]] = df['Color'][i]

    sns.set_style('darkgrid')
    sns.set_context('paper')
    sns.set(font_scale=1.1)

    plt.figure(figsize=(14, 14))
    ax = sns.scatterplot(x='X_coordinate', y='Y_coordinate', data=df,
                         palette=colors, hue='Party', size='Count', 
                         alpha=0.5, sizes=(100, 10000),
                         size_norm=(normalization[0], normalization[1]))

    ax.set_title('Eixo político-econômico: Acumulado até ' + str(date), y=1.04, fontsize='x-large')

    ax.set(xlim=(-5.5, 5.5), ylim=(-5.5, 5.5))
    
    ax.axhline(y=0, linewidth=0.5, color='black')
    ax.axvline(x=0, linewidth=0.5, color='black')

    for i in range(len(df)):
        ax.annotate(df['Party'][i],
                    xy=(df['X_coordinate'][i], df['Y_coordinate'][i]),
                    xycoords='data',
                    xytext=(df['X_coordinate'][i]-0.15, df['Y_coordinate'][i]+0.15),
                    )
        ax.annotate(df['Count'][i],
            xy=(df['X_coordinate'][i], df['Y_coordinate'][i]),
            xycoords='data',
            xytext=(df['X_coordinate'][i]+0.1, df['Y_coordinate'][i]-0.1),
            )
    
    ax.legend(fancybox=True, shadow=True)

    plt.xticks(np.arange(-5, 6, 1), 5*['']+['Conservador']+5*[''], fontsize='large')
    plt.yticks(np.arange(-5, 6, 1), 5*['']+['Esquerda']+5*[''], fontsize='large')

    labelx = ax.set_xlabel('Liberal', fontsize='large')
    ax.xaxis.set_label_coords(0.5, 1.03)

    labely = ax.set_ylabel('Direita', fontsize='large', rotation='horizontal')
    ax.yaxis.set_label_coords(1.04, 0.489)
    
    ax.get_legend().remove()
    
    plt.close()

    return ax.get_figure()

'''
Calculates the accumulation of keyword citations across all dataframes in the dictionary

Input:
    citations_dict: A dictionary of DataFrames, with the dates as key
    citations_dates: A list of the dates (keys) 

Output:
    Dataframes dictionary with citation count for keywords accumulated up to the date provided by the key
'''

def acumulative(citations_dict, citations_dates):

    acumulative_dict = copy.deepcopy(citations_dict)

    for i in range(1, len(citations_dates)):
        acumulative_dict[citations_dates[i]]['Count'] += acumulative_dict[citations_dates[i-1]]['Count']
    
    return acumulative_dict

'''
Clears parties that have not had keyword quotes throughout the selected period

Input:
    acumulative_dict: A dictionary of DataFrames, with the dates as key and with citation count for keywords accumulated
    acumulative_dates: A list of the dates (keys) 

Output:
    Accumulative_dict without parties that did not cite the keywords
'''

def clean_acumulative(acumulative_dict, acumulative_dates):

    clean_dict = copy.deepcopy(acumulative_dict)

    last_df = clean_dict[acumulative_dates[-1]]
    null_values = []

    for i in range(len(last_df['Party'])):
        if last_df['Count'][i] == 0:
            null_values.append(last_df['Party'][i])

    for date in acumulative_dates:
        for party in null_values:
            clean_dict[date] = clean_dict[date][clean_dict[date]['Party'] != party]
        clean_dict[date].reset_index(drop=True, inplace=True)    
    return clean_dict

'''
Automated way to obtain the normalization parameters for the create_politic_economic_graph function

Input:
    acumulative_dict (cleaned): A dictionary of DataFrames, with the dates as key and with citation count for keywords accumulated
    acumulative_dates: A list of the dates (keys) 

Output:
    Min and Max values for normalization of the points, used in create_politic_economic_graph
'''

def get_normalization(citations_dict, citations_dates):
    return (citations_dict[citations_dates[0]]['Count'].min(), citations_dict[citations_dates[-1]]['Count'].max())

'''
Uses the various auxiliary functions such as create_politic_economic_graph and cumulative to generate an animated gif of the political-economic graph of the parties where each day the points increase according to the increase in citations to keywords

Input:
    acumulative_dict (cleaned): A dictionary of DataFrames, with the dates as key and with citation count for keywords accumulated
    acumulative_dates: A list of the dates (keys) 

Optional:
    folder_name: Name of the folder that will be created to save each frame of the gif and the gif itself (default = 'citations')
    gif_name: Name of the .gif file that will be generated (default = 'citations')
    duration : Duration of each frame in the gif (default = 1s)

Output:
    Animated gif of the political-economic graph of the parties in which the points increase every day as the number of citations to the keywords increases 
'''

def create_gif(citations_dict, citations_dates, folder_name='citations', gif_name='citations', duration=1):
    acumulative_dict = acumulative(citations_dict, citations_dates)
    clean_dict = clean_acumulative(acumulative_dict, citations_dates)
    norm = get_normalization(clean_dict, citations_dates)

    graph_images = []
    png_images = []
    
    origin_path = os.getcwd()
    os.makedirs(os.path.join(origin_path, folder_name), exist_ok=True)
    os.chdir(os.path.join(origin_path, folder_name))

    for i in range(len(citations_dates)):
        graph_images.append(create_politic_economic_graph(clean_dict[citations_dates[i]], citations_dates[i], norm))
        graph_images[i].savefig(citations_dates[i] + '.png')
        png_images.append(imageio.imread(citations_dates[i] + '.png'))

    imageio.mimsave(gif_name+'.gif', png_images, format='GIF', duration=1)

    display(Image(open(os.path.join(origin_path, folder_name, gif_name+'.gif'),'rb').read()))

    os.chdir(origin_path)