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
def drawNeighborhoods(mymap,ax,hood_map,crime_counts,crime,cmap,norm):
    for hood in hood_map.neighborhoods:
        lon,lat = hood.polygon.exterior.coords.xy
        x,y = mymap(lon,lat)
        poly = Polygon(zip(x,y))
        color = cmap(norm(crime_counts[hood.name][crime]))
        patch = PolygonPatch(poly,facecolor=color, edgecolor='#999999', alpha=0.9)
        ax.add_patch(patch)
        #print crime_counts[hood.name]['VIOLENT CRIMES'],norm(crime_counts[hood.name]['VIOLENT CRIMES']),color

def drawRefPoints(mymap,refpoints):
    for town in refpoints:
        name,lat,lon, offx, offy = town
        x,y = mymap(lon,lat)
        mymap.plot(x, y, 'ok')
        plt.annotate(name, xy=(x,y), xytext=(offx,offy),textcoords='offset points',size=14)

def get_list_of_crime_counts(crime_count, hood_map, crime):
    num_crime = []
    for h in hood_map.neighborhoods:
        num_crime.append(crime_count[h.name][crime])
    return num_crime

def make_plot(crime_counts, crime, hood_map, df, title, label, filename):
    print "Making plot for " + str(crime) + " in Chicago 2016"
    number_of_crime = get_list_of_crime_counts(crime_counts, hood_map, crime)
    fig = plt.figure()
    fig.set_size_inches(18.5,10.5,forward=True)
    ax = fig.add_subplot(111)
    mymap = getMap(df.crimes)
    mymap.drawmapboundary(fill_color='#46bcec')
    mymap.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    mymap.drawcoastlines()
    ax.set_title(title)
    cax = fig.add_axes([0.73,0.1,0.04,0.8])
    cmap = cm.get_cmap('YlOrRd')
    norm = Normalize(vmin=0, vmax=max(number_of_crime)+0.15*max(number_of_crime))
    cb = ColorbarBase(cax, cmap=cmap, norm=norm)
    drawNeighborhoods(mymap,ax,hood_map,crime_counts,crime,cmap,norm)
    cb.set_label(label)
    oname = filename+".png"
    onameref = filename+"_RefTowns.png"
    fig.savefig(oname,dpi=200)
    plt.sca(ax)
    drawRefPoints(mymap,refpoints)
    fig.savefig(onameref,dpi=200)
    print "Made " + oname
    print "Made " + onameref


""" Main """
if __name__ == "__main__":
    refpoints = [['Loop',41.883333, -87.633333,20,-3],['Wrigley Field',41.948, -87.656,17,-3],['O\'Hare',42, -87.92,-10,10],['Irving Park',41.95, -87.73,-20,10],
                 ['Oakland',41.82, -87.6,15,-3],['Hyde Park',41.8, -87.59,10,-7],['West Lawn',41.77, -87.72,-20,-20],['Calumet\nHeights',41.728333, -87.579722,-30,-30],
                 ['Washington\nHeights',41.72, -87.65,-50,-30],['Clearing',41.78, -87.76,-70,-5],['Austin',41.9, -87.76,-60,-5],['Pilsen',41.85, -87.66,-20,-16],
                 ['New City',41.81, -87.66,-75,-3],["Englewood",41.779786, -87.644778,0,-20]]
    
    """
    Initialize neighborhood finder and dataframe with the data 
    from Chicago's Open Data Portal
    """
    hood_map = neighborhoodize.NeighborhoodMap(neighborhoodize.zillow.ILLINOIS)
    #ca = crimes('ChicagoCrimes2016_Map_test.csv',hood_map)
    ca = crimes('ChicagoCrimes2016_Map.csv',hood_map)
    neighborhoods = ca.crimes['Neighborhood'].unique()
    crimeTypes = ca.crimes['Primary Type'].unique()
    
    """
    Create a dictionary that contains the counts of each crime type
    by neighborhood. Any unknown neighborhods (bad longitude, latitude
    associated with the crime report, not in a defined neighborhood, etc)
    will be stored in 'Unknown' and not processed for mapping.
    """
    crime_counts_by_neighborhood = {}
    for h in hood_map.neighborhoods:
        crime_counts_by_neighborhood.update({h.name: {}})
        for crime in crimeTypes:
            crime_counts_by_neighborhood[h.name].update({crime: 0}) 
    
    crime_counts_by_neighborhood.update({'Unknown': {}})
    for crime in crimeTypes:
        crime_counts_by_neighborhood['Unknown'].update({crime: 0}) 

    for h,crime in zip(ca.crimes['Neighborhood'].values,ca.crimes['Primary Type'].values):
        crime_counts_by_neighborhood[h][crime] += 1

    """
    Make a new label that combines the counts from all crimes 
    considered violent by Chicago PD.
    """
    violent_crime_labels = ['HOMICIDE','ASSAULT','BATTERY','CRIM SEXUAL ASSAULT']
    for h in hood_map.neighborhoods:
        violent_crimes = 0
        for lbl in violent_crime_labels:
            violent_crimes += crime_counts_by_neighborhood[h.name][lbl]
        crime_counts_by_neighborhood[h.name].update({'VIOLENT CRIMES':violent_crimes})

    """
    Plot the result on a map, colorizing each neighborhood by the number of crimes. 
    """
    #make_plot(crime_counts_by_neighborhood,'VIOLENT CRIMES',hood_map,ca,"Violent Crimes in Chicago 2016","Number of Violent Crimes","violentCrimesChicago2016")
    #make_plot(crime_counts_by_neighborhood,'MOTOR VEHICLE THEFT',hood_map,ca,"Vehicle Theft in Chicago 2016","Number of Vehicle Thefts","vehicleTheftsChicago2016")
    make_plot(crime_counts_by_neighborhood,'HOMICIDE',hood_map,ca,"Homicides in Chicago 2016","Number of Homicides","homicidesChicago2016")
