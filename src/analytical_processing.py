import numpy as np
import pandas as pd

def _prepare_keyword_sring(df):
    '''
        Placeholder
    '''
    arr = []
    for cat, keywords in df.iteritems():
        arr.append([cat, '|'.join(keywords)])

    return arr

def naive_keyword_search(df,
                        keywords_str
                        ):
    '''
       Check if keyword from dictionary exist in translated text.
           * No hashing
           * No stema- or lemmatizations
           * No specific text preprocessing
           * No specific text modeling
           * No specific embedings
           V Just search and return of searched groups
    '''
    find_arr = []
    for keyword_str in keywords_str:
        col_name = '_'.join(keyword_str[0]) + '_flag'
        find_arr = df.translated_text.str.lower().str.findall(keyword_str[1])

        df.loc[:, col_name] = find_arr.where(cond=~find_arr.isin([[]]), other=np.nan)
        #df.loc[:, subcat_col_name_str] = df.translated_text.str.contains(group_keywords_str, case=False)
        #break

    return df
