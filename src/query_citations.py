import pandas as pd
import re

'''
Define the subject of each speech contained on the minute dataframe
by searching certain word sequences.

DEPRECATED, moved to different package

Inputs: minutes dataframe
Outputs: minute dataframe with added Subject field

---------------------------------------
Define assunto de cada fala nas atas de acordo
com a comparacao de trechos padronizado no texto.

DESATUALIZADO, sera outro pacote

Entra: DataFrame das atas 
Sai: DataFrame das atas com coluna de assunto (Subject)
'''

def set_subject(dialogs):
    subjects = []
    # political declarations are enumerated in ascending order
    last_subject = 'declarações políticas 0'
    last_transcript = 'DAR-001'
    j = 1
    for i in range(len(dialogs['Text'])):
        name = dialogs['Person'][i]
        text = dialogs['Text'][i]
        transcript = dialogs['Transcript'][i]
        # restart cont on new minute
        if(transcript != last_transcript):
            j = 0
            last_transcript = transcript
        # lowercase text comparisson 
        lower_text = text.lower()
        # search for presidents speeches
        if name == 'Presidente':
            # search 'declaraç' extracts on the speech
            if('declaraç' in lower_text):
                last_subject = 'declarações políticas {}'.format(j)
                j = j + 1            
            # search 'projeto de' to define the subject after political declarations (subject is defined as the name of the project in that case)
            elif ('projeto de ' in lower_text and '/' in lower_text):
                # search all repetitions of 'projeto de'
                positions = [m.start() for m in re.finditer('Projeto de', text)]
                last_subject = ''
                k = 0
                # subject is the concatenation of citated projects on the same president speech
                # Ex.: Projeto de lei 123, Projeto de resolução 456
                for position in positions:
                    if (k == 0):
                        # retrieve project number identification
                        last_subject = text[position:text.find('/', position)+4].replace('n.º ', '')
                    last_subject = last_subject + ', ' + text[position:text.find('/', position)+4].replace('n.º ', '')
                    k = k + 1
        subjects.append(last_subject)
    dialogs['Subject'] = subjects
    #dialogs.to_csv('atas_com_subject.csv')
    return dialogs

'''
Find citation position in one or more fields of a given DataFrame

Input: dataframe to be inspected, list of fields to be inspected, list of words to search for
Output: Citations positions on searched fields, -1 when not found

---------------------------------

Encontra posicao das citacoes (words) em um ou mais campo(s) (fields) de um DataFrame (data_frame)

Sai: posicoes das citacoes nos campos buscados, quando nao encontra posicao e -1

'''
def find_words(data_frame, fields, words):
    series = [data_frame[field] for field in fields]
    positions = pd.DataFrame()
    for serie in series:
        for word in words:
            positions[serie.name+'_'+word+"_pos"] = serie.str.lower().str.find(word)
    return positions

'''
Returns DataFrame lines that contain citations on specified fields

Input: dataframe, list of fields to be inspected, list of words to search for
Output: Subset of input dataframe with only rows with citations

----------------------------------------------

Retorna linhas do DataFrame (data_frame) com citacoes (words) nos campos (fields) especificados

Entra: DataFrame, nome dos campos pesquisados, palavras a serem buscadas
Sai: subset do DataFrame de entrada com citacoes

'''
def get_citations(data_frame, fields, words):
    # find citation positions
    positions = find_words(data_frame, fields, words)
    out_list = [] # pd.DataFrame(columns = data_frame.columns)
    i = 0
    for ind in positions.index:
        has_found = False
        for field_word in positions:
            # check if position = -1 (word not found)
            if (positions[field_word][ind] != -1):
                has_found = True
                break
        # if at least one word is found
        if(has_found):
            #print(data_frame.iloc[ind].values)
            # add line to the list 
            out_list.append(data_frame.iloc[ind].values)
            i = i + 1
    return pd.DataFrame(out_list, columns = data_frame.columns)

'''
Search for lines on minutes dataframe that are indirectly associated with the citations.
Been indirectly associated means that the speech belongs in the same discussion (same subject and day)

Input: Complete minutes dataframe, subset of minutes dataframe with citations, fields utilized as unique keys
Output: subset of minutes dataframe if rows directly (with citations) and indirectly (same discussion as the previous) related to the search words

-----------------------
Busca linhas do DataFrame das atas que estao associadas as citacoes encontradas.
Ser associado significa pertencer a MESMA DISCUSSAO (mesmo tema e dia das linhas com citacoes)

ENTRA: DataFrame das atas completo, DataFrame das linhas das atas com citacoes, campos usados como chave unica (definem discussao)
SAI: DataFrame limitado com linhas com citacoes diretas e associacao indireta
'''
def get_related_dialogs(full_dataframe, citation_dataframe, key_fields):
    # create key field: concatenation of strings at key_fields input
    citation_dataframe['key'] = citation_dataframe[key_fields[0]]
    full_dataframe['key'] = full_dataframe[key_fields[0]]
    for i in range(1, len(key_fields)):
        citation_dataframe['key'] = citation_dataframe['key'] + citation_dataframe[key_fields[i]]
        full_dataframe['key'] = full_dataframe['key'] + full_dataframe[key_fields[i]]
    # retrieve list of possible keys at citations dataframe
    topics = citation_dataframe['key'].unique()
    #print(topics)
    to_out = pd.DataFrame(columns = full_dataframe.columns)
    # for each possible key, search for lines in complete minutes dataframe with the same key
    for topic in topics:
        to_out = to_out.append(full_dataframe.loc[full_dataframe['key'] == topic])
    return to_out

'''
Search for projects dataframe lines that are associated to the citations found at the minutes.
On this case, been associated means to be cited at the same discussion as searched words on minutes dataframe.

Input: subset of minutes dataframe with citations, complete projects dataframe
Output: subset of projects dataframe with projects associated to the searched words

---------------------------------------------------
Busca linhas do DataFrame dos projetos que estao associados as citacoes encontradas NAS ATAS.
Nesse caso, ser associado significa ser citado na MESMA DISCUSSAO que citacoes as palavras buscadas
NAS ATAS.

Entra: dataframe limitado de linhas das atas com citacoes, dataframe completo de projetos
SAI: dataframe limitado de projetos associados indiretamente as citacoes
'''
def get_related_projects(citations_df, projects_df):
    to_out = pd.DataFrame(columns = projects_df.columns)
    # for each subject in the citations dataframe
    for subject in citations_df['Subject'].unique():
        titles = subject.split(', ')
        # for each project contained in the subject
        for title in titles:
            # if project title at citations dataframe is at projects dataframe, add to the output
            to_out = to_out.append(projects_df.loc[projects_df['title'] == title])
    return to_out

'''
Generate relevant statistics about the projects, parties and politicians 
by counting and comparing complete projects and minutes dataframes with subsets with citations.

Input: complete minutes df, direct citations minutes df, indirectly related minutes df, complete projects df, directly related projects df,  indirectly related projects df
Output: politicians statistics df, parties statistics df, projects statistics df

--------------------------------------
Gera estatisticas relevantes sobre projetos, partidos e politicos
A partir da contagem e comparacao de linhas entre dataframes completos de atas/projetos e dataframes limitados

Entra: df de atas completo, df de linhas das atas com citacoes diretas, df de linhas das atas associadas indiretamente, df de projetos, df de projetos diretamente associados, df de projetos indiretamente associados
Sai: df de estatisticas de politicos, df de estatisticas de partidos, df de estatisticas de projetos
'''

def generate_statistics(all_dialogs, direct_citations_dialogs, related_dialogs, projects, direct_citations_projects, related_projects):
    # initial definition of statistics dicts 
    people_statistics = {'name' : [], 
               'amount_of_corruption_citations' : [], 
               'amount_of_discussion_participations' : [],
                'percentage_of_discussion_participations' : []}
    party_statistics = {'name' : [], 
               'amount_of_corruption_citations' : [], 
               'amount_of_discussion_participations' : []}
    projects_statistics = {'total_amount_of_projects' : 0,
                'amount_of_projects_with_direct_citations' : 0,
                'amount_of_related_projects' : 0,
                'percentage_of_corruption_related_projects' : 0.,
                'people_involved' : []}
    # from here on, statistics are processed in order
    # PEOPLE
    people_statistics['name'] = all_dialogs['Person'].unique()
    total_participations = len(direct_citations_dialogs)
    for name in people_statistics['name']:
        people_statistics['amount_of_corruption_citations'].append(len(direct_citations_dialogs.loc[direct_citations_dialogs['Person'] == name]))
        people_statistics['amount_of_discussion_participations'].append(len(related_dialogs.loc[related_dialogs['Person'] == name]))
        people_statistics['percentage_of_discussion_participations'].append(float(people_statistics['amount_of_discussion_participations'][-1])/total_participations)
    # PARTIES
    party_statistics['name'] = all_dialogs['Party'].unique()
    for name in party_statistics['name']:
        party_statistics['amount_of_corruption_citations'].append(len(direct_citations_dialogs.loc[direct_citations_dialogs['Party'] == name]))
        party_statistics['amount_of_discussion_participations'].append(len(related_dialogs.loc[related_dialogs['Party'] == name]))
    # PROJECTS
    projects_statistics['amount_of_related_projects'] = len(direct_citations_projects)
    projects_statistics['amount_of_projects_with_direct_citations'] = len(direct_citations_projects)
    projects_statistics['total_amount_of_projects'] = len(projects)
    projects_statistics['percentage_of_corruption_related_projects'] = float(projects_statistics['amount_of_related_projects'])/projects_statistics['total_amount_of_projects']
    for authors_list in direct_citations_projects['author'].unique():
        for author in authors_list.split(','):
            if(author not in projects_statistics['people_involved']):
                projects_statistics['people_involved'].append(author)
    return pd.DataFrame.from_dict(people_statistics), pd.DataFrame.from_dict(party_statistics), projects_statistics
 