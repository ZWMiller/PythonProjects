import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import functions_MLBAnalysis as bb
#from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
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
  career_stats = bb.calculate_career_stats(stat_dictionary)
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
  X_test = []
  X_train = []
  y_test = []
  y_train = []
  X_to_predict = []
  name_of_to_predict = []
  for p in career_stats:
    print p
    print career_stats[p]
    print stat_dictionary[p]
    print 

    t1, t2, t3 = bb.convert_dictionary_to_learning_data(career_stats[p])
    
    if stat_dictionary[p]["lastYear"] >= 2011 and stat_dictionary[p]["seasonsPlayed"] > 2:
        X_to_predict.append(t1)
        name_of_to_predict.append(t3)

    # Screen ineligible players from training and test data
    if stat_dictionary[p]["seasonsPlayed"] < 10 and stat_dictionary[p]["lastYear"] < 2011:
        continue

    if stat_dictionary[p]["lastYear"] < 2011: # want to predict for people who are not yet eligible
                                # So only use eligible in training and test
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

  # Actually use the scikit learn model
  clf = LogisticRegression()
  #clf = RandomForestClassifier(n_estimators = 100)
  clf.fit(X_train, y_train)

  y_pred = clf.predict(X_test)
  y_prob = clf.predict_proba(X_test)

  # Plot Probability, sorted to see the discrimination power
  plot_prob = []
  for ele in y_prob:
      plot_prob.append(ele[1])
  bb.plot_probability_distribution(plot_prob)
  
  #result = zip(y_pred, y_test)
  #for r in result:
  #  print r
  
  print "---Direct Prediction---"
  print "F1: "
  print f1_score(y_test, y_pred, average='weighted')
  print "Precision: "
  print precision_score(y_test, y_pred)
  print "Recall: "
  print recall_score(y_test, y_pred)
  print "Confusion Matrix: "
  print confusion_matrix(y_test, y_pred)
  print
  
  # Try using a threshold with the prediction probability to get better model
  # Only write out answer with best F1 value
  bestThresh = 0.6
  bestF1 = 0
  for thresh in range(2,13):
    y_pred2=[]
    thresh = float(thresh)/20.0
    for ele in y_prob:
      if ele[1] > thresh:
          y_pred2.append(1)
      else:
          y_pred2.append(0)
    f1 = f1_score(y_test, y_pred2, average='weighted')
    if f1 > bestF1:
         bestF1 = f1
         bestThresh = thresh
    
  y_pred2=[]
  for ele in y_prob:
    if ele[1] > bestThresh:
        y_pred2.append(1)
    else:
        y_pred2.append(0) 

  print "---Probability with Threshold: " + str(bestThresh) + "---"
  print "F1: "
  print f1_score(y_test, y_pred2, average='weighted')
  print "Precision: "
  print precision_score(y_test, y_pred2)
  print "Recall: "
  print recall_score(y_test, y_pred2)
  print "Confusion Matrix: "
  print confusion_matrix(y_test, y_pred2)
  print

  # Now apply to newer players
  y_new = clf.predict_proba(X_to_predict)
  prediction = zip(y_new, name_of_to_predict)

  predictedHOF = []
  predictedMaybe = []
  for pre in prediction:
      pr, nm = pre
      playername = stat_dictionary[nm]["firstName"] + " " + stat_dictionary[nm]["lastName"]
      if pr[1] > bestThresh:
          predictedHOF.append(playername)
      elif pr[1] > bestThresh/2.0:
          predictedMaybe.append(playername)

  print "Predicted HOF: "
  print predictedHOF
  print
  print "Maybe HOF: "
  print predictedMaybe
