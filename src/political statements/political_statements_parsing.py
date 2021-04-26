"""Political Statements Parser

This script is responsible for analyzing the political statements made 
on a dataframe that consolidates Minutes of the Assembly of the Republic 
of Portugal and separating them into blocks of dialogues on the same 
subject. This is important to identify direct citations to a given 
subject, and participations in the discussion on this topic (which we called
indirect citations).

This parser expects that the consolidated data frame of minutes (the input) 
has already been pre-processed (
 ******************** include here information on how it should be 
                                pre-processed in query_citations.py) 
and contains the columns 'Transcript' that defines the meeting's identifier, 
'Person' that defines who is the current debater (in Portuguese, 'orador') 
of each line (remark) and 'Subject' that contains the subject of each 
line.

This script requires that `pandas` and `re` be installed within the Python
environment you are running this in. It also requires that the 
'ChairmanStatementClassifier' module be included.

This file can also be imported as a module and contains the following
functions:

    * political_statements_parsing - process the minutes of the Assembly
    * main - an execution example importing an existing dataframe saved in .xlsx.
"""

import re

import pandas as pd

from models.StatementsClassifier import ChairmanStatementClassifier


def political_statements_parsing(full_df):
  """It classifies the statements of the session chairman (in Portuguese, 
      'Presidente') and uses that information to separate different dialogues.

    Parameters
    ----------
    full_df : pandas.core.frame.DataFrame
        The Minutes of the Assembly of the Republic

  """
  #Select only the lines that refer to the political statements and make a copy
  df_mask = full_df['Subject'].str.contains('Declarações políticas', flags=re.IGNORECASE, regex=True)
  df_political_statements = full_df[df_mask].copy()

  #Create the chairman's declarations classifier
  classifier = ChairmanStatementClassifier()

  #Defines num_dialog which is an Id of each dialog within the same meeting
  num_dialog = 0 

  #Defines a boolean variable that tracks if the dialogue has changed based on the chairman's lines
  new_dialog = False 

  #Defines current_minute as the id of the current minute being analyzed
  #And sets as the minute of first meeting in the dataframe
  start_index = df_political_statements.index.to_list()[0]
  current_minute = df_political_statements.loc[start_index]['Transcript']
  
  #For-loop that iterates over the political statements lines
  for index, row in df_political_statements.iterrows():

    #Verify if a new dialog is starting when it is the chairman speaking
    if row['Person'] == 'Presidente' and classifier(row['Text']):
        new_dialog = True

    #Verify if it is a new session (new meeting) and update variables
    if row['Transcript'] != current_minute:
      new_dialog = True
      current_minute = row['Transcript']
      num_dialog = 0

    #Increments the dialog id in case of a new dialog
    if new_dialog:
      new_dialog = False
      num_dialog +=1

    #Set the subject of the line adding the number of the dialog it belongs
    df_political_statements.loc[index, 'Subject'] = 'Declarações políticas ' + str(num_dialog)
  
  #Insted of returning a new dataframe, it updates the given as input
  full_df.update(df_political_statements)

def main():
  data_path = '../data/'
  dialogs_file = 'dialog_lines_with_discussion_topic_EXAMPLE.xlsx'
  dialogs = pd.read_excel(data_path+dialogs_file)
  
  political_statements_parsing(dialogs)
  
  dialogs.to_excel('output.xlsx')  

if __name__ == "__main__":
    main()