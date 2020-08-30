import pandas as pd


path = 'RawData/'
#Working Function to Translate INVESTING.COM Data.
def getTestData(str):
    df = pd.read_csv(path + str, delimiter='\t')
    df = df[['Release Date', 'Actual']]
    df = df.rename(columns={'Release Date': 'Date', 'Actual': 'Value'})
    df['Date'] = df['Date'].str[0:13]
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df = df.set_index('Date')
    df = df.iloc[::-1] #Flip the order
    #Optional Step to normalize data to Z-Score
    df.Value = df.apply(lambda x: (x-x.expanding().mean())/x.expanding().std()).round(2)
    name = "InvestingCom_testdata"
    df.to_csv(os.path.join(path, name + '.csv'))
    return df

testData = getTestData('investingTestData.csv')
print(testData) #Success!