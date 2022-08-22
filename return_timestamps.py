import pandas as pd
import sys 
import os 

input_file=sys.argv[1]
#print('-->Returning Timestamps...')
cwd=os.getcwd()
output_file=os.path.join(cwd,'output/timestamps.csv')

b=pd.read_csv(input_file)
b= b[b['tier']=='words']
b.to_csv(output_file)

print(output_file)
