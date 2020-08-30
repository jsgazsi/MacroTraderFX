#import WebScrapingLists
import os, csv
#import itertools


import pandas as pd

path = 'RawData/'
 
def str_to_datetime(string):
  return pd.to_datetime(string) # + " 00:00:00"), format='%d/%m/%Y %H:%M:%S')


def import_csv(fname):
  # read in csv
  with open(fname, "r") as read_file:
    raw = read_file.read()
  raw = raw.replace("%", "")

  out = []
  
  # get rid of the header tab
  rows = raw.split("\n")[1:]

  for row in rows:
    if "," in row:
      date = str_to_datetime(row.split(",")[0])
      change = float(row.split(",")[1]) / 100 # convert out of percent here
      out.append([date, change])

  return pd.DataFrame(out)



# takes MoM as dataframe, calculates index
def MoM_to_index(data_MoM):
  index = []

  # keep track of the current index so we dont have to access the last one each time
  cur_index_value = 100
  
  for i, row in data_MoM.iterrows():
    cur_index_value *= (1 + row[1])
    index.append([data_MoM[0][i], cur_index_value])

  return pd.DataFrame(index) 


# takes the index as a dataframe, calculates YoY changes
def index_to_YoY(index):
  YoY = []
  
  for i, row in index.iterrows():
    prev_i = max(i - 12, 0) # stops the index being negative for the first few values

    cur_YoY = 100 * row[1] / index[1][prev_i] - 100

    YoY.append([row[0], cur_YoY])
    
  #name = "InvestingCom_testdata"
  #df = pd.DataFrame(YoY)
  #df.to_csv(os.path.join(path, name + '.csv'))
  return pd.DataFrame(YoY) 



def MoM_to_YoY(data_MoM):
  return index_to_YoY(MoM_to_index(data_MoM))



print(MoM_to_YoY(import_csv(path + "United States Retail Sales MoM.csv")))

print(MoM_to_index(import_csv(path + "United States Retail Sales MoM.csv")))