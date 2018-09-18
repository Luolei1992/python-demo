import csv

with open('csv.csv','ab') as f:
   f.write(open('demo.csv','rb').read())