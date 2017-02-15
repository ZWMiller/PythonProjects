import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

def init():
    point.set_data([], [])
    return point,

def data_gen(df):
    for index, row in df.iterrows():
        yield [row['Latitude'],row['Longitude']]

def update(pt):
    #array = scat.get_offsets()
    #x,y = m(point[0],point[1])
    #array = np.append(array, [x,y])
    #scat.set_offsets(array)
    #return scat
    x, y = mymap(pt[1], pt[0])
    point.set_data(x, y)
    #array = point.get_offsets()
    #array = np.append(array, [x,y])
    #point.set_offsets(array)
    return point,
    

""" Main """
if __name__ == "__main__":
    hood_map = neighborhoodize.NeighborhoodMap(neighborhoodize.zillow.ILLINOIS)
    #chicagoarea = crimes('ChicagoCrimes2016_Map_test.csv',hood_map)
    chicagoarea = crimes('ChicagoCrimes2016_Map.csv',hood_map)

    # Make a map
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    mymap = Basemap(llcrnrlon=chicagoarea.crimes['Longitude'].min()-0.4,
                llcrnrlat=chicagoarea.crimes['Latitude'].min(),
                urcrnrlon=chicagoarea.crimes['Longitude'].max()+0.2,
                urcrnrlat=chicagoarea.crimes['Latitude'].max()+0.2,
                projection='lcc',lat_1=32,lat_2=45,lon_0=-95,
                resolution = 'h')
    mymap.drawmapboundary(fill_color='#46bcec')
    mymap.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    mymap.drawcoastlines()

    # Draw neighborhood bounds
    for hood in hood_map.neighborhoods:
        lon,lat = hood.polygon.exterior.coords.xy
        x,y = mymap(lon,lat)
        mymap.plot(x,y,'-k',alpha=0.5)

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
    
    # To animate it
    #ani = animation.FuncAnimation(plt.gcf(), update, data_gen(chicagoarea.crimes), init_func=init, interval=50, blit=False, save_count=1000)
    #ani.save('myanimation.gif',writer='imagemagick',fps=30)
    plt.legend(loc='upper left',prop={'size':6}, numpoints=1)
    plt.savefig("chicagoCrimeMap_2016.png")
    #plt.show()

    plt.clf()
    mymap = Basemap(llcrnrlon=chicagoarea.crimes['Longitude'].min()-0.4,
                llcrnrlat=chicagoarea.crimes['Latitude'].min(),
                urcrnrlon=chicagoarea.crimes['Longitude'].max()+0.2,
                urcrnrlat=chicagoarea.crimes['Latitude'].max()+0.2,
                projection='lcc',lat_1=32,lat_2=45,lon_0=-95,
                resolution = 'h')
    mymap.drawmapboundary(fill_color='#46bcec')
    mymap.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    mymap.drawcoastlines()
    
    # Draw neighborhood bounds
    for hood in hood_map.neighborhoods:
        lon,lat = hood.polygon.exterior.coords.xy
        x,y = mymap(lon,lat)
        mymap.plot(x,y,'-k',alpha=0.5)

    data = chicagoarea.crimes[:][chicagoarea.crimes['Primary Type'] == 'HOMICIDE']
    #x,y = mymap(0, 0)
    lon = data['Longitude'].values
    lat = data['Latitude'].values
    x,y = mymap(lon,lat)
    mymap.plot(x, y, color='r', linestyle='None', markersize=5, marker='o', alpha=1., label=data['Primary Type'].unique()[0])
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
