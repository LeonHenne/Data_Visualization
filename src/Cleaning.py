import pandas as pd

#reading in the original data and the additional datasets
df = pd.read_csv("https://gist.githubusercontent.com/Inwernos/6643dc386e6563720b3bc62a6bc0bfb8/raw/349521123a4713faf7d068f6898e097778b7edef/Alle_Fluege.csv",low_memory=False)
df_airlines = pd.read_csv("https://gist.githubusercontent.com/Inwernos/9d57694cceaa458a4c18e78911e69606/raw/d4d2c0769d56cb06c9f0923890145687737dbeaf/Airlines.csv",low_memory=False)
df_airports = pd.read_csv("https://gist.githubusercontent.com/Inwernos/f3caef84f6cf2ced32cee25b5e8e9cfd/raw/6a9b807d69d634490efb43ecbc14c1b00c647cd0/Airports.csv",low_memory=False)


#merging the original and the airline datasets and repositioning the airlinename column next to the respective airline code
df_airlines = df_airlines.rename(columns=dict(AIRLINE='AIRLINE_NAME'))
df = pd.merge(left=df, right=df_airlines, how='left', left_on='AIRLINE', right_on='IATA_CODE').drop(columns=['IATA_CODE','Unnamed: 0','Unnamed: 0.1'])
column = df['AIRLINE_NAME']
df = df.drop(columns = 'AIRLINE_NAME')
df.insert(4,'AIRLINE_NAME',column)


#merging the recently modified dataset with the airport dataframe and repositioning the two airportname column (origin airport and destination airport) next to the respective airport code 
df_airports = df_airports.rename(columns = dict(IATA_CODE = 'AIRPORT_CODE'))
df_airports = df_airports.rename(columns = dict(AIRPORT = 'ORIGIN_AIRPORT_NAME'))
df = pd.merge(left=df, right=df_airports, how='left', left_on='ORIGIN_AIRPORT', right_on='AIRPORT_CODE').drop(columns=['AIRPORT_CODE','CITY','STATE','COUNTRY','LATITUDE','LONGITUDE'])
column = df['ORIGIN_AIRPORT_NAME']
df = df.drop(columns = 'ORIGIN_AIRPORT_NAME')
df.insert(7,'ORIGIN_AIRPORT_NAME',column)

df_airports = df_airports.rename(columns = dict(ORIGIN_AIRPORT_NAME = 'DESTINATION_AIRPORT_NAME'))
df = pd.merge(left=df, right=df_airports, how='left', left_on='DESTINATION_AIRPORT', right_on='AIRPORT_CODE').drop(columns=['AIRPORT_CODE','CITY','STATE','COUNTRY','LATITUDE','LONGITUDE'])
column = df['DESTINATION_AIRPORT_NAME']
df = df.drop(columns = 'DESTINATION_AIRPORT_NAME')
df.insert(9,'DESTINATION_AIRPORT_NAME',column)



#saving the changes into a new csv file
#df.to_csv('/Users/leonhenne/Repositories/git-dhbw/DS101_DV/Abgabe/data/cleaned data/Alle_Fluege_cleaned.csv')