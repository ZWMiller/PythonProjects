import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import functions_MLBAnalysis as bb
#from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import random

if __name__ == "__main__":
  stat_dictionary = bb.get_mlb_data_from_csv()
  bb.add_personal_info_to_dictionary(stat_dictionary)
  bb.add_hall_of_fame_to_dictionary(stat_dictionary)
  bb.calculate_processed_stats(stat_dictionary)
  bb.remove_pitchers_from_dictionary(stat_dictionary)
  #plot_data = bb.get_plot_data_lists(stat_dictionary)
  #bb.plot_all_2D_correlations(plot_data)
  #print "Avg Avg: " + str(bb.calculate_average(stat_dictionary,"AVG"))
  career_stats = bb.calculate_career_average(stat_dictionary)
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
  
  X = []
  Y = []
  for p in career_stats:
    X_temp,Y_temp = bb.convert_dictionary_to_learning_data(career_stats[p])
    X.append(X_temp)
    Y.append(Y_temp)

  X_test = []
  X_train = []
  y_test = []
  y_train = []
  inData = zip(X,Y)
  for tup in inData:
      t1, t2 = zip(*inData)
      if t2 == 1:
        if random.random() < 0.7:
            X_train.append(t1)
            y_train.append(t2)
        else:
            X_test.append(t1)
            y_test.append(t2)
      else:
        if random.random() < 0.7:
            X_train.append(t1)
            y_train.append(t2)
        else:
            X_test.append(t1)
            y_test.append(t2)


#  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)
  clf = LogisticRegression()
  clf.fit(X_train, y_train)

  y_pred = clf.predict(X_test)

  result = zip(y_pred, y_test)

  print result
  print f1_score(y_test, y_pred, average='weighted')




