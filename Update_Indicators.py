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
    name = indicatorName.replace("/", " ") #Identify what is being scrape
    print(name)
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
        indicatorName = driver.title.replace("/", " ")

        for table in wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//*[contains(@id,"eventHistoryTable")]//tr'))):
            data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
            row_list.append(data)

        df = pd.DataFrame(row_list)
        df = processData(df)
        

        with open(path + indicatorName + '.csv', 'a') as f:
            orig_df = pd.read_csv(path + indicatorName + '.csv')

            for date in df.index:
                isFound = False
                for oldDate in orig_df['Date']:
                    if date == oldDate:
                        isFound = True
                #if record is found, do nothing, it's already in data set, otherwise if not found, it is new and need to append dataset
                if not isFound: 
                    print("New Record Found: " + date, df.Value[date])  
                    writer = csv.writer(f)
                    writer.writerow([date, df.Value[date]]) 


#After looping quit web driver
driver.quit()


