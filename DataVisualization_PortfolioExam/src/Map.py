import pandas as pd
import numpy as np
import plotly.graph_objects as go

"""
•	Wie verteilt sich das Flugaufkommen geografisch im Land und gibt es Flughäfen, die den Verkehr besonders gut oder besonders schlecht abwickeln?
"""

#Cleaned dataframe
df = pd.read_csv("https://gist.githubusercontent.com/Inwernos/eb5ebc9e2a44be85a5a695f3fe365367/raw/3a0cef60f2fcdfbf2f96cb21b7027a647f5fa7b4/Alle_Fluege_cleaned.csv")
token = 'pk.eyJ1Ijoid2kyMDE2NiIsImEiOiJja21uNXpubm8xcnQwMzFxa2RwdmIyNWgyIn0.-0n7ZC-GuVWkaRrYQCwUHA'


#data frame which only contains a single lat and lon value for an airport
df_originairportcoordinates = df[['ORIGIN_AIRPORT_NAME','ORIGIN_AIRPORT_LAT','ORIGIN_AIRPORT_LON']].drop_duplicates()
df_destinationairportcoordinates = df[['DESTINATION_AIRPORT_NAME','DESTINATION_AIRPORT_LAT','DESTINATION_AIRPORT_LON']].drop_duplicates()

#arrival flight count of destination airports 
df_ArrivalCountPerAirport = pd.DataFrame()
df_ArrivalCountPerAirport = ((df.groupby('DESTINATION_AIRPORT_NAME')['FLIGHT_NUMBER'].count().astype('float')))

# departure flight count of respective airports 
df_DepartureCountPerAirport = pd.DataFrame()
df_DepartureCountPerAirport = ((df.groupby('ORIGIN_AIRPORT_NAME')['FLIGHT_NUMBER'].count().astype('float')))

#Mean of Departure Delay per Airport
df_DepartureDelayPerAirport = df.groupby('ORIGIN_AIRPORT_NAME').mean()['DEPARTURE_DELAY']

#Mean of Destination Delay per Airport
df_DestinationDelayPerAirport = df.groupby('DESTINATION_AIRPORT_NAME').mean()['DESTINATION_DELAY']



fig = go.Figure()


scatter = go.Scattermapbox(
    name = 'Origin Airports',
    lat = df_originairportcoordinates['ORIGIN_AIRPORT_LAT'],
    lon = df_originairportcoordinates['ORIGIN_AIRPORT_LON'],
    hoverinfo = 'text',
    text = df_originairportcoordinates['ORIGIN_AIRPORT_NAME'],
    mode = 'markers',
    marker=go.scattermapbox.Marker(
        size= (np.log(df_DepartureCountPerAirport)*10),
        sizemin = 5,
        color= df_DepartureDelayPerAirport,
        colorscale = 'thermal',
        cmin = -30,#df_DepartureDelayPerAirport.min(),
        cmax = 60,
        showscale=True,
    ),
    # Daten die angezeigt werden sollen müssen dem graphic object hinzugefügt werden
    customdata  = np.stack((df_originairportcoordinates['ORIGIN_AIRPORT_NAME'], df_DepartureCountPerAirport, round(df_DepartureDelayPerAirport,2)), axis=-1),
    #html template, was angezeigt werden soll
    hovertemplate=('<b>Latitude</b>: %{lat}<br>'+ #Attribute des graph objects können direkt referenziert werden z.B. lat, lon
                    '<b>Longitude</b>: %{lon}<br>'+ 
                      '<b>Airport name:</b>: %{customdata[0]}<br>'+ #customdaten
                      '<b>Flight count: </b>: %{customdata[1]}<br>'+
                      '<b>Average departure delay in min.</b>: %{customdata[2]}<br>'+
                      '<extra></extra>') #leere <extra> entfernen Trace1 am Ende des Tooltipps
)

scatter2 = go.Scattermapbox(
    lat = df_destinationairportcoordinates['DESTINATION_AIRPORT_LAT'],
    lon = df_destinationairportcoordinates['DESTINATION_AIRPORT_LON'],
    hoverinfo = 'text',
    text =  df_DestinationDelayPerAirport,
    mode = 'markers',
    marker = go.scattermapbox.Marker(
        size = (np.log(df_DepartureCountPerAirport)*10),
        sizemin = 5,
        color = df_DestinationDelayPerAirport,
        colorscale = 'thermal',
        cmin = -30,#df_DestinationDelayPerAirport.min(),
        cmax = 60,
        showscale = True
    ),
    # Daten die angezeigt werden sollen müssen dem graphic object hinzugefügt werden
    customdata  = np.stack((df_destinationairportcoordinates['DESTINATION_AIRPORT_NAME'], df_DepartureCountPerAirport, round(df_DestinationDelayPerAirport,2)), axis=-1),
    #html template, was angezeigt werden soll
    hovertemplate=('<b>Latitude</b>: %{lat}<br>'+ #Attribute des graph objects können direkt referenziert werden z.B. lat, lon
                    '<b>Longitude</b>: %{lon}<br>'+ 
                      '<b>Airport name:</b>: %{customdata[0]}<br>'+ #customdaten
                      '<b>Flight count: </b>: %{customdata[1]}<br>'+
                      '<b>Average destination delay in min.</b>: %{customdata[2]}<br>'+
                      '<extra></extra>') #leere <extra> entfernen Trace1 am Ende des Tooltipps
)


fig.add_trace(scatter)
fig.add_trace(scatter2)


fig.update_layout(
        mapbox_style="streets",
        mapbox_accesstoken=token,
        mapbox_zoom=4,
        mapbox_center={"lat": 37.92752, "lon": (-100.72411)})

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    updatemenus = [dict(active=4,
                    type = "buttons",
                    buttons = list([
                        dict(label = "Abflugsflughafen mit. durchschn. Abflugverspätung",
                        method = "update",
                        args = [{"visible": [True,False,False,False]}]),
                        dict(label = "Ankunftsflughafen mit durchschn. Ankunftsverspätung",
                        method = "update",
                        args = [{"visible": [False,True,False,False]}]),
                    ]),
                    pad = {"r":0,"t":0},
                    showactive = True,
                    x = 0,
                    xanchor = "left",
                    y = 1,
                    yanchor= "bottom",
                    direction = "right")],
        xaxis = dict(showgrid = False)
)

#fig.write_html('/Users/leonhenne/Desktop/DHBW/12_Eichin_Data Visualization/Abgabe/Map.html')
fig.show()
