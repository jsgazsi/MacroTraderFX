import os
import shutil
import requests
import Macro_CSV_Lists

if os.path.exists('CSV_Data_copy'):
    shutil.rmtree('CSV_Data_copy')

if os.path.exists('CSV_Data'):
    os.rename('CSV_Data', 'CSV_Data_copy')

if not os.path.exists('CSV_Data'):
    os.makedirs('CSV_Data')


#Get Economic Data by countries from source file
Countries = Macro_CSV_Lists.Countries

#Downlaod Path
#path = "../MacroTraderFX/CSV_Data/{}"
path = "CSV_Data/{}"

#Grabs all the CSV data from the export links in the Countries List and saves them in the download path directory
for Country in Countries:
    for link in Country:
        print("Downloading... " + link.split('/')[-3] + "_" + link.split('/')[-2] + ".csv")
        r = requests.get(link) # create HTTP response object 
        file_name = link.split('/')[-3] + "_" + link.split('/')[-2] + ".csv"
        with open(path.format(file_name), "wb") as csv: 
            for chunk in r.iter_content(chunk_size=1024*1024): 
                if chunk:
                    csv.write(chunk)
                    print("Success.")
                else:
                    print("Error Downloading file: " + link.split('/')[-3] + "_" + link.split('/')[-2] + ".csv" )

#for Country in Countries:
#    for link in Country:
#        file_name = link.split('/')[-3] + "_" + link.split('/')[-2] + ".csv"
#        print(file_name)
