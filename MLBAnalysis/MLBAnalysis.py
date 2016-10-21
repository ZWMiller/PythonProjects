import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import functions_MLBAnalysis as bb

if __name__ == "__main__":
  stat_dictionary = bb.get_mlb_data_from_csv()
  bb.add_personal_info_to_dictionary(stat_dictionary)
  bb.add_hall_of_fame_to_dictionary(stat_dictionary)
  bb.calculate_processed_stats(stat_dictionary)
  #plot_data = bb.get_plot_data_lists(stat_dictionary)
  #bb.plot_all_2D_correlations(plot_data)
  #print "Avg Avg: " + str(bb.calculate_average(stat_dictionary,"AVG"))
  count_players = []
  count_HOF = []
  for p in stat_dictionary:
      if p not in count_players:
        count_players.append(p)
      if p not in count_HOF: 
        if stat_dictionary[p]["HOF"]:
          count_HOF.append(p)
  print "Players in HOF: " + str(len(count_HOF))
  print "Players in MLB: " + str(len(count_players))
  print "Percentage of Players in HOF: " + str(float(len(count_HOF))/float(len(count_players))*100) +"%"
