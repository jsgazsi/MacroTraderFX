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
    "United States Retail Sales Ex Gas Autos MoM.csv",
    "United States Retail Sales MoM.csv",
    "United States Business Inventories MoM.csv",
    "United States Construction Spending MoM.csv",
    "United States Core Retail Sales MoM.csv",
    "United States Durables Excluding Defense MoM.csv",
    "United States Factory Orders ex Transportation MoM.csv",
    "United States Factory Orders MoM.csv",
    "United States House Price Index (HPI) MoM.csv",
    "United States Industrial Production MoM.csv",
    "United States Manufacturing Production MoM.csv",
    "United States Personal Spending MoM.csv",
    "United States Wholesale Inventories MoM.csv",
]
#Macro Trader Test
#import Macro_CSV_Lists

#path = "../MacroTraderFX/CSV_Data/"
path = 'CSV_Data/'

def MoM_to_Index(df):
    df.Value = df.Value/100
    df.Value = 100*np.exp(np.nan_to_num(df.Value.cumsum()))
    df.Value = df.Value.round(1)    
    return df

def Simple_YoY_Conversion(df):
    df.Value = df.Value.pct_change(12) * 100
    df = df.round(2)
    return df

def MoM_to_YoY(df):
    df = MoM_to_Index(df)
    df = Simple_YoY_Conversion(df)
    #df.Value = df.Value.pct_change(12) * 100
    #df = df.round(2)
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
    df.Value = df.apply(lambda x: (x-x.expanding(1).mean())/x.expanding(1).std())
    #df.Value = df.apply(lambda x: (x-x.rolling(36).mean())/x.rolling(36).std())
    df = df.round(2)
    ##If the indicator is inversely correlated to economic activity (i.e. Unemployment) Correct the correlation by multiplying by -1
    if (inverse_correlation=='TRUE'):
        df = df.multiply(-1)
    return df

#Funtion not needed? Maybe for getting normalized data raw, no inverse correlation check
def getNormalized(str, inverse_correlation):
    df = pd.read_csv(path + str, delimiter=',')
    df['Date'] = pd.to_datetime(df['Date'])  
    df = df[['Date', 'Value']]
    df = df.set_index('Date')
    df = df.iloc[::-1] #Flip df to ascending order
    df.Value = df.apply(lambda x: (x-x.expanding().mean())/x.expanding().std())
    #df.ActualValue = sp.stats.zscore(df.ActualValue) #NOT EXPANDING WINDOW
    #If the indicator is inversely correlated to economic activity (i.e. Unemployment) Correct the correlation by multiplying by -1
    if (inverse_correlation=='TRUE'):
        df = df.multiply(-1)
    return df


#This function gets the data for an economic indicator, Raw, not normalized (For Int Rates, COT reports, etc)
def getIndicator(str):
    df = pd.read_csv(path + str, delimiter='\t')
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df = df[['Date', 'ActualValue']]
    df = df.set_index('Date')
    df = df.iloc[::-1] #Flip df to ascending order
    return df

#Function Takes all the Macro indicators in the list, and merges them into a single DataFrame, then averages all the normalized values
#into a single value (i.e. an average of economic health)
def createCountryHelix(list):
    merged = pd.DataFrame()
    #Loop through all the indicators from the list, call the getData on each indicator to retrieve and process/normalize the data
    for i in list:
        indicator = getData(i[0], i[1])
        #Add the normalized data from new indicator onto the DataFrame
        merged = pd.merge(merged, indicator, right_index=True, left_index=True, how = 'outer')
    merged = merged.ffill(axis=0) 
    average = merged.mean(axis=1)
    return average

def createGlobalAverage(economies):
    merged = pd.DataFrame()
    #Loop through all the indicators from the list, call the getData on each indicator to retrieve and process/normalize the data
    for country in economies:
        indicator = country
        #Add the normalized data from new indicator onto the DataFrame
        merged = pd.merge(merged, indicator.to_frame(), right_index=True, left_index=True, how = 'outer')
    merged = merged.ffill(axis=0) 
    average = merged.mean(axis=1)
    return average

#Country - Country2 (or global average)
def createIndexScore(country, country2):
    merged = pd.DataFrame()
    merged = pd.merge(country.to_frame(), country2.to_frame(), right_index=True, left_index=True, how = 'outer')
    merged = merged.ffill(axis=0) 
    differential = merged['0_x'] - merged['0_y']
    return differential

#These CSV files contain the list of macro economic indicators used for respective countries (where name corresponds to the raw file data in CSV_Data folder)
#fileListPath = '../MacroTraderFX/Indicator_Lists/'
fileListPath = 'Indicator_Lists/'
US_Files = np.genfromtxt(fileListPath + 'US_Files.csv', delimiter=',', dtype=str)
EU_Files = np.genfromtxt(fileListPath + 'EU_Files.csv', delimiter=',', dtype=str)
JP_Files = np.genfromtxt(fileListPath + 'JP_Files.csv', delimiter=',', dtype=str)
UK_Files = np.genfromtxt(fileListPath + 'UK_Files.csv', delimiter=',', dtype=str)
CA_Files = np.genfromtxt(fileListPath + 'CA_Files.csv', delimiter=',', dtype=str)
AU_Files = np.genfromtxt(fileListPath + 'AU_Files.csv', delimiter=',', dtype=str)
CH_Files = np.genfromtxt(fileListPath + 'CH_Files.csv', delimiter=',', dtype=str)
NZ_Files = np.genfromtxt(fileListPath + 'NZ_Files.csv', delimiter=',', dtype=str)


#Create super macro indicator for countries.
US = createCountryHelix(US_Files)   #United States
EU = createCountryHelix(EU_Files)   #European Union
JP = createCountryHelix(JP_Files)   #Japan
UK = createCountryHelix(UK_Files)   #United Kingdom
CA = createCountryHelix(CA_Files)   #Canada
AU = createCountryHelix(AU_Files)   #Australia
CH = createCountryHelix(CH_Files)   #Switzerland
NZ = createCountryHelix(NZ_Files)   #New Zealand

allEconomies = [US, EU, JP, UK, CA, AU, CH, NZ]


#Global Average
globalAverage = createGlobalAverage(allEconomies)


#Calculation for Economic Relative Global Strength Indexes (Country - globalAverage)
US_Index_Score = createIndexScore(US, globalAverage)
EU_Index_Score = createIndexScore(EU, globalAverage)
JP_Index_Score = createIndexScore(JP, globalAverage)
UK_Index_Score = createIndexScore(UK, globalAverage)
CA_Index_Score = createIndexScore(CA, globalAverage)
AU_Index_Score = createIndexScore(AU, globalAverage)
CH_Index_Score = createIndexScore(CH, globalAverage)
NZ_Index_Score = createIndexScore(NZ, globalAverage)

#Central Bank Interest Rates
#US_IntRate = getIndicator('united-states_fed-interest-rate-decision.csv')
#EU_IntRate = getIndicator('european-union_ecb-interest-rate-decision.csv')
#JP_IntRate = getIndicator('japan_boj-interest-rate-decision.csv')
#UK_IntRate = getIndicator('united-kingdom_boe-interest-rate-decision.csv')
#CA_IntRate = getIndicator('canada_boc-interest-rate-decision.csv')
#AU_IntRate = getIndicator('australia_rba-interest-rate-decision.csv')
#CH_IntRate = getIndicator('switzerland_snb-interest-rate-decision.csv')
#NZ_IntRate = getIndicator('new-zealand_rbnz-interest-rate-decision.csv')

#CFTC COT Reports (Commitment of Traders Reports)
#EUR_CFTC_COT = getIndicator('european-union_cftc-eur-non-commercial-net-positions.csv')
#JPY_CFTC_COT = getIndicator('japan_cftc-jpy-non-commercial-net-positions.csv')
#GBP_CFTC_COT = getIndicator('united-kingdom_cftc-gbp-non-commercial-net-positions.csv')
#CAD_CFTC_COT = getIndicator('canada_cftc-cad-non-commercial-net-positions.csv')
#AUD_CFTC_COT = getIndicator('australia_cftc-aud-non-commercial-net-positions.csv')
#CHF_CFTC_COT = getIndicator('switzerland_cftc-chf-non-commercial-net-positions.csv')
#NZD_CFTC_COT = getIndicator('new-zealand_cftc-nzd-non-commercial-net-positions.csv')


#FOR DASH PLOTS
#------------------------
#Baseline Macrofundamental Z-Score Index for Countries (Z-Score average of multiple economic indicators)
US_Macro = {'x': US.index, 'y': US, 'name': 'United States', 'marker': {'color': 'lime'}}
EU_Macro = {'x': EU.index, 'y': EU, 'name': 'Euro Area', 'marker': {'color': 'blue'}}
JP_Macro = {'x': JP.index, 'y': JP, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
UK_Macro = {'x': UK.index, 'y': UK, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
CA_Macro = {'x': CA.index, 'y': CA, 'name': 'Canada', 'marker': {'color': 'orange'}}
AU_Macro = {'x': AU.index, 'y': AU, 'name': 'Australia', 'marker': {'color': 'red'}}
CH_Macro = {'x': CH.index, 'y': CH, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
NZ_Macro = {'x': NZ.index, 'y': NZ, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}
GlobalAverage_Macro = {'x': globalAverage.index, 'y': globalAverage, 'name': 'Global Average', 'marker': {'color': 'black'}}

#Global Relative Strength Index (i.e. country - globalAverage)
US_Index = {'x': US_Index_Score.index, 'y': US_Index_Score, 'name': 'United States', 'marker': {'color': 'lime'}}
EU_Index = {'x': EU_Index_Score.index, 'y': EU_Index_Score, 'name': 'Euro Area', 'marker': {'color': 'blue'}}
JP_Index = {'x': JP_Index_Score.index, 'y': JP_Index_Score, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
UK_Index = {'x': UK_Index_Score.index, 'y': UK_Index_Score, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
CA_Index = {'x': CA_Index_Score.index, 'y': CA_Index_Score, 'name': 'Canada', 'marker': {'color': 'orange'}}
AU_Index = {'x': AU_Index_Score.index, 'y': AU_Index_Score, 'name': 'Australia', 'marker': {'color': 'red'}}
CH_Index = {'x': CH_Index_Score.index, 'y': CH_Index_Score, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
NZ_Index = {'x': NZ_Index_Score.index, 'y': NZ_Index_Score, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}

#Central Bank Interest Rates
#FED_IntRate = {'x': US_IntRate.index, 'y': US_IntRate.ActualValue, 'name': 'United States', 'marker': {'color': 'lime'}}
#ECB_IntRate = {'x': EU_IntRate.index, 'y': EU_IntRate.ActualValue, 'name': 'Euro Area', 'marker': {'color': 'blue'}}
#BOJ_IntRate = {'x': JP_IntRate.index, 'y': JP_IntRate.ActualValue, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
#BOE_IntRate = {'x': UK_IntRate.index, 'y': UK_IntRate.ActualValue, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
#BOC_IntRate = {'x': CA_IntRate.index, 'y': CA_IntRate.ActualValue, 'name': 'Canada', 'marker': {'color': 'orange'}}
#RBA_IntRate = {'x': AU_IntRate.index, 'y': AU_IntRate.ActualValue, 'name': 'Australia', 'marker': {'color': 'red'}}
#SNB_IntRate = {'x': CH_IntRate.index, 'y': CH_IntRate.ActualValue, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
#RBNZ_IntRate = {'x': NZ_IntRate.index, 'y': NZ_IntRate.ActualValue, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}

#CFTC COT Reports (Commitment of Traders)
#EUR_COT = {'x': EUR_CFTC_COT.index, 'y': EUR_CFTC_COT.ActualValue, 'name': 'EUR: COT Report', 'marker': {'color': 'blue'}}
#JPY_COT = {'x': JPY_CFTC_COT.index, 'y': JPY_CFTC_COT.ActualValue, 'name': 'JPY: COT Report', 'marker': {'color': 'fuchsia'}}
#GBP_COT = {'x': GBP_CFTC_COT.index, 'y': GBP_CFTC_COT.ActualValue, 'name': 'GBP: COT Report', 'marker': {'color': 'silver'}}
#CAD_COT = {'x': CAD_CFTC_COT.index, 'y': CAD_CFTC_COT.ActualValue, 'name': 'CAD: COT Report', 'marker': {'color': 'orange'}}
#AUD_COT = {'x': AUD_CFTC_COT.index, 'y': AUD_CFTC_COT.ActualValue, 'name': 'AUD: COT Report', 'marker': {'color': 'red'}}
#CHF_COT = {'x': CHF_CFTC_COT.index, 'y': CHF_CFTC_COT.ActualValue, 'name': 'CHF: COT Report', 'marker': {'color': 'yellow'}}
#NZD_COT = {'x': NZD_CFTC_COT.index, 'y': NZD_CFTC_COT.ActualValue, 'name': 'NZD: COT Report', 'marker': {'color': 'turquoise'}}

#TESTING NEW DATA
#US_TB = getNormalized('united-states_trade-balance.csv')
#EU_TB = getNormalized('european-union_trade-balance-nsa.csv')
#JP_TB = getNormalized('japan_trade-balance.csv')
#UK_TB = getNormalized('united-kingdom_trade-balance.csv')
#CA_TB = getNormalized('canada_trade-balance.csv')
#AU_TB = getNormalized('australia_trade-balance.csv')
#CH_TB = getNormalized('switzerland_trade-balance.csv')
#NZ_TB = getNormalized('new-zealand_trade-balance.csv')
#CN_TB = getNormalized('china_trade-balance.csv')

#Nation's TESTING NEW DATA
#US_TradeBalance = {'x': US_TB.index, 'y': US_TB.ActualValue, 'name': 'United States', 'marker': {'color': 'lime'}}
#EU_TradeBalance = {'x': EU_TB.index, 'y': EU_TB.ActualValue, 'name': 'Euro Area', 'marker': {'color': 'blue'}}
#JP_TradeBalance = {'x': JP_TB.index, 'y': JP_TB.ActualValue, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
#UK_TradeBalance = {'x': UK_TB.index, 'y': UK_TB.ActualValue, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
#CA_TradeBalance = {'x': CA_TB.index, 'y': CA_TB.ActualValue, 'name': 'Canada', 'marker': {'color': 'orange'}}
#AU_TradeBalance = {'x': AU_TB.index, 'y': AU_TB.ActualValue, 'name': 'Australia', 'marker': {'color': 'red'}}
#CH_TradeBalance = {'x': CH_TB.index, 'y': CH_TB.ActualValue, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
#NZ_TradeBalance = {'x': NZ_TB.index, 'y': NZ_TB.ActualValue, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}
#CN_TradeBalance = {'x': CN_TB.index, 'y': CN_TB.ActualValue, 'name': 'China', 'marker': {'color': 'tan'}}


#Importing currency data through Yahoo API
start = "2007-02-01"
#Function to get Currencies data
def getCurrencyPrice(str):
    currencyPrice = yf.download(str, interval='1d')
    return currencyPrice

#### TEMPLATE FOR CREATING Z INDEX FROM CURRENCIES
#Currency_Z = pd.DataFrame()
#Currency_Z = currency
#Currency_Z = Currency_Z.apply(lambda x: (x-x.rolling(200).mean())/x.rolling(200).std())

