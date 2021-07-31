import pandas as pd
import numpy as np
import plotly.graph_objects as go

"""
•	Gibt es Unterschiede zwischen den Airlines hinsichtlich ihrer durchschnittlichen Geschwindigkeit zwischen zwei Zielen?
"""

#Cleaned dataframe
df = pd.read_csv("https://gist.githubusercontent.com/Inwernos/eb5ebc9e2a44be85a5a695f3fe365367/raw/3a0cef60f2fcdfbf2f96cb21b7027a647f5fa7b4/Alle_Fluege_cleaned.csv")


df2 = df[['AIRLINE','DISTANCE','ELAPSED_TIME','AIRLINE_NAME']]
df2['AIRSPEED'] = ((df['DISTANCE'] / df['ELAPSED_TIME'])*60)*1.4

df3 = pd.DataFrame()
df3['AVG_AIRSPEED'] = df2[['AIRLINE_NAME','AIRSPEED']].groupby(['AIRLINE_NAME']).mean()['AIRSPEED']


fig = go.Figure()
bar = go.Bar(
    x = df2['AIRLINE_NAME'].drop_duplicates().sort_values(ascending = True),
    y = df3['AVG_AIRSPEED'], name = 'Airline_Speed',
    marker = dict(color = df3['AVG_AIRSPEED'],
    colorscale = 'thermal'),
    # Daten die angezeigt werden sollen werden dem graphic object hinzugefügt werden
    customdata  = np.stack((df2['AIRLINE_NAME'].drop_duplicates().sort_values(ascending = True), round(df3['AVG_AIRSPEED'],0)), axis=-1),
    #html template, was angezeigt werden soll
    hovertemplate=('<b>Airline name</b>: %{customdata[0]}<br>'+ #Attribute des graph objects können direkt referenziert werden z.B. lat, lon
                    '<b>Average speed</b>: %{customdata[1]} km/h<br>'+ 
                      '<extra></extra>') #leere <extra> entfernen Trace1 am Ende des Tooltipps
)
fig.add_trace(bar)
fig.update_layout(title = dict(text = "Durchschnittliche Geschwindigkeit einzelner Airlines" ))
fig.update_yaxes(title_text = 'Avg. speed (Km/h)')
fig.update_xaxes(title_text = 'Airlines')

#fig.write_html('/Users/leonhenne/Desktop/DHBW/12_Eichin_Data Visualization/Abgabe/Barchart.html')
fig.show()