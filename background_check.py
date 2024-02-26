import pandas as pd
import numpy as np
import string
from dotenv import load_dotenv
load_dotenv()

def read_response(SHEET_ID:str) -> pd.DataFrame:
    """
    This function reads the results of the GSheet as a result 
    of filling out the background check's GForm.

    Args: 
        - SHEET_ID(str): googlesheet id

    Returns:
        - dataframe of GForm response
    """
    
    # declare url
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

    # read csv 
    data = pd.read_csv(url)

    return data

def simple_clean(txt:str) -> str:
    """
    This function does: 
      - lowering all letters
      - removing unnecessary space
      - removing punctuation.

    Args: 
        - txt(str): raw text data

    Returns:
        - cleaned text data
    """

    # skip cleaning steps if there is no text (empty response/answer)
    if len(str(txt))<1: 
        return txt
    
    # do the cleaning
    txt = txt.lower() # lowering text
    txt = txt.strip() # remove excess white space
    txt = txt.translate(str.maketrans("","",string.punctuation)) # remove punctuation

    return txt

def preprocess_text_data(df:pd.DataFrame) -> pd.DataFrame:
    """
    This function aims to process text data from the "Background Check" Form 
    before it is visualized.
    """
    cols = df.columns # get column names
    df_txt = df[cols[-2:]].copy() # create new dataframe that consist text(paragraph) from GForm
    df_txt.replace({np.nan:"", "-":"", "None":""}, inplace=True) # make consistency of missing value

    for col, simple_meaning in list(zip(*[df_txt.columns, ["expectation", "obstacle"]])): # iterating every column
        df_txt[col] = df_txt[col].apply(lambda t: simple_clean(t)) # do cleaning text data
        df_txt[f"{simple_meaning}_answer_length"] = df_txt[col].apply(lambda txt: len(str(txt))) # measure text length
        df_txt.rename(columns={col: simple_meaning}, inplace=True) # renaming columns

    df_txt.sort_values(by=list(df_txt.columns[2:]), ascending=[False]*2, inplace=True) # sorting dataframe

    return df_txt