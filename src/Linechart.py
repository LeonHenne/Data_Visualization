import pandas as pd
import numpy as np
import plotly.graph_objects as go

"""
•    Gibt es eine Korrelation zwischen der Tageszeit und der Abflugverzögerungen und wie verteilen sich diese über den Tag?
"""


def CalcDepartureDelayOverTime(Airport, name, count):
        
        DepartureTimes= Airport['SCHEDULED_DEPARTURE'].astype('str')
        DepartureDelays = Airport['DEPARTURE_DELAY'].astype('int32')

        AllFlights = {DepartureTimes.iloc[idx]: DepartureDelays.iloc[idx] for idx in range(len(DepartureTimes))}
        data = {
                'HOUR': [],
                'DEPARTURE_TIME':[],
                'DEPARTURE_DELAY':[]}

        delayPerHour = pd.DataFrame(data)
        for hour in range(0, 24):
                for DepartureTime, DepartureDelay in AllFlights.items():
                        if hour == int(DepartureTime[10:13]):
                                new_row = {'HOUR':hour,'DEPARTURE_TIME':DepartureTime,'DEPARTURE_DELAY':DepartureDelay}
                                delayPerHour = delayPerHour.append(new_row,ignore_index = True)

        avgdelayPerHour = delayPerHour.groupby('HOUR').median()

        #Anzeigen der ersten 10 Airports zur Übersichtlichkeit des Graphen, andere können jedoch angeklickt werden um sie hinzuzufügen
        if (count < 10):
                line = go.Scatter(x = delayPerHour['HOUR'].drop_duplicates(),
                                y= avgdelayPerHour['DEPARTURE_DELAY'],
                                name = name,
                                # Daten die angezeigt werden sollen müssen dem graphic object hinzugefügt werden
                                customdata  = np.stack((delayPerHour['HOUR'].drop_duplicates(), round(avgdelayPerHour['DEPARTURE_DELAY'],2)), axis=-1),
                                #html template, was angezeigt werden soll
                                hovertemplate=('<b>Hour</b>: %{customdata[0]}<br>'+ #Attribute des graph objects können direkt referenziert werden z.B. lat, lon
                                                '<b>Average delay</b>: %{customdata[1]} min.<br>'+ 
                                                '<extra></extra>') #leere <extra> entfernen Trace1 am Ende des Tooltipps
                                )
        else:
                line = go.Scatter(x = delayPerHour['HOUR'].drop_duplicates(),
                                y= avgdelayPerHour['DEPARTURE_DELAY'],
                                name = name,
                                #Linien werden nur in der Legende angezeigt
                                visible = 'legendonly',
                                # Daten die angezeigt werden sollen müssen dem graphic object hinzugefügt werden
                                customdata  = np.stack((delayPerHour['HOUR'].drop_duplicates(), round(avgdelayPerHour['DEPARTURE_DELAY'],2)), axis=-1),
                                #html template, was angezeigt werden soll
                                hovertemplate=('<b>Hour</b>: %{customdata[0]}<br>'+ #Attribute des graph objects können direkt referenziert werden z.B. lat, lon
                                                '<b>Average delay:</b>: %{customdata[1]} min.<br>'+ 
                                                '<extra></extra>') #leere <extra> entfernen Trace1 am Ende des Tooltipps
                                )
        return line



#Cleaned dataframe
df = pd.read_csv("https://gist.githubusercontent.com/Inwernos/eb5ebc9e2a44be85a5a695f3fe365367/raw/3a0cef60f2fcdfbf2f96cb21b7027a647f5fa7b4/Alle_Fluege_cleaned.csv",low_memory=False)

df_filtered = pd.DataFrame()
df_filtered = df[['ORIGIN_AIRPORT_NAME','SCHEDULED_DEPARTURE','DEPARTURE_DELAY']].sort_values(by = 'ORIGIN_AIRPORT_NAME',ascending = True)
df_filtered = df_filtered.reset_index(drop = True)

# Get Airports from DataFrame
AirportGroup = df_filtered.groupby('ORIGIN_AIRPORT_NAME')

fig = go.Figure()
count = 0
#Iterate through the different groups of the AirportGroup groupby object
for index, row in df_filtered['ORIGIN_AIRPORT_NAME'].drop_duplicates().iteritems():
        airportdata = AirportGroup.get_group(row)
        #calling the defined function to receive the scatterobject for each airport
        line = CalcDepartureDelayOverTime(airportdata, row,count)
        fig.add_trace(line)
        count = count +1

fig.update_layout(title = dict(text = "Abflugverspätung der Startflughäfen über den Tagesverlauf"))
fig.update_xaxes(title_text = 'Tagesverlauf in Stunden')
fig.update_yaxes(title_text = 'Durchschnittliche Verspätung zu einer Uhrzeit an einem Flughafen in Minuten')
#fig.write_html('/Users/leonhenne/Desktop/DHBW/12_Eichin_Data Visualization/Abgabe/Linechart.html')
fig.show()

