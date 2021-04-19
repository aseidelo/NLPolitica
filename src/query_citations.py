import pandas as pd
import re

'''
DESATUALIZADO, sera outro pacote

Define assunto de cada fala nas atas de acordo
com a comparacao de trechos padronizado no texto.

Entra: DataFrame das atas 
Sai: DataFrame das atas com coluna de assunto (Subject)
'''

def set_subject(dialogs):
    subjects = []
    # declaracoes politicas sao enumeradas em ordem crescente
    last_subject = 'declarações políticas 0'
    last_transcript = 'DAR-001'
    j = 1
    for i in range(len(dialogs['Text'])):
        name = dialogs['Person'][i]
        text = dialogs['Text'][i]
        transcript = dialogs['Transcript'][i]
        # contagem recomeca quando muda a ata (outra sessao)
        if(transcript != last_transcript):
            j = 0
            last_transcript = transcript
        # texto comparado em minusculo
        lower_text = text.lower()
        # faz comparacao apenas em falas do Presidente
        if name == 'Presidente':
            # bucs primeiramente o trecho 'declaraç' para definir declaracoes politicas
            if('declaraç' in lower_text):
                last_subject = 'declarações políticas {}'.format(j)
                j = j + 1            
            # busca 'projeto de' para definir assunto apos declaracoes (assunto e o proprio nome dos projetos)
            elif ('projeto de ' in lower_text and '/' in lower_text):
                # busca TODAS as repeticoes de 'Projeto de'
                positions = [m.start() for m in re.finditer('Projeto de', text)]
                last_subject = ''
                k = 0
                # assunto e a concatenacao dos projetos citados na mesma fala do presidente
                # Ex.: Projeto de lei 123, Projeto de resolução 456
                for position in positions:
                    if (k == 0):
                        # recupera numero do projeto: posicao de 'projeto de ' ate '/' 
                        last_subject = text[position:text.find('/', position)+4].replace('n.º ', '')
                    last_subject = last_subject + ', ' + text[position:text.find('/', position)+4].replace('n.º ', '')
                    k = k + 1
        subjects.append(last_subject)
    dialogs['Subject'] = subjects
    #dialogs.to_csv('atas_com_subject.csv')
    return dialogs

'''
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
Retorna linhas do DataFrame (data_frame) com citacoes (words) nos campos (fields) especificados

Entra: DataFrame, nome dos campos pesquisados, palavras a serem buscadas
Sai: subset do DataFrame de entrada com citacoes

'''
def get_citations(data_frame, fields, words):
    # acha posicao das citacoes
    positions = find_words(data_frame, fields, words)
    out_list = [] # pd.DataFrame(columns = data_frame.columns)
    i = 0
    for ind in positions.index:
        has_found = False
        for field_word in positions:
            # checa se position = -1 (nao encontrou texto)
            if (positions[field_word][ind] != -1):
                has_found = True
                break
        # se pelo menos uma das palavras e encontrada
        if(has_found):
            #print(data_frame.iloc[ind].values)
            # adiciona linha na lista
            out_list.append(data_frame.iloc[ind].values)
            i = i + 1
    return pd.DataFrame(out_list, columns = data_frame.columns)

'''
Busca linhas do DataFrame das atas que estao associadas as citacoes encontradas.
Ser associado significa pertencer a MESMA DISCUSSAO (mesmo tema e dia das linhas com citacoes)

ENTRA: DataFrame das atas completo, DataFrame das linhas das atas com citacoes, campos usados como chave unica (definem discussao)
SAI: DataFrame limitado com linhas com citacoes diretas e associacao indireta
'''
def get_related_dialogs(full_dataframe, citation_dataframe, key_fields):
    # cria campo key: concatenacao das strings da lista key_fields
    citation_dataframe['key'] = citation_dataframe[key_fields[0]]
    full_dataframe['key'] = full_dataframe[key_fields[0]]
    for i in range(1, len(key_fields)):
        citation_dataframe['key'] = citation_dataframe['key'] + citation_dataframe[key_fields[i]]
        full_dataframe['key'] = full_dataframe['key'] + full_dataframe[key_fields[i]]
    # pega lista de keys possiveis no dataframe de citacoes
    topics = citation_dataframe['key'].unique()
    #print(topics)
    to_out = pd.DataFrame(columns = full_dataframe.columns)
    # para cada key na lista de citacoes, busca linhas no dataframe completo com a mesma key
    for topic in topics:
        to_out = to_out.append(full_dataframe.loc[full_dataframe['key'] == topic])
    return to_out

'''
Busca linhas do DataFrame dos projetos que estao associados as citacoes encontradas NAS ATAS.
Nesse caso, ser associado significa ser citado na MESMA DISCUSSAO que citacoes as palavras buscadas
NAS ATAS.

Entra: dataframe limitado de linhas das atas com citacoes, dataframe completo de projetos
SAI: dataframe limitado de projetos associados indiretamente as citacoes
'''
def get_related_projects(citations_df, projects_df):
    to_out = pd.DataFrame(columns = projects_df.columns)
    # para cada assunto no dataframe limitado de citacoes nas atas
    for subject in citations_df['Subject'].unique():
        titles = subject.split(', ')
        # para cada projeto nos assuntos 
        for title in titles:
            # se titulo do projeto no assunto das atas se encontra no dataframe de projetos, 
            # adiciona a saida
            to_out = to_out.append(projects_df.loc[projects_df['title'] == title])
    return to_out

'''

Gera estatisticas relevantes sobre projetos, partidos e politicos
A partir da contagem e comparacao de linhas entre dataframes completos de atas/projetos e dataframes limitados

Entra: df de atas completo, df de linhas das atas com citacoes diretas, df de linhas das atas associadas indiretamente, df de projetos, df de projetos diretamente associados, df de projetos indiretamente associados
Sai: df de estatisticas de politicos, df de estatisticas de partidos, df de estatisticas de projetos

'''
def generate_statistics(all_dialogs, direct_citations_dialogs, related_dialogs, projects, direct_citations_projects, related_projects):
    # definicao inicial de dicts das estatisticas buscadas
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
    # a partir daqui, estatisticas sao computadas em ordem
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
 