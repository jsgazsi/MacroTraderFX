import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go 
import Macro


#MacroTrader Testing a change , yet another change

app = dash.Dash(__name__)
server = app.server

app.title = 'MacroTrader'

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
    'EUR (Euro)': Macro.EUR_COT,
    'JPY (Japanese Yen)': Macro.JPY_COT,
    'GBP (British Pound)': Macro.GBP_COT,
    'CAD (Canadian Dollar)': Macro.CAD_COT,
    'AUD (Australian Dollar': Macro.AUD_COT,
    'NZD (New Zealand Dollar': Macro.NZD_COT,
    'CHF (Swiss Franc)': Macro.CHF_COT,    
}

graph_height = 600
currency_color = {'color': 'black'}

#for option in all_options:
#    print(all_options[option])

app.layout = html.Div([
    #Header
    html.H1(
    children='MacroTrader',
    style={
        'font-size': '250%',
        'textAlign': 'center',
        'color': '#7FDBFF'}
    ),

    #Header
    html.H1(
    children='Global Economies',
    style={
        'font-size': '175%',
        'textAlign': 'center',
        'color': '#7FDBFF'}
    ),

    #General Macro Z-Score Section
    html.Label('Macroeconomic Z-Scores'),
    dcc.Dropdown(id='Dropdown_1', style={'width': '100%'},
        options=[
            {'label': 'United States', 'value': 'US_Macro'},
            {'label': 'European Union', 'value': 'EU_Macro'},
            {'label': 'Japan', 'value': 'JP_Macro'},
            {'label': 'United Kingdom', 'value': 'UK_Macro'},
            {'label': 'Canada', 'value': 'CA_Macro'},
            {'label': 'Australia', 'value': 'AU_Macro'},
            {'label': 'Switzerland', 'value': 'CH_Macro'},
            {'label': 'New Zealand', 'value': 'NZ_Macro'},
            {'label': 'China', 'value': 'CN_Macro'},
        ],
        value = ['US_Macro', 'EU_Macro'],
        multi = True
    ),
    dcc.Graph(id='Graph1', config={'scrollZoom': True}),

    #Macro Indexes Section (Country VS. Rest of World Global Avg.)
    html.Label('Macro Index (i.e. Country vs Global Average)'),
    dcc.Dropdown(id='Dropdown_2', style={'width': '100%'},
        options=[
            {'label': 'United States', 'value': 'US_Index'},
            {'label': 'European Union', 'value': 'EU_Index'},
            {'label': 'Japan', 'value': 'JP_Index'},
            {'label': 'United Kingdom', 'value': 'UK_Index'},
            {'label': 'Canada', 'value': 'CA_Index'},
            {'label': 'Australia', 'value': 'AU_Index'},
            {'label': 'Switzerland', 'value': 'CH_Index'},
            {'label': 'New Zealand', 'value': 'NZ_Index'},
            {'label': 'China', 'value': 'CN_Index'},
        ],
        value = ['US_Index', 'EU_Index'],
        multi = True
    ),
    dcc.Graph(id='Graph2', config={'scrollZoom': True}),

    #Individual Economony Comparision with Currency Prices Section
    html.Div([html.Label('Economy Differentials')]),
    dcc.Dropdown(id='Dropdown_3_Left', style={'display': 'inline-block', 'width': '51%'},
        options=[
            {'label': 'United States', 'value': 'US_Index'},
            {'label': 'European Union', 'value': 'EU_Index'},
            {'label': 'Japan', 'value': 'JP_Index'},
            {'label': 'United Kingdom', 'value': 'UK_Index'},
            {'label': 'Canada', 'value': 'CA_Index'},
            {'label': 'Australia', 'value': 'AU_Index'},
            {'label': 'Switzerland', 'value': 'CH_Index'},
            {'label': 'New Zealand', 'value': 'NZ_Index'},
            {'label': 'China', 'value': 'CN_Index'},
        ],
        value = 'US_Index',
    ),
    dcc.Dropdown(id='Dropdown_3_Right',style={'display': 'inline-block', 'width': '51%'},
        options=[
            {'label': 'United States', 'value': 'US_Index'},
            {'label': 'European Union', 'value': 'EU_Index'},
            {'label': 'Japan', 'value': 'JP_Index'},
            {'label': 'United Kingdom', 'value': 'UK_Index'},
            {'label': 'Canada', 'value': 'CA_Index'},
            {'label': 'Australia', 'value': 'AU_Index'},
            {'label': 'Switzerland', 'value': 'CH_Index'},
            {'label': 'New Zealand', 'value': 'NZ_Index'},
            {'label': 'China', 'value': 'CN_Index'},
        ],
        value = 'EU_Index',
    ),
    dcc.Checklist(id='CurrencyInverse',
        options=[
            {'label': 'Currency Inverse', 'value': 'inverse'},
        ],  
    ),  
    dcc.Graph(id='Graph3', config={'scrollZoom': True}),

    #Interest Rates Section
    html.Label('Central Bank Interest Rates'),
    dcc.Dropdown(id='Dropdown_IntRates', style={'width': '100%'},
        options=[
            {'label': 'Federal Reserve (USD)', 'value': 'FED'},
            {'label': 'European Central Bank (EUR)', 'value': 'ECB'},
            {'label': 'Bank of Japan (JPY)', 'value': 'BOJ'},
            {'label': 'Bank of England (GBP)', 'value': 'BOE'},
            {'label': 'Bank of Canada (CAD)', 'value': 'BOC'},
            {'label': 'Royal Bank of Australia (AUD)', 'value': 'RBA'},
            {'label': 'Swiss National Bank (CHF)', 'value': 'SNB'},
            {'label': 'Royal Bank of New Zealand (NZD)', 'value': 'RBNZ'},
        ],
        value = ['FED', 'ECB', 'BOJ', 'BOE', 'BOC', 'RBA', 'SNB', 'RBNZ'],
        multi = True
    ),
    dcc.Graph(id='Graph_IntRates', config={'scrollZoom': True}),
  
])

#Callback for Graph1, Macroeconomic Z-Scores
@app.callback(
    Output(component_id='Graph1', component_property='figure'),
    [Input(component_id='Dropdown_1', component_property= 'value')]
)
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
            height= graph_height, 
        )
    }     


#Callback for Graph2, Macroeconomic indexes (i.e. Country vs Global Average)
@app.callback(
    Output(component_id='Graph2', component_property='figure'),
    [Input(component_id='Dropdown_2', component_property= 'value')]
)
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


#Callback for Macro Index Differential, (One on One comparision)
@app.callback(
    Output(component_id='Graph3', component_property='figure'),
    [Input(component_id='Dropdown_3_Left', component_property= 'value'),
    Input(component_id='Dropdown_3_Right', component_property= 'value'),
    Input(component_id='CurrencyInverse', component_property= 'value')]
)
def updateMacroDifferential(input_value, input_value2, checkbox):
    traces = []
    #for input_value in selected_plot:
    traces.append(dict(
        x = all_options[input_value]['x'],
        y = all_options[input_value]['y'] - all_options[input_value2]['y'],
        mode='lines',
        name= all_options[input_value]['name'],
        marker = all_options[input_value]['marker'],   
        )
    )
    traces.append(dict(
        x = all_options[input_value2]['x'],
        y = all_options[input_value2]['y'] - all_options[input_value]['y'],
        mode='lines',
        name= all_options[input_value2]['name'],
        marker = all_options[input_value2]['marker'],
        )
    )
    
    
    #Logic to auto populate correct currency to graph
    if (input_value == 'US_Index' or input_value == 'CA_Index') and (input_value2 == 'US_Index' or input_value2 == 'CA_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CAD=X')
            name = 'USD/CAD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CADUSD=X')
            name = 'CAD/USD'
    if (input_value == 'US_Index' or input_value == 'JP_Index') and (input_value2 == 'US_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('JPY=X')
            name = 'USD/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYUSD=X')
            name = 'JPY/USD'
    if (input_value == 'US_Index' or input_value == 'CH_Index') and (input_value2 == 'US_Index' or input_value2 == 'CH_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CHF=X')
            name = 'USD/CHF'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CHFUSD=X')
            name = 'CHF/USD'
    if (input_value == 'US_Index' or input_value == 'CN_Index') and (input_value2 == 'US_Index' or input_value2 == 'CN_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CNY=X')
            name = 'USD/CNY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CNYUSD=X')
            name = 'CNY/USD'
    if (input_value == 'EU_Index' or input_value == 'US_Index') and (input_value2 == 'EU_Index' or input_value2 == 'US_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURUSD=X')
            name = 'EUR/USD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('EUR=X')
            name = 'USD/EUR'
    if (input_value == 'EU_Index' or input_value == 'AU_Index') and (input_value2 == 'EU_Index' or input_value2 == 'AU_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURAUD=X')
            name = 'EUR/AUD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('AUDEUR=X')
            name = 'AUD/EUR'
    if (input_value == 'EU_Index' or input_value == 'CA_Index') and (input_value2 == 'EU_Index' or input_value2 == 'CA_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURCAD=X')
            name = 'EUR/CAD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CADEUR=X')
            name = 'CAD/EUR'
    if (input_value == 'EU_Index' or input_value == 'JP_Index') and (input_value2 == 'EU_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURJPY=X')
            name = 'EUR/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYEUR=X')
            name = 'JPY/EUR'
    if (input_value == 'EU_Index' or input_value == 'UK_Index') and (input_value2 == 'EU_Index' or input_value2 == 'UK_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURGBP=X')
            name = 'EUR/GBP'
        else: #if inverse
            currency = Macro.getCurrencyPrice('GBPEUR=X')
            name = 'GBP/EUR'
    if (input_value == 'EU_Index' or input_value == 'CH_Index') and (input_value2 == 'EU_Index' or input_value2 == 'CH_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURCHF=X')
            name = 'EUR/CHF'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CHFEUR=X')
            name = 'CHF/EUR'
    if (input_value == 'EU_Index' or input_value == 'NZ_Index') and (input_value2 == 'EU_Index' or input_value2 == 'NZ_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURNZD=X')
            name = 'EUR/NZD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('NZDEUR=X')
            name = 'NZD/EUR'
    if (input_value == 'EU_Index' or input_value == 'CN_Index') and (input_value2 == 'EU_Index' or input_value2 == 'CN_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('EURCNY=X')
            name = 'EUR/CNY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CNYEUR=X')
            name = 'CNY/EUR'
    elif (input_value == 'AU_Index' or input_value == 'US_Index') and (input_value2 == 'AU_Index' or input_value2 == 'US_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('AUDUSD=X')
            name = 'AUD/USD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('AUD=X')
            name = 'USD/AUD'
    elif (input_value == 'AU_Index' or input_value == 'CA_Index') and (input_value2 == 'AU_Index' or input_value2 == 'CA_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('AUDCAD=X')
            name = 'AUD/CAD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CADAUD=X')
            name = 'CAD/AUD'
    elif (input_value == 'AU_Index' or input_value == 'JP_Index') and (input_value2 == 'AU_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('AUDJPY=X')
            name = 'AUD/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYAUD=X')
            name = 'JPY/AUD'
    elif (input_value == 'AU_Index' or input_value == 'CH_Index') and (input_value2 == 'AU_Index' or input_value2 == 'CH_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('AUDCHF=X')
            name = 'AUD/CHF'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CHFAUD=X')
            name = 'CHF/AUD'
    elif (input_value == 'AU_Index' or input_value == 'NZ_Index') and (input_value2 == 'AU_Index' or input_value2 == 'NZ_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('AUDNZD=X')
            name = 'AUD/NZD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('NZDAUD=X')
            name = 'NZD/AUD'
    elif (input_value == 'AU_Index' or input_value == 'CN_Index') and (input_value2 == 'AU_Index' or input_value2 == 'CN_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('AUDCNY=X')
            name = 'AUD/CNY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CNYAUD=X')
            name = 'CNY/AUD'
    elif (input_value == 'UK_Index' or input_value == 'AU_Index') and (input_value2 == 'UK_Index' or input_value2 == 'AU_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('GBPAUD=X')
            name = 'GBP/AUD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('AUDGBP=X')
            name = 'AUD/GBP'
    elif (input_value == 'UK_Index' or input_value == 'CA_Index') and (input_value2 == 'UK_Index' or input_value2 == 'CA_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('GBPCAD=X')
            name = 'GBP/CAD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CADGBP=X')
            name = 'CAD/GBP'
    elif (input_value == 'UK_Index' or input_value == 'JP_Index') and (input_value2 == 'UK_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('GBPJPY=X')
            name = 'GBP/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYGBP=X')
            name = 'JPY/GBP'
    elif (input_value == 'UK_Index' or input_value == 'US_Index') and (input_value2 == 'UK_Index' or input_value2 == 'US_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('GBPUSD=X')
            name = 'GBP/USD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('GBP=X')
            name = 'USD/GBP'
    elif (input_value == 'UK_Index' or input_value == 'CH_Index') and (input_value2 == 'UK_Index' or input_value2 == 'CH_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('GBPCHF=X')
            name = 'GBP/CHF'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CHFGBP=X')
            name = 'CHF/GBP'
    elif (input_value == 'UK_Index' or input_value == 'NZ_Index') and (input_value2 == 'UK_Index' or input_value2 == 'NZ_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('GBPNZD=X')
            name = 'GBP/NZD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('NZDGBP=X')
            name = 'NZD/GBP'
    elif (input_value == 'UK_Index' or input_value == 'CN_Index') and (input_value2 == 'UK_Index' or input_value2 == 'CN_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('GBPCNY=X')
            name = 'GBP/CNY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CNYGBP=X')
            name = 'CNY/GBP'
    elif (input_value == 'CA_Index' or input_value == 'JP_Index') and (input_value2 == 'CA_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CADJPY=X')
            name = 'CAD/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYCAD=X')
            name = 'JPY/CAD'
    elif (input_value == 'CA_Index' or input_value == 'CH_Index') and (input_value2 == 'CA_Index' or input_value2 == 'CH_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CADCHF=X')
            name = 'CAD/CHF'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CHFCAD=X')
            name = 'CHF/CAD'
    elif (input_value == 'CA_Index' or input_value == 'CN_Index') and (input_value2 == 'CA_Index' or input_value2 == 'CN_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CADCNY=X')
            name = 'CAD/CNY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CNYCAD=X')
            name = 'CNY/CAD'
    elif (input_value == 'CH_Index' or input_value == 'JP_Index') and (input_value2 == 'CH_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CHFJPY=X')
            name = 'CHF/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYCHF=X')
            name = 'JPY/CHF'
    elif (input_value == 'CH_Index' or input_value == 'CN_Index') and (input_value2 == 'CH_Index' or input_value2 == 'CN_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CHFCNY=X')
            name = 'CHF/CNY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CNYCHF=X')
            name = 'CNY/CHF'
    elif (input_value == 'NZ_Index' or input_value == 'US_Index') and (input_value2 == 'NZ_Index' or input_value2 == 'US_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('NZDUSD=X')
            name = 'NZD/USD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('NZD=X')
            name = 'USD/NZD'
    elif (input_value == 'NZ_Index' or input_value == 'JP_Index') and (input_value2 == 'NZ_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('NZDJPY=X')
            name = 'NZD/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYNZD=X')
            name = 'JPY/NZD'
    elif (input_value == 'NZ_Index' or input_value == 'CA_Index') and (input_value2 == 'NZ_Index' or input_value2 == 'CA_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('NZDCAD=X')
            name = 'NZD/CAD'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CADNZD=X')
            name = 'CAD/NZD'
    elif (input_value == 'NZ_Index' or input_value == 'CH_Index') and (input_value2 == 'NZ_Index' or input_value2 == 'CH_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('NZDCHF=X')
            name = 'NZD/CHF'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CHFNZD=X')
            name = 'CHF/NZD'
    elif (input_value == 'NZ_Index' or input_value == 'CN_Index') and (input_value2 == 'NZ_Index' or input_value2 == 'CN_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('NZDCNY=X')
            name = 'NZD/CNY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('CNYNZD=X')
            name = 'CNY/NZD'
    elif (input_value == 'CN_Index' or input_value == 'JP_Index') and (input_value2 == 'CN_Index' or input_value2 == 'JP_Index'):
        if not checkbox: #standard currency format
            currency = Macro.getCurrencyPrice('CNYJPY=X')
            name = 'CNY/JPY'
        else: #if inverse
            currency = Macro.getCurrencyPrice('JPYCNY=X')
            name = 'JPY/CNY'
    

    traces.append(dict(
        x = currency.index,
        y = currency['Close'],
        mode= 'lines',
        name= name,
        marker = currency_color,
        yaxis= 'y2',
        )
    )

    return {
        'data': traces,
        'layout': go.Layout(
            dragmode='pan', 
            height= graph_height,
            #hovermode= False,
            yaxis2=dict(
                overlaying= 'y',
                side= "right"
            )
            
        )
    }    


#Callback for Graph - Central Bank Interest Rates
@app.callback(
    Output(component_id='Graph_IntRates', component_property='figure'),
    [Input(component_id='Dropdown_IntRates', component_property= 'value')]
)
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



#RUN PROGRAM
if __name__ == '__main__':
    app.run_server()

