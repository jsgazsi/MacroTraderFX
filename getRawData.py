from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import WebScrapingLists
import os


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
    df.to_csv(os.path.join(path, name + '.csv'))
    print(df)
    #return df


path_to_extension = '/home/jsgart/Downloads/chromedriver_linux64/3.4.31_0'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)
driver = webdriver.Chrome('/home/jsgart/Downloads/chromedriver_linux64/chromedriver', options=chrome_options)
wait = WebDriverWait(driver, 2)


for Country in WebScrapingLists.Countries:
    for Indicator in Country:

        driver.get(Indicator)
        row_list = []
        indicatorName = driver.title
        print(indicatorName)
        
        while True:
            try:
                item = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[contains(@id,"showMoreHistory")]/a')))
                driver.execute_script("arguments[0].click();", item)
            except Exception:break


        for table in wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//*[contains(@id,"eventHistoryTable")]//tr'))):
            data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
            print(data)
            row_list.append(data)

        df = pd.DataFrame(row_list)
        processData(df)


#Keep after Loop when creating loop function
driver.quit()


