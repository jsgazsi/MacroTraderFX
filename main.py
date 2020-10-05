import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go 
import Macro
import Functions


#Link to myfxbook
external_scripts = [
    {'src': 'http://widgets.myfxbook.com/scripts/fxOutlook.js?type=1&symbols=,1,2,3,' }
]





#MacroTraderFX Dashboard

app = dash.Dash(__name__,external_scripts=external_scripts)
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True

server = app.server



app.title = 'MacroTrader'


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


    #Radio Button to select Macro Z-Score or Macro Index
    #dcc.RadioItems(id='radio_button_Macro_View',
    #options=[
    #    {'label': 'Macroeconomic Z-Scores', 'value': 'MacroScore'},
    #    {'label': 'Macro Index (i.e. Country vs Global Average)', 'value': 'MacroIndex'},
    #],
    #value='MacroScore'
    #),

    

    #General Macro Z-Score Section
    html.Label('Macroeconomic Z-Scores'),
    dcc.Dropdown(id='dd_MacroScore', style={'width': '100%'},
        options=[
            {'label': 'United States', 'value': 'US_Macro'},
            {'label': 'Euro Area', 'value': 'EU_Macro'},
            {'label': 'Japan', 'value': 'JP_Macro'},
            {'label': 'United Kingdom', 'value': 'UK_Macro'},
            {'label': 'Canada', 'value': 'CA_Macro'},
            {'label': 'Australia', 'value': 'AU_Macro'},
            {'label': 'Switzerland', 'value': 'CH_Macro'},
            {'label': 'New Zealand', 'value': 'NZ_Macro'},
            {'label': 'China', 'value': 'CN_Macro'},
            {'label': 'Global Average', 'value': 'Global_Average'},
        ],
        value = ['US_Macro', 'EU_Macro', 'Global_Average'],
        multi = True
    ),
    dcc.Graph(id='MacroScore', config={'scrollZoom': True}),

    #Macro Indexes Section (Country VS. Rest of World Global Avg.)
    html.Label('Macro Index (i.e. Country vs Global Average)'),
    dcc.Dropdown(id='dd_MacroIndex', style={'width': '100%'},
        options=[
            {'label': 'United States', 'value': 'US_Index'},
            {'label': 'Euro Area', 'value': 'EU_Index'},
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
    dcc.Graph(id='MacroIndex', config={'scrollZoom': True}),

    #Individual Economony Comparision with Currency Prices Section
    html.Div([html.Label('Economy Differentials')]),
    dcc.Dropdown(id='dd_MacroIndexDiff_1', style={'display': 'inline-block', 'width': '51%'},
        options=[
            {'label': 'EURUSD', 'value': 'EUR/USD'},
            {'label': 'EURJPY', 'value': 'EUR/JPY'},
            {'label': 'EURGBP', 'value': 'EUR/GBP'},
            {'label': 'EURCAD', 'value': 'EUR/CAD'},
            {'label': 'EURAUD', 'value': 'EUR/AUD'},
            {'label': 'EURCHF', 'value': 'EUR/CHF'},
            {'label': 'EURNZD', 'value': 'EUR/NZD'},
            {'label': 'EURCNH', 'value': 'EUR/CNH'},
            {'label': 'EURJPY', 'value': 'EUR/JPY'},
            {'label': 'USDJPY', 'value': 'USD/JPY'},
            {'label': 'USDCAD', 'value': 'USD/CAD'},
            {'label': 'USDCHF', 'value': 'USD/CHF'},
            {'label': 'USDCNH', 'value': 'USD/CNH'},
            {'label': 'GBPUSD', 'value': 'GBP/USD'},
            {'label': 'GBPJPY', 'value': 'GBP/JPY'},
            {'label': 'GBPCAD', 'value': 'GBP/CAD'},
            {'label': 'GBPAUD', 'value': 'GBP/AUD'},
            {'label': 'GBPCHF', 'value': 'GBP/CHF'},
            {'label': 'GBPNZD', 'value': 'GBP/NZD'},
            {'label': 'GBPCNH', 'value': 'GBP/CNH'},
            {'label': 'CADJPY', 'value': 'CAD/JPY'},
            {'label': 'CADCHF', 'value': 'CAD/CHF'},
            {'label': 'CADCNH', 'value': 'CAD/CNH'},
            {'label': 'AUDUSD', 'value': 'AUD/USD'},
            {'label': 'AUDJPY', 'value': 'AUD/JPY'},
            {'label': 'AUDCAD', 'value': 'AUD/CAD'},
            {'label': 'AUDCHF', 'value': 'AUD/CHF'},
            {'label': 'AUDNZD', 'value': 'AUD/NZD'},
            {'label': 'AUDCNH', 'value': 'AUD/CNH'},
            {'label': 'NZDUSD', 'value': 'NZD/USD'},
            {'label': 'NZDJPY', 'value': 'NZD/JPY'},
            {'label': 'NZDCAD', 'value': 'NZD/CAD'},
            {'label': 'NZDCHF', 'value': 'NZD/CHF'},
            {'label': 'NZDCNH', 'value': 'NZD/CNH'},
            {'label': 'CHFJPY', 'value': 'CHF/JPY'},
            {'label': 'CHFCNH', 'value': 'CHF/CNH'},
            {'label': 'CNHJPY', 'value': 'CNH/JPY'},
        ],
        value = 'EUR/USD',
    ),
    #dcc.Dropdown(id='dd_MacroIndexDiff_2',style={'display': 'inline-block', 'width': '51%'},
    #    options=[
    #        {'label': 'United States', 'value': 'US_Index'},
    #        {'label': 'Euro Area', 'value': 'EU_Index'},
    #        {'label': 'Japan', 'value': 'JP_Index'},
    #        {'label': 'United Kingdom', 'value': 'UK_Index'},
    #        {'label': 'Canada', 'value': 'CA_Index'},
    #        {'label': 'Australia', 'value': 'AU_Index'},
    #        {'label': 'Switzerland', 'value': 'CH_Index'},
    #        {'label': 'New Zealand', 'value': 'NZ_Index'},
    #        {'label': 'China', 'value': 'CN_Index'},
    #    ],
    #    value = 'US_Index',
    #),
    #dcc.Checklist(id='CurrencyInverse',
    #    options=[
    #        {'label': 'Currency Inverse', 'value': 'inverse'},
    #    ],  
    #),  
    dcc.Graph(id='MacroIndexDifferential', config={'scrollZoom': True}),


    #COT Report Section
    html.Label('Commitment of Traders Report (CFTC) Non-commercial Positions (Institutional Money)'),
    dcc.Dropdown(id='dd_COT', style={'width': '100%'},
        options=[
            {'label': 'EUR (COT)', 'value': 'EUR_COT'},
            {'label': 'JPY (COT)', 'value': 'JPY_COT'},
            {'label': 'GBP (COT)', 'value': 'GBP_COT'},
            {'label': 'CAD (COT)', 'value': 'CAD_COT'},
            {'label': 'AUD (COT)', 'value': 'AUD_COT'},
            {'label': 'NZD (COT)', 'value': 'NZD_COT'},
            {'label': 'CHF (COT)', 'value': 'CHF_COT'},
        ],
        value = ['EUR_COT', 'JPY_COT', 'GBP_COT', 'CAD_COT', 'AUD_COT', 'NZD_COT', 'CHF_COT'],
        multi = True
    ),
    dcc.Graph(id='COT', config={'scrollZoom': True}),


    #Interest Rates Section
    html.Label('Central Bank Interest Rates'),
    dcc.Dropdown(id='dd_IntRates', style={'width': '100%'},
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
    dcc.Graph(id='IntRates', config={'scrollZoom': True}),

   

])

   
#Callback for MacroScore, Macroeconomic Z-Scores
@app.callback(
    Output(component_id='MacroScore', component_property='figure'),
    [Input(component_id='dd_MacroScore', component_property= 'value')]
)
def updateMacroScore(input_value):
    figure = Functions.updateMacroScore(input_value)
    return figure


#Callback for MacroIndex, Macroeconomic indexes (i.e. Country vs Global Average)
@app.callback(
    Output(component_id='MacroIndex', component_property='figure'),
    [Input(component_id='dd_MacroIndex', component_property= 'value')]
)
def updateMacroIndex(input_value):
    figure = Functions.updateMacroIndex(input_value)
    return figure


#Callback for MacroIndexDifferential, (One on One comparision)
@app.callback(
    Output(component_id='MacroIndexDifferential', component_property='figure'),
    [Input(component_id='dd_MacroIndexDiff_1', component_property= 'value')]
)
def updateMacroDifferential(input_value):
    figure = Functions.updateMacroDifferential(input_value)
    return figure
  

#Callback for Graph_COT Commitment of Traders Report
@app.callback(
    Output(component_id='COT', component_property='figure'),
    [Input(component_id='dd_COT', component_property= 'value')]
)
def updateCOT_Report(input_value):
    figure = Functions.updateCOT_Report(input_value)
    return figure

#Callback for Graph - Central Bank Interest Rates
@app.callback(
    Output(component_id='IntRates', component_property='figure'),
    [Input(component_id='dd_IntRates', component_property= 'value')]
)
def updateInterestRates(input_value):
    figure = Functions.updateInterestRates(input_value)
    return figure



#RUN PROGRAM
if __name__ == '__main__':
    app.run_server(debug=True)

