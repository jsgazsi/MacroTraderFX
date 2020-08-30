import pandas as pd
#from pandas_ods_reader import read_ods
import numpy as np
import io
import os
import requests
from functools import reduce
import scipy as sp
from scipy.stats import zscore
from functools import reduce
#import pandas_datareader as web
import yfinance as yf

Convert_MoM_to_YoY = [
    "United States Philadelphia Federal Reserve Manufacturing Index.csv",
    "United States Producer Price Index (PPI) YoY.csv",
    "United States Redbook YoY.csv",
    "United States Retail Sales Ex Gas Autos MoM.csv",
    "United States Retail Sales MoM.csv",
]

#path = "../MacroTraderFX/CSV_Data/"
path = 'CSV_Data/'

def MoM_to_Index(df):
    df.Value = df.Value/100
    df.Value = 100*np.exp(np.nan_to_num(df.Value.cumsum()))
    df.Value = df.Value.round(1)    
    return df

def Simple_YoY_Conversion(df):
    df = df.Value.pct_change(12) * 100
    df = df.round(2)
    return df

def MoM_to_YoY(df):
    df = MoM_to_Index(df)
    df.Value = df.Value.pct_change(12) * 100
    df = df.round(2)
    #df.Value = df.Value.fillna(0)
    return df

#This function gets the data for an economic indicator (e.g. GDP, Unemployment), and normalizes the data to it's Standard Score (Z-Score))
def getData(str, inverse_correlation):
    df = pd.read_csv(path + str, delimiter=',')
    df = df.replace({'M':'', '%':'', 'B':'', 'K':'', ',':''}, regex=True)
    df['Date'] = pd.to_datetime(df['Date'])   #####.dt.strftime('%Y-%m')
    df = df.set_index('Date')
    df.Value = df.Value.astype(float)
    #If in list to convert MoM to YoY
    if str in Convert_MoM_to_YoY:
        df = MoM_to_YoY(df)
    df.Value = df.apply(lambda x: (x-x.expanding().mean())/x.expanding().std())
    df = df.round(2)
    ##If the indicator is inversely correlated to economic activity (i.e. Unemployment) Correct the correlation by multiplying by -1
    if (inverse_correlation=='TRUE'):
        df = df.multiply(-1)
    
    return df

US_test = getData("United States Retail Sales MoM.csv", False)


with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
    print(US_test)



