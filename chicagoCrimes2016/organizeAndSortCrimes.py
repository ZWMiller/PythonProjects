import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import neighborhoodize
# Neighborhoodize from here: https://github.com/bjlange/neighborhoodize

""" Define Class Here """
class crimes(object):
    def __init__(self,filename,hoods):
        self.file = filename
        self.crimes = pd.read_csv(filename)
        self._cleanFrame()
        self.hoodize = hoods
        self._add_neighborhoods_to_dataframe()

    def _cleanFrame(self):
        self.crimes = self.crimes[pd.notnull(self.crimes['Latitude'])]
        self.crimes = self.crimes[pd.notnull(self.crimes['Longitude'])]
            
    def _add_neighborhoods_to_dataframe(self):
        if not 'Neighborhood' in self.crimes.columns:
            print "Adding Neighborhoods to DataFrame by Longitude, Latitude"
            self.crimes['Neighborhood'] = self.crimes.apply(lambda x: ''.join(self.hoodize.get_neighborhoods(x['Latitude'], x['Longitude'])),axis=1)
            self.crimes.loc[self.crimes['Neighborhood']=='','Neighborhood'] = "Unknown"
        else:
            print "Neighborhoods Already Calculated!"

    def _save_dataframe_to_file(self, fname):
        self.crimes.to_csv(fname)

def getMap(df):
    return Basemap(llcrnrlon=df['Longitude'].min()-0.4,
                llcrnrlat=df['Latitude'].min(),
                urcrnrlon=df['Longitude'].max()+0.2,
                urcrnrlat=df['Latitude'].max()+0.2,
                projection='lcc',lat_1=32,lat_2=45,lon_0=-95,
                resolution = 'h')
def drawNeighborhoods(mymap,hood_map):
    for hood in hood_map.neighborhoods:
        lon,lat = hood.polygon.exterior.coords.xy
        x,y = mymap(lon,lat)
        mymap.plot(x,y,'-k',color='lightgrey')

def drawRefPoints(mymap,refpoints):
    for town in refpoints:
        name,lat,lon, offx, offy = town
        x,y = mymap(lon,lat)
        mymap.plot(x, y, 'ok')
        plt.annotate(name, xy=(x,y), xytext=(offx,offy),textcoords='offset points')

    

""" Main """
if __name__ == "__main__":
    refpoints = [['Loop',41.883333, -87.633333,15,-3],['Wrigley Field',41.948, -87.656,15,-3],['O\'Hare',42, -87.92,-10,10],['Irving Park',41.95, -87.73,-20,10],
                 ['Oakland',41.82, -87.6,15,-3],['Hyde Park',41.8, -87.59,15,-7],['West Lawn',41.77, -87.72,-5,5],['Calumet Heights',41.728333, -87.579722,15,-5],
                 ['Washington Heights',41.72, -87.65,-15,-15],['Clearing',41.78, -87.76,-60,-5],['Austin',41.9, -87.76,-50,-5],['Pilsen',41.85, -87.66,-20,-13],
                 ['New City',41.81, -87.66,-60,-3]]
    hood_map = neighborhoodize.NeighborhoodMap(neighborhoodize.zillow.ILLINOIS)
    chicagoarea = crimes('ChicagoCrimes2016_Map_test.csv',hood_map)
    #chicagoarea = crimes('ChicagoCrimes2016_Map.csv',hood_map)

    # Make a map
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    mymap = getMap(chicagoarea.crimes)
    mymap.drawmapboundary(fill_color='#46bcec')
    mymap.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    mymap.drawcoastlines()
    drawNeighborhoods(mymap,hood_map)

    # Seperate dataframe into list of crime types
    crimeTypes = chicagoarea.crimes['Primary Type'].unique()
    colors = iter(cm.rainbow(np.linspace(0, 1, len(crimeTypes))))
    for crime in crimeTypes:
        data = chicagoarea.crimes[:][chicagoarea.crimes['Primary Type'] == crime]
        #x,y = mymap(0, 0)
        lon = data['Longitude'].values
        lat = data['Latitude'].values
        x,y = mymap(lon,lat)
        mymap.plot(x, y, color=next(colors), linestyle='None', markersize=5, marker='o', alpha=0.7, label=data['Primary Type'].unique()[0])
    
    drawRefPoints(mymap,refpoints)
    
    plt.legend(loc='upper left',prop={'size':6}, numpoints=1)
    plt.savefig("chicagoCrimeMap_2016.png")

    plt.clf()
    mymap = getMap(chicagoarea.crimes)
    mymap.drawmapboundary(fill_color='#46bcec')
    mymap.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    mymap.drawcoastlines()
    drawNeighborhoods(mymap,hood_map)

    data = chicagoarea.crimes[:][chicagoarea.crimes['Primary Type'] == 'HOMICIDE']
    #x,y = mymap(0, 0)
    lon = data['Longitude'].values
    lat = data['Latitude'].values
    x,y = mymap(lon,lat)
    mymap.plot(x, y, color='r', linestyle='None', markersize=5, marker='o', alpha=1., label=data['Primary Type'].unique()[0])
    drawRefPoints(mymap,refpoints)
    plt.legend(loc='upper left',prop={'size':6}, numpoints=1)
    plt.savefig("chicagoHomicideMap_2016.png")


    # For making neighborhood specific csv
    """
    chicagoarea.crimes.sort_values(['Neighborhood','Date'], inplace=True)
    chicagoarea._save_dataframe_to_file('testOut.csv')
    gb = chicagoarea.crimes.groupby('Neighborhood')
    i = 0
    for name,group in gb:
        outName = "crimesByNeighborhood/" + name + ".csv"
        pd.DataFrame(group).to_csv(outName)
        i+=1
    """
