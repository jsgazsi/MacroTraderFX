import glob
import csv
import os


for file in glob.glob("RawData/*.csv"):
    file.replace("RawData/", "")
    print(file)




#with open("All_Indicators" + '.csv', 'w') as f:
#    writer = csv.writer(f)
#    writer.writerow(files) 

