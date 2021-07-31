import pandas as pd
import numpy as np
import plotly.graph_objects as go

"""
•	Ermöglichen größere Airlines eine bessere Dienstleistung, bezogen auf die Zuverlässigkeit ihres Zeitversprechens, als kleinere Unternehmen?
"""

#Cleaned dataframe
df = pd.read_csv("https://gist.githubusercontent.com/Inwernos/eb5ebc9e2a44be85a5a695f3fe365367/raw/3a0cef60f2fcdfbf2f96cb21b7027a647f5fa7b4/Alle_Fluege_cleaned.csv")

#Creating a dataframe and count all flightnumbers per airline
df2 = pd.DataFrame()
df2['SUM_OF_FLIGHTS'] = df[['AIRLINE_NAME', 'FLIGHT_NUMBER']].groupby(['AIRLINE_NAME']).count()['FLIGHT_NUMBER']

#adding the average delay per Airline as a column to the df
df2['MEAN_DESTINATION_DELAY'] = df[['AIRLINE_NAME','DESTINATION_DELAY']].groupby(['AIRLINE_NAME']).mean()['DESTINATION_DELAY']


fig = go.Figure()
scatter = go.Scatter(x = df2['SUM_OF_FLIGHTS'],
                     y = df2['MEAN_DESTINATION_DELAY'],
                     mode = 'markers',
                     legendgroup = 'Airports',
                     #visible = 'legendonly',
                     customdata  = np.stack((df['AIRLINE_NAME'].drop_duplicates().sort_values(ascending = True),df2['SUM_OF_FLIGHTS'], round(df2['MEAN_DESTINATION_DELAY'],2)), axis=-1),
                     #html template, was angezeigt werden soll
                     hovertemplate=('<b>Airline name</b>: %{customdata[0]}<br>'+ #Attribute des graph objects können direkt referenziert werden z.B. lat, lon
                     '<b>Sum of Flights</b>: %{customdata[1]}<br>'+ 
                     '<b>Average destination delay</b>: %{customdata[2]} min<br>'+ 
                     '<extra></extra>') #leere <extra> entfernen Trace1 am Ende des Tooltipps
)
fig.add_trace(scatter)
fig.update_layout(title = dict(text = "Zusammenhang zwischen der Größe und der Verspätung einer Airline"))
fig.update_xaxes(title_text = 'Summe der Flüge einer Airline')
fig.update_yaxes(title_text = 'Durchschnittliche Verspätung einer Airline in  Minuten')
#fig.write_html('/Users/leonhenne/Desktop/DHBW/12_Eichin_Data Visualization/Abgabe/Scatter.html')
fig.show()