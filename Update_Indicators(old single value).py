from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import WebScrapingLists
import os
import csv


path = 'RawData/'

#Working Function to Translate INVESTING.COM Data.
def processData(df):
    headers = df.iloc[0]
    df  = pd.DataFrame(df.values[1:], columns=headers)
    df = df[['Release Date', 'Actual']]
    df = df.rename(columns={'Release Date': 'Date', 'Actual': 'Value'})
    df['Date'] = df['Date'].str[0:13]
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df = df.set_index('Date')
    df = df.iloc[::-1] #Flip the order to ascending
    filter = df["Value"] != " "
    df = df[filter]
    name = indicatorName #Identify what is being scraped
    print(name)
    df = df.tail(1) #Get only the latest value to check for appending data file
    #df.to_csv(os.path.join(path, name + '.csv'))
    print(df) #print to verify scraping
    return df


path_to_extension = '/home/jsgart/Downloads/chromedriver_linux64/3.4.31_0'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)
driver = webdriver.Chrome('/home/jsgart/Downloads/chromedriver_linux64/chromedriver', options=chrome_options)
wait = WebDriverWait(driver, 2)
#driver.implicitly_wait(10)


for Country in WebScrapingLists.Countries:
    for Indicator in Country:


        driver.get(Indicator)

        row_list = []

        indicatorName = driver.title
        print(indicatorName)


        for table in wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//*[contains(@id,"eventHistoryTable")]//tr'))):
            data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
            #print(data)
            row_list.append(data)
        df = pd.DataFrame(row_list)
        df = processData(df)

        
            
     
        
        newDate = df.index[0]
        newValue = df.Value[0]
        newField = [df.index[0], df.Value[0]]

        with open(path + indicatorName + '.csv', 'a') as f:
            orig_df = pd.read_csv(path + indicatorName + '.csv').tail(1)
            orig_df = orig_df.set_index('Date')
            oldDate = orig_df.index[0]
            oldValue = orig_df.Value[0]
            print(newField)
            #NEW VALUE DETECTED - APPEND FILE
            if newDate != oldDate:
                writer = csv.writer(f)
                writer.writerow(newField)


#Keep after Loop when crating loop function
driver.quit()


