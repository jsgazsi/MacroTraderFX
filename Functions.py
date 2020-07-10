import Macro
import plotly.graph_objects as go 
import pandas as pd


#graph_height = 200
#---------------------------
#Functions for App Callbacks
#---------------------------
graph_height = 750
currency_color = {'color': 'black'}

all_options = {
    #Country Macroeconomic Z-Score
    'US_Macro': Macro.US_Macro,
    'EU_Macro': Macro.EU_Macro,
    'JP_Macro': Macro.JP_Macro,
    'UK_Macro': Macro.UK_Macro,
    'CA_Macro': Macro.CA_Macro,
    'AU_Macro': Macro.AU_Macro,
    'CH_Macro': Macro.CH_Macro,
    'NZ_Macro': Macro.NZ_Macro,
    'CN_Macro': Macro.CN_Macro,
    'Global_Average': Macro.GlobalAverage_Macro,
    #Indexes (i.e. country vs global average)
    'US_Index': Macro.US_Index,
    'EU_Index': Macro.EU_Index,
    'JP_Index': Macro.JP_Index,
    'UK_Index': Macro.UK_Index,
    'CA_Index': Macro.CA_Index,
    'AU_Index': Macro.AU_Index,
    'CH_Index': Macro.CH_Index,
    'NZ_Index': Macro.NZ_Index,
    'CN_Index': Macro.CN_Index,
    #Interest Rates
    'FED': Macro.FED_IntRate,
    'ECB': Macro.ECB_IntRate,
    'BOJ': Macro.BOJ_IntRate,
    'BOE': Macro.BOE_IntRate,
    'BOC': Macro.BOC_IntRate,
    'RBA': Macro.RBA_IntRate,
    'SNB': Macro.SNB_IntRate,
    'RBNZ': Macro.RBNZ_IntRate,
    #CFTC - COT Reports
    'EUR_COT': Macro.EUR_COT,
    'JPY_COT': Macro.JPY_COT,
    'GBP_COT': Macro.GBP_COT,
    'CAD_COT': Macro.CAD_COT,
    'AUD_COT': Macro.AUD_COT,
    'NZD_COT': Macro.NZD_COT,
    'CHF_COT': Macro.CHF_COT,   
}



def updateMacroScore(input_value):
    traces = []
    selected_plot = input_value
    
    for input_value in selected_plot:
        traces.append(dict(
            x = all_options[input_value]['x'],
            y = all_options[input_value]['y'],
            mode='lines',
            name= all_options[input_value]['name'],
            marker = all_options[input_value]['marker']
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            dragmode='pan',
            height= graph_height
        )
    }     

def updateMacroIndex(input_value):
    traces = []
    selected_plot = input_value
    
    for input_value in selected_plot:
        traces.append(dict(
            x = all_options[input_value]['x'],
            y = all_options[input_value]['y'],
            mode='lines',
            name= all_options[input_value]['name'],
            marker = all_options[input_value]['marker']
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            dragmode='pan', 
            height= graph_height, 
        )
    }    

def updateMacroDifferential(input_value):
    traces = []

    subStr = input_value.split('/')
    base = subStr[0]
    quote = subStr[1]

    if (base == 'USD'):
        econBase = Macro.US_Index
    elif (base == 'EUR'):
        econBase = Macro.EU_Index
    elif(base == 'GBP'):
        econBase = Macro.UK_Index
    elif(base == 'CAD'):
        econBase = Macro.CA_Index
    elif(base == 'AUD'):
        econBase = Macro.AU_Index
    elif(base == 'CHF'):
        econBase = Macro.CH_Index
    elif(base == 'NZD'):
        econBase = Macro.NZ_Index
    elif(base == 'CNH'):
        econBase = Macro.CN_Index

    if (quote == 'USD'):
        econQuote = Macro.US_Index
    elif (quote == 'JPY'):
        econQuote = Macro.JP_Index
    elif (quote == 'GBP'):
        econQuote = Macro.UK_Index
    elif (quote == 'CAD'):
        econQuote = Macro.CA_Index
    elif (quote == 'AUD'):
        econQuote = Macro.AU_Index
    elif (quote == 'CHF'):
        econQuote = Macro.CH_Index
    elif (quote == 'NZD'):
        econQuote = Macro.NZ_Index
    elif (quote == 'CNH'):
        econQuote = Macro.CN_Index


    differential = Macro.createIndexScore(econBase['y'], econQuote['y'])
    name = econBase['name'] + " VS " + econQuote['name'] + " Fundamentals"
    marker = econBase['marker']
    currency = Macro.getCurrencyPrice(base + quote + '=X')
    currencyName = input_value + " Price"
    #Manually Drop previous extreme obviously erronious values from yFinance API
    if(input_value == 'EUR/USD'):
        currency = currency.drop(pd.to_datetime(['2008-03-17', '2012-01-27']))

    #Fundamentals Trace
    traces.append(dict(
        x = differential.index,
        y = differential,
        mode='lines',
        name= name,
        marker = marker,   
        )
    )    

    #Currency Trace
    traces.append(dict(
        type= 'candlestick',
        x = currency.index,
        #y = currency['Close'],
        #mode= 'lines',
        open = currency.Open,
        high = currency.High,
        low = currency.Low,
        close = currency.Close,
        name= currencyName,
        #marker = currency_color,
        yaxis= 'y2',
          
        )
    )
    
    #return traces
    return {
        'data': traces,
        'layout': go.Layout(
            dragmode='pan', 
            height= graph_height,
            xaxis_rangeslider_visible=False,
            hovermode= False,
            yaxis2=dict(
                overlaying= 'y',
                side= "right",
            ),
        )
    }    

def updateCOT_Report(input_value):
    traces = []
    selected_plot = input_value
    
    for input_value in selected_plot:
        traces.append(dict(
            x = all_options[input_value]['x'],
            y = all_options[input_value]['y'],
            mode='lines',
            name= all_options[input_value]['name'],
            marker = all_options[input_value]['marker']
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            dragmode='pan',
            height= graph_height, 
        )
    }    

def updateTradeBalance(input_value):
    traces = []
    selected_plot = input_value
    
    for input_value in selected_plot:
        traces.append(dict(
            x = all_options[input_value]['x'],
            y = all_options[input_value]['y'],
            mode='lines',
            name= all_options[input_value]['name'],
            marker = all_options[input_value]['marker']
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            dragmode='pan',
            height= graph_height, 
        )
    }    

def updateInterestRates(input_value):
    traces = []
    selected_plot = input_value
    
    for input_value in selected_plot:
        traces.append(dict(
            x = all_options[input_value]['x'],
            y = all_options[input_value]['y'],
            mode='lines',
            name= all_options[input_value]['name'],
            marker = all_options[input_value]['marker']
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            dragmode='pan',
            height= graph_height, 
        )
    }    