import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

class helper():
    def __init__(self):
        pass
    def dropcol(self, df, cols):
        return df.drop(cols, axis = 1, inplace = True)

    # we convert dates to datetime format
    def to_datetime(self,data, cols):
        for col in cols:
            data[col] = pd.to_datetime(data[col])

    def extract_hour(self, df):
        df['HORA'] = df['Fecha-I'].hour 

    def periodo_dia(self,df):
        self.extract_hour(df)
        if (df['HORA'] >= 5) and (df['HORA'] < 12):
            return 'mañana'
        elif  (df['HORA'] >=12) and  (df['HORA'] < 19):
            return 'tarde'
        elif  (df['HORA'] >=19) or  (df['HORA'] < 5):
            return 'noche'

    def addcol_periodo_dia(self,df):
        df['periodo_dia'] = df.apply(lambda x: self.periodo_dia(x), axis = 1)

    def analisis_atraso_por_col(self,df,col):
        # % de vuelos atrasados por col
        col_atraso = df.groupby([col])['atraso_15'].value_counts(normalize=True)
        col_atraso = col_atraso.groupby([col]).apply(lambda x: x.iloc[0]).reset_index().sort_values(by = 'atraso_15')
        col_atraso.rename(columns = {'atraso_15':'%_no_atrasados'}, inplace=True)
        col_atraso['atraso_15']= 1-col_atraso['%_no_atrasados']
        # % de vuelos operados por cada col 
        column_df = df[col].value_counts(normalize=True).reset_index()
        column_df.rename(columns = {f'{col}':'%_de_total_vuelos'}, inplace=True)
        column_df[f'%_atrasados_por_{col}'] = col_atraso['atraso_15']
        atraso_total = (df.groupby(col)['atraso_15'].sum()/len(df[df['atraso_15']==1])).reset_index()
        column_df = pd.merge(atraso_total, column_df, left_on = [col], right_on= ['index'], how = 'left')
        column_df.rename(columns = {'atraso_15':'%_atrasados_de_total_atrasados'}, inplace=True)
        column_df = column_df.sort_values('%_de_total_vuelos', ascending = False)
        column_df['cumsum_total_vuelos'] = column_df['%_de_total_vuelos'].cumsum()
        column_df['cumsum_atrasados'] = column_df['%_atrasados_de_total_atrasados'].cumsum()
        self.dropcol(column_df,['index'])
        return column_df 

    def DummyCol(self,df,columnsToEncode):
        df = pd.get_dummies(df,columns = columnsToEncode, drop_first=False)
        return df
    