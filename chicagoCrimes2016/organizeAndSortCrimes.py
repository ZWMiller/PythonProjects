import numpy as np
import pandas as pd
import neighborhoodize
# Neighborhoodize from here: https://github.com/bjlange/neighborhoodize

""" Define Class Here """
class crimes(object):
    def __init__(self,filename,hoods):
        self.file = filename
        self.crimes = pd.read_csv(filename)
        self.hoodize = hoods
        self._add_neighborhoods_to_dataframe()
    
    def _add_neighborhoods_to_dataframe(self):
        if not 'Neighborhood' in self.crimes.columns:
            print "Adding Neighborhoods to DataFrame by Longitude, Latitude"
            self.crimes['Neighborhood'] = self.crimes.apply(lambda x: ''.join(self.hoodize.get_neighborhoods(x['Latitude'], x['Longitude'])),axis=1)
            self.crimes.loc[self.crimes['Neighborhood']=='','Neighborhood'] = "Unknown"
        else:
            print "Neighborhoods Already Calculated!"

    def _save_dataframe_to_file(self, fname):
        self.crimes.to_csv(fname)
    

""" Main """
if __name__ == "__main__":
    hood_map = neighborhoodize.NeighborhoodMap(neighborhoodize.zillow.ILLINOIS)
    chicagoarea = crimes('ChicagoCrimes2016_Map_test.csv',hood_map)
    chicagoarea.crimes.sort_values(['Neighborhood','Date'], inplace=True)
    chicagoarea._save_dataframe_to_file('testOut.csv')
    gb = chicagoarea.crimes.groupby('Neighborhood')
    i = 0
    for name,group in gb:
        outName = "crimesByNeighborhood/" + name + ".csv"
        pd.DataFrame(group).to_csv(outName)
        i+=1
