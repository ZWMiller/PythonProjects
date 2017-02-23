import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
from descartes import PolygonPatch
import neighborhoodize
from shapely.geometry import Point, MultiPoint, MultiPolygon, Polygon
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
    return Basemap(llcrnrlon=df['Longitude'].min()-.05,
                llcrnrlat=df['Latitude'].min()-.025,
                urcrnrlon=df['Longitude'].max()+.05,
                urcrnrlat=df['Latitude'].max()+.025,
                projection='lcc',lat_1=32,lat_2=45,lon_0=-95,
                resolution = 'h')
def drawNeighborhoods(mymap,hood_map,crime_counts,cmap,norm):
    for hood in hood_map.neighborhoods:
        lon,lat = hood.polygon.exterior.coords.xy
        x,y = mymap(lon,lat)
        poly = Polygon(zip(x,y))
        color = cmap(norm(crime_counts[hood.name]['VIOLENT CRIMES']))
        patch = PolygonPatch(poly,facecolor=color, edgecolor='#111111', alpha=0.7)
        ax.add_patch(patch)
        #print crime_counts[hood.name]['VIOLENT CRIMES'],norm(crime_counts[hood.name]['VIOLENT CRIMES']),color

def drawRefPoints(mymap,refpoints):
    for town in refpoints:
        name,lat,lon, offx, offy = town
        x,y = mymap(lon,lat)
        mymap.plot(x, y, 'ok')
        plt.annotate(name, xy=(x,y), xytext=(offx,offy),textcoords='offset points')


""" Main """
if __name__ == "__main__":
    refpoints = [['Loop',41.883333, -87.633333,15,-3],['Wrigley Field',41.948, -87.656,15,-3],['O\'Hare',42, -87.92,-10,10],['Irving Park',41.95, -87.73,-20,10],
                 ['Oakland',41.82, -87.6,15,-3],['Hyde Park',41.8, -87.59,15,-7],['West Lawn',41.77, -87.72,-5,5],['Calumet\nHeights',41.728333, -87.579722,15,-5],
                 ['Washington\nHeights',41.72, -87.65,-15,-15],['Clearing',41.78, -87.76,-60,-5],['Austin',41.9, -87.76,-50,-5],['Pilsen',41.85, -87.66,-20,-13],
                 ['New City',41.81, -87.66,-60,-3]]
    hood_map = neighborhoodize.NeighborhoodMap(neighborhoodize.zillow.ILLINOIS)
    #ca = crimes('ChicagoCrimes2016_Map_test.csv',hood_map)
    ca = crimes('ChicagoCrimes2016_Map.csv',hood_map)

    neighborhoods = ca.crimes['Neighborhood'].unique()
    crimeTypes = ca.crimes['Primary Type'].unique()
    crime_counts_by_neighborhood = {}
    #for h in neighborhoods:
    for h in hood_map.neighborhoods:
        crime_counts_by_neighborhood.update({h.name: {}})
        for crime in crimeTypes:
            crime_counts_by_neighborhood[h.name].update({crime: 0}) 
    crime_counts_by_neighborhood.update({'Unknown': {}})
    for crime in crimeTypes:
        crime_counts_by_neighborhood['Unknown'].update({crime: 0}) 
    for h,crime in zip(ca.crimes['Neighborhood'].values,ca.crimes['Primary Type'].values):
        crime_counts_by_neighborhood[h][crime] += 1

    violent_crime_labels = ['BATTERY','ASSAULT','HOMICIDE','CRIM SEXUAL ASSAULT']
    number_of_violent_crimes = []
    for h in hood_map.neighborhoods:
        violent_crimes = 0
        for lbl in violent_crime_labels:
            violent_crimes += crime_counts_by_neighborhood[h.name][lbl]
        crime_counts_by_neighborhood[h.name].update({'VIOLENT CRIMES':violent_crimes})
        number_of_violent_crimes.append(violent_crimes)

    cmap = cm.get_cmap('YlOrRd')
    norm = Normalize(vmin=0, vmax=max(number_of_violent_crimes))
    
    fig = plt.figure()
    fig.set_size_inches(18.5,10.5,forward=True)
    ax = fig.add_subplot(111)
    mymap = getMap(ca.crimes)
    mymap.drawmapboundary(fill_color='#46bcec')
    mymap.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    mymap.drawcoastlines()
    ax.set_title("Violent Crimes in Chicago by Neighborhood")
    cax = fig.add_axes([0.73,0.1,0.04,0.8])
    cb = ColorbarBase(cax, cmap=cmap, norm=norm)
    drawNeighborhoods(mymap,hood_map,crime_counts_by_neighborhood,cmap,norm)
    cb.set_label("Number of Violent Crimes")
    fig.savefig("violentCrimeHeatMap.png",dpi=200)
    plt.sca(ax)
    drawRefPoints(mymap,refpoints)
    fig.savefig("violentCrimeHeatMap_RefTowns.png",dpi=200)

    #for h in neighborhoods:
    #    print "\n"+str(h)
    #    print crime_counts_by_neighborhood[h]
