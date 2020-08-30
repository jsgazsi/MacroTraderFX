import pandas as pd 
import os


path = 'RawData/'
#Working Function to Translate INVESTING.COM Data.
def getData(str):
    df = pd.read_csv(path + str, delimiter=',')
    #df = df[['Release Date', 'Actual']]
    #df = df.rename(columns={'Release Date': 'Date', 'Actual': 'Value'})
    #df['Date'] = df['Date'].str[0:13]
    #df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    #df = df.set_index('Date')
    #df = df.iloc[::-1] #Flip the order
    #Optional Step to normalize data to Z-Score
    #df.Value = df.apply(lambda x: (x-x.expanding().mean())/x.expanding().std()).round(2)
    name = "InvestingCom_testdata"
    df.to_csv(os.path.join(path, name + '.csv'))
    return df

def normalizeData(str):
    df = pd.read_csv(path + str + '.csv', delimiter=',')
    df = df.set_index('Date')
    df.Value = df.apply(lambda x: (x-x.expanding().mean())/x.expanding().std()).round(2)
    name = "InvestingCom_testdata_normalized"
    df.to_csv(os.path.join(path, name + '.csv'))
    return df

getData("United States Retail Sales MoM.csv")

#testData = getData('investingTestData.csv')
#print(testData) #Success!
#testData = normalizeData('InvestingCom_testdata')
#print(testData)
