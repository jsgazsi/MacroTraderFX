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


#Macro Trader Test
#import Macro_CSV_Lists

#path = "../MacroTraderFX/CSV_Data/"
path = 'CSV_Data/'
#This function gets the data for an economic indicator (e.g. GDP, Unemployment), and normalizes the data to it's Standard Score (Z-Score))
def getData(str, inverse_correlation):
    #read in CSV data
    df = pd.read_csv(path + str, delimiter='\t')
    #Convert to datetime, then to period, then timestamp to get year and month only that is plottable
    # -- df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp().dt.strftime('%Y-%m') --Old method 
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m')
    #Set DataFrame to desired columns
    df = df[['Date', 'ActualValue']]
    #Keep only most recent date and data point for month, i.e. account for revisions, the new revised number overwrites the previous value for the month
    df.drop_duplicates(subset ="Date", keep = "first", inplace = True) 
    #Set the Date as the index
    df = df.set_index('Date')
    #Calculate zScore - This normalizes all the values for comparison
    df.ActualValue = sp.stats.zscore(df.ActualValue)
    #If the indicator is inversely correlated to economic activity (i.e. Unemployment) Correct the correlation by multiplying by -1
    if (inverse_correlation=='TRUE' or inverse_correlation =='True'):
        df = df.multiply(-1)
    #Create Dataframe
    return df

#This function gets the data for an economic indicator, Raw, not normalized (For Int Rates, COT reports, etc)
def getIndicator(str):
    #read in CSV data
    df = pd.read_csv(path + str, delimiter='\t')
    #Convert to datetime
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    #Set DataFrame to desired columns
    df = df[['Date', 'ActualValue']]
    #Set the Date as the index
    df = df.set_index('Date')
    return df

#Function Takes all the Macro indicators in the list, and merges them into a single DataFrame, then averages all the normalized values
#into a single value (i.e. an average of economic health)
def createCountryHelix(list):
    #create blank DataFrame to hold contents
    merged = pd.DataFrame()
    #Loop through all the indicators from the list, call the getData on each indicator to retrieve and process/normalize the data
    for i in list:
        indicator = getData(i[0], i[1])
        #Add the normalized data from new indicator onto the DataFrame
        merged = pd.merge(merged, indicator, right_index=True, left_index=True, how = 'outer')
    #Some months may be skipped in the data. Forward fill the data so that the previous month's value is retained until a new value is populated
    #This also keeps this current months date peroid populated with lasts month's data until we get this month's economic release of that figure
    merged = merged.ffill(axis=0)
    #Average all normalized indicators. Forward fill ensures current month's rolling average is based on all most recent data for all indicators
    average = merged.mean(axis=1)
    return average



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
CN_Files = np.genfromtxt(fileListPath + 'CN_Files.csv', delimiter=',', dtype=str)

#Create super macro indicator for countries.
US = createCountryHelix(US_Files)   #United States
EU = createCountryHelix(EU_Files)   #European Union
JP = createCountryHelix(JP_Files)   #Japan
UK = createCountryHelix(UK_Files)   #United Kingdom
CA = createCountryHelix(CA_Files)   #Canada
AU = createCountryHelix(AU_Files)   #Australia
CH = createCountryHelix(CH_Files)   #Switzerland
NZ = createCountryHelix(NZ_Files)   #New Zealand
CN = createCountryHelix(CN_Files)   #China


#Global Average
numberOfEconomies = 6
globalAverage = ((US + EU + JP + UK + CA + AU) / numberOfEconomies)


#Calculation for Economic Relative Global Strength Indexes
US_Index_Score = US - globalAverage
EU_Index_Score = EU - globalAverage
JP_Index_Score = JP - globalAverage
UK_Index_Score = UK - globalAverage
CA_Index_Score = CA - globalAverage
AU_Index_Score = AU - globalAverage
CH_Index_Score = CH - globalAverage
NZ_Index_Score = NZ - globalAverage
CN_Index_Score = CN - globalAverage

#Central Bank Interest Rates
US_IntRate = getIndicator('united-states_fed-interest-rate-decision.csv')
EU_IntRate = getIndicator('european-union_ecb-interest-rate-decision.csv')
JP_IntRate = getIndicator('japan_boj-interest-rate-decision.csv')
UK_IntRate = getIndicator('united-kingdom_boe-interest-rate-decision.csv')
CA_IntRate = getIndicator('canada_boc-interest-rate-decision.csv')
AU_IntRate = getIndicator('australia_rba-interest-rate-decision.csv')
CH_IntRate = getIndicator('switzerland_snb-interest-rate-decision.csv')
NZ_IntRate = getIndicator('new-zealand_rbnz-interest-rate-decision.csv')

#Trade Balances
US_TB = getIndicator('united-states_trade-balance.csv')
EU_TB = getIndicator('european-union_trade-balance-nsa.csv')
JP_TB = getIndicator('japan_trade-balance.csv')
UK_TB = getIndicator('united-kingdom_trade-balance.csv')
CA_TB = getIndicator('canada_trade-balance.csv')
AU_TB = getIndicator('australia_trade-balance.csv')
CH_TB = getIndicator('switzerland_trade-balance.csv')
NZ_TB = getIndicator('new-zealand_trade-balance.csv')
CN_TB = getIndicator('china_trade-balance.csv')

#CFTC COT Reports (Commitment of Traders Reports)
EUR_CFTC_COT = getIndicator('european-union_cftc-eur-non-commercial-net-positions.csv')
JPY_CFTC_COT = getIndicator('japan_cftc-jpy-non-commercial-net-positions.csv')
GBP_CFTC_COT = getIndicator('united-kingdom_cftc-gbp-non-commercial-net-positions.csv')
CAD_CFTC_COT = getIndicator('canada_cftc-cad-non-commercial-net-positions.csv')
AUD_CFTC_COT = getIndicator('australia_cftc-aud-non-commercial-net-positions.csv')
CHF_CFTC_COT = getIndicator('switzerland_cftc-chf-non-commercial-net-positions.csv')
NZD_CFTC_COT = getIndicator('new-zealand_cftc-nzd-non-commercial-net-positions.csv')


#FOR DASH PLOTS
#------------------------
#Baseline Macrofundamental Z-Score Index for Countries (Z-Score average of multiple economic indicators)
US_Macro = {'x': US.index, 'y': US, 'name': 'United States', 'marker': {'color': 'lime'}}
EU_Macro = {'x': EU.index, 'y': EU, 'name': 'European Union', 'marker': {'color': 'blue'}}
JP_Macro = {'x': JP.index, 'y': JP, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
UK_Macro = {'x': UK.index, 'y': UK, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
CA_Macro = {'x': CA.index, 'y': CA, 'name': 'Canada', 'marker': {'color': 'orange'}}
AU_Macro = {'x': AU.index, 'y': AU, 'name': 'Australia', 'marker': {'color': 'red'}}
CH_Macro = {'x': CH.index, 'y': CH, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
NZ_Macro = {'x': NZ.index, 'y': NZ, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}
CN_Macro = {'x': CN.index, 'y': CN, 'name': 'China', 'marker': {'color': 'tan'}}

#Global Relative Strength Index (i.e. country - globalAverage)
US_Index = {'x': US_Index_Score.index, 'y': US_Index_Score, 'name': 'United States', 'marker': {'color': 'lime'}}
EU_Index = {'x': EU_Index_Score.index, 'y': EU_Index_Score, 'name': 'European Union', 'marker': {'color': 'blue'}}
JP_Index = {'x': JP_Index_Score.index, 'y': JP_Index_Score, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
UK_Index = {'x': UK_Index_Score.index, 'y': UK_Index_Score, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
CA_Index = {'x': CA_Index_Score.index, 'y': CA_Index_Score, 'name': 'Canada', 'marker': {'color': 'orange'}}
AU_Index = {'x': AU_Index_Score.index, 'y': AU_Index_Score, 'name': 'Australia', 'marker': {'color': 'red'}}
CH_Index = {'x': CH_Index_Score.index, 'y': CH_Index_Score, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
NZ_Index = {'x': NZ_Index_Score.index, 'y': NZ_Index_Score, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}
CN_Index = {'x': CN_Index_Score.index, 'y': CN_Index_Score, 'name': 'China', 'marker': {'color': 'tan'}}

#Central Bank Interest Rates
FED_IntRate = {'x': US_IntRate.index, 'y': US_IntRate.ActualValue, 'name': 'United States', 'marker': {'color': 'lime'}}
ECB_IntRate = {'x': EU_IntRate.index, 'y': EU_IntRate.ActualValue, 'name': 'European Union', 'marker': {'color': 'blue'}}
BOJ_IntRate = {'x': JP_IntRate.index, 'y': JP_IntRate.ActualValue, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
BOE_IntRate = {'x': UK_IntRate.index, 'y': UK_IntRate.ActualValue, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
BOC_IntRate = {'x': CA_IntRate.index, 'y': CA_IntRate.ActualValue, 'name': 'Canada', 'marker': {'color': 'orange'}}
RBA_IntRate = {'x': AU_IntRate.index, 'y': AU_IntRate.ActualValue, 'name': 'Australia', 'marker': {'color': 'red'}}
SNB_IntRate = {'x': CH_IntRate.index, 'y': CH_IntRate.ActualValue, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
RBNZ_IntRate = {'x': NZ_IntRate.index, 'y': NZ_IntRate.ActualValue, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}

#Nation's Trade Balances
US_TradeBalance = {'x': US_TB.index, 'y': US_TB, 'name': 'United States', 'marker': {'color': 'lime'}}
EU_TradeBalance = {'x': EU_TB.index, 'y': EU_TB, 'name': 'European Union', 'marker': {'color': 'blue'}}
JP_TradeBalance = {'x': JP_TB.index, 'y': JP_TB, 'name': 'Japan', 'marker': {'color': 'fuchsia'}}
UK_TradeBalance = {'x': UK_TB.index, 'y': UK_TB, 'name': 'United Kingdom', 'marker': {'color': 'silver'}}
CA_TradeBalance = {'x': CA_TB.index, 'y': CA_TB, 'name': 'Canada', 'marker': {'color': 'orange'}}
AU_TradeBalance = {'x': AU_TB.index, 'y': AU_TB, 'name': 'Australia', 'marker': {'color': 'red'}}
CH_TradeBalance = {'x': CH_TB.index, 'y': CH_TB, 'name': 'Switzerland', 'marker': {'color': 'yellow'}}
NZ_TradeBalance = {'x': NZ_TB.index, 'y': NZ_TB, 'name': 'New Zealand', 'marker': {'color': 'turquoise'}}
CN_TradeBalance = {'x': CN_TB.index, 'y': CN_TB, 'name': 'China', 'marker': {'color': 'tan'}}

#CFTC COT Reports (Commitment of Traders)
EUR_COT = {'x': EUR_CFTC_COT.index, 'y': EUR_CFTC_COT.ActualValue, 'name': 'EUR: COT Report', 'marker': {'color': 'blue'}}
JPY_COT = {'x': JPY_CFTC_COT.index, 'y': JPY_CFTC_COT.ActualValue, 'name': 'JPY: COT Report', 'marker': {'color': 'fuchsia'}}
GBP_COT = {'x': GBP_CFTC_COT.index, 'y': GBP_CFTC_COT.ActualValue, 'name': 'GBP: COT Report', 'marker': {'color': 'silver'}}
CAD_COT = {'x': CAD_CFTC_COT.index, 'y': CAD_CFTC_COT.ActualValue, 'name': 'CAD: COT Report', 'marker': {'color': 'orange'}}
AUD_COT = {'x': AUD_CFTC_COT.index, 'y': AUD_CFTC_COT.ActualValue, 'name': 'AUD: COT Report', 'marker': {'color': 'red'}}
CHF_COT = {'x': CHF_CFTC_COT.index, 'y': CHF_CFTC_COT.ActualValue, 'name': 'CHF: COT Report', 'marker': {'color': 'yellow'}}
NZD_COT = {'x': NZD_CFTC_COT.index, 'y': NZD_CFTC_COT.ActualValue, 'name': 'NZD: COT Report', 'marker': {'color': 'turquoise'}}



#Importing currency data through Yahoo API
start = "2007-02-01"
#Function to get Currencies data
def getCurrencyPrice(str):
    currencyPrice = yf.download(str, start, interval='1wk')
    return currencyPrice

#TODO: FOR FUTURE DOWNLOADING INTO CSV FILES
#Currencies
#usdcad = getCurrencyPrice('CAD=X')
#usdjpy = getCurrencyPrice('JPY=X')
#usdchf = getCurrencyPrice('CHF=X')
#usdcny = getCurrencyPrice('CNY=X')
#eurusd = getCurrencyPrice('EURUSD=X')
#euraud = getCurrencyPrice('EURAUD=X')
#eurcad = getCurrencyPrice('EURCAD=X')
#eurjpy = getCurrencyPrice('EURJPY=x')
#eurgbp = getCurrencyPrice('EURGBP=X')
#eurchf = getCurrencyPrice('EURCHF=X')
#eurnzd = getCurrencyPrice('EURNZD=X')
#eurcny = getCurrencyPrice('EURCNY=X')
#audusd = getCurrencyPrice('AUDUSD=X')
#audcad = getCurrencyPrice('AUDCAD=X')
#audjpy = getCurrencyPrice('AUDJPY=X')
#audchf = getCurrencyPrice('AUDCHF=X')
#audnzd = getCurrencyPrice('AUDNZD=X')
#audcny = getCurrencyPrice('AUDCNY=X')
#gbpaud = getCurrencyPrice('GBPAUD=X')
#gbpcad = getCurrencyPrice('GBPCAD=X')
#gbpjpy = getCurrencyPrice('GBPJPY=X')
#gbpusd = getCurrencyPrice('GBPUSD=X')
#gbpchf = getCurrencyPrice('GBPCHF=X')
#gbpnzd = getCurrencyPrice('GBPNZD=X')
#gbpcny = getCurrencyPrice('GBPCNY=X')
#cadjpy = getCurrencyPrice('CADJPY=X')
#cadchf = getCurrencyPrice('CADCHF=X')
#cadcny = getCurrencyPrice('CADCNY=X')
#chfjpy = getCurrencyPrice('CHFJPY=X')
#chfcny = getCurrencyPrice('CHFCNY=X')
#nzdusd = getCurrencyPrice('NZDUSD=X')
#nzdjpy = getCurrencyPrice('NZDJPY=X')
#nzdcad = getCurrencyPrice('NZDCAD=X')
#nzdchf = getCurrencyPrice('NZDCHF=X')
#nzdcny = getCurrencyPrice('NZDCNY=X')
#cnyjpy = getCurrencyPrice('CNYJPY=X')

#Currency Plots         ***NOT NEEDED?***
#USDCAD = {'x': usdcad.index, 'y': usdcad, 'name':'USD/CAD'}
#USDJPY = {'x': usdjpy.index, 'y': usdjpy, 'name':'USD/JPY'}
#USDCHF = {'x': usdchf.index, 'y': usdchf, 'name':'USD/CHF'}
#EURUSD = {'x': eurusd.index, 'y': eurusd, 'name':'EUR/USD'}
#EURAUD = {'x': euraud.index, 'y': euraud, 'name':'EUR/AUD'}
#EURCAD = {'x': eurcad.index, 'y': eurcad, 'name':'EUR/CAD'}
#EURJPY = {'x': eurjpy.index, 'y': eurjpy, 'name':'EUR/JPY'}
#EURGBP = {'x': eurgbp.index, 'y': eurgbp, 'name':'EUR/GBP'}
#EURCHF = {'x': eurchf.index, 'y': eurchf, 'name':'EUR/CHF'}
#EURNZD = {'x': eurnzd.index, 'y': eurnzd, 'name':'EUR/NZD'}
#AUDUSD = {'x': audusd.index, 'y': audusd, 'name':'AUD/USD'}
#AUDCAD = {'x': audcad.index, 'y': audcad, 'name':'AUD/CAD'}
#AUDJPY = {'x': audjpy.index, 'y': audjpy, 'name':'AUD/JPY'}
#AUDCHF = {'x': audchf.index, 'y': audchf, 'name':'AUD/CHF'}
#AUDNZD = {'x': audnzd.index, 'y': audnzd, 'name':'AUD/NZD'}
#GBPAUD = {'x': gbpaud.index, 'y': gbpaud, 'name':'GBP/AUD'}
#GBPCAD = {'x': gbpcad.index, 'y': gbpcad, 'name':'GBP/CAD'}
#GBPJPY = {'x': gbpjpy.index, 'y': gbpjpy, 'name':'GBP/JPY'}
#GBPUSD = {'x': gbpusd.index, 'y': gbpusd, 'name':'GBP/USD'}
#GBPCHF = {'x': gbpchf.index, 'y': gbpchf, 'name':'GBP/CHF'}
#GBPNZD = {'x': gbpnzd.index, 'y': gbpnzd, 'name':'GBP/NZD'}
#CADJPY = {'x': cadjpy.index, 'y': cadjpy, 'name':'CAD/JPY'}
#CADCHF = {'x': cadchf.index, 'y': cadchf, 'name':'CAD/CHF'}
#CHFJPY = {'x': chfjpy.index, 'y': chfjpy, 'name':'CHF/JPY'}
#NZDJPY = {'x': nzdjpy.index, 'y': nzdjpy, 'name':'NZD/JPY'}
#NZDUSD = {'x': nzdusd.index, 'y': nzdusd, 'name':'NZD/USD'}
#NZDCAD = {'x': nzdcad.index, 'y': nzdcad, 'name':'NZD/CAD'}
#NZDCHF = {'x': nzdchf.index, 'y': nzdchf, 'name':'NZD/CHF'}



