import numpy as np
import csv
import matplotlib.pyplot as plt
import sys

def get_mlb_data_from_csv(): 
  stat_dictionary = {}
  with open('baseballDatabank/Batting.csv','r') as f:
  #with open('testInput.txt','r') as f:
    skipFirstLine = True
    reader = csv.reader(f)
    for row in reader:
      line2 = []
      if skipFirstLine:
        skipFirstLine = False
        continue
      try:
        for i, x in enumerate(row):
          if len(x.strip())< 1:
            x = row[i] = '-999'
          line2.append(str(x))
        playerID, year, stint, teamID, lgID, g, ab, r, h, x2b, x3b, hr, rbi, sb, cs, bb, so, ibb, hbp, sh, sf, gidp = line2
      except:
        print "Bad Line, Skipping!\n"
        continue
      playerID = playerID.lower()
      year = int(year)
      stint = int(stint)
      teamID = teamID.lower()
      lgID = lgID.lower()
      g = int(g)
      ab = int(ab)
      r = int(r)
      h = int(h)
      x2b = int(x2b)
      x3b = int(x3b)
      hr = int(hr)
      rbi = int(rbi)
      sb = int(sb)
      cs = int(cs)
      bb = int(bb)
      so = int(so)
      ibb = int(ibb)
      hbp = int(hbp)
      sh = int(sh)
      sf = int(sf)
      gidp = int(gidp)
      if playerID not in stat_dictionary:
        stat_dictionary[playerID]={}
      stat_dictionary[playerID][year] = {
          "stint": stint, "teamID": teamID, "lgID": lgID, "G": g, "AB": ab, "R": r, "H": h, "X2B": x2b, "X3B": x3b, "HR": hr, "RBI": rbi, 
          "SB": sb, "CS": cs, "BB": bb, "SO": so, "IBB": ibb, "HBP": hbp, "SH": sh, "SF": sf, "GIDP": gidp,
      }
  return stat_dictionary

def add_personal_info_to_dictionary(d):
  with open('baseballDatabank/Master.csv','r') as f:
    skipFirstLine = True
    reader = csv.reader(f)
    for row in reader:
      line2 = []
      if skipFirstLine:
        skipFirstLine = False
        continue
      try:
        for i, x in enumerate(row):
          if len(x.strip())< 1:
            x = row[i] = '-999'
          line2.append(str(x))
        playerID, birthYear, birthMonth, birthDay, birthCountry, birthState, birthCity, deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, nameLast, nameGiven, weight, height, bats, throws, debut, finalGame, retroID, bbrefID = line2
      except:
        print "Bad Line, Skipping!\n"
        print "Unexpected error:", sys.exc_info()[0]
        continue
      playerID = playerID.lower()
      birthYear = int(birthYear)
      for player in d:
          if player == playerID:
            d[player].update( {"firstName": nameFirst, "lastName": nameLast, "birthYear": birthYear} )
            break

def add_hall_of_fame_to_dictionary(d):
  with open('baseballDatabank/HallOfFame.csv','r') as f:
    skipFirstLine = True
    reader = csv.reader(f)
    for row in reader:
      line2 = []
      if skipFirstLine:
        skipFirstLine = False
        continue
      try:
        for i, x in enumerate(row):
          if len(x.strip())< 1:
            x = row[i] = '-999'
          line2.append(str(x))
        playerID, yearid, votedBy, ballots, needed, votes, inducted, category, needed_note = line2
      except:
        print "Bad Line, Skipping!\n"
        print "Unexpected error:", sys.exc_info()[0]
        continue
      playerID = playerID.lower()
      inducted = inducted.lower()
      for player in d:
        if player == playerID:
          if inducted == "y":
            d[player].update( {"HOF": 1,} )
            break
  for player in d:
    if "HOF" not in d[player]:
      d[player].update( {"HOF": 0,} )

def calculate_processed_stats(d):
  for p in d:
    for y in d[p]: 
      if not isinstance(y,(int, long)):
        continue
      if d[p][y]["AB"] == 0:
        avg = 0
        iso = 0
        pa = d[p][y]["AB"]+d[p][y]["BB"]+d[p][y]["HBP"]
      else:
        avg = float(d[p][y]["H"])/float(d[p][y]["AB"])
        pa = d[p][y]["AB"]+d[p][y]["BB"]+d[p][y]["HBP"]
        iso = (float(d[p][y]["X2B"])+2.*float(d[p][y]["X3B"])+3.*float(d[p][y]["HR"]))/float(d[p][y]["AB"])
        obp = (float(d[p][y]["H"])+float(d[p][y]["BB"])+float(d[p][y]["HBP"]))/float(pa)
      d[p][y].update( {"AVG": avg, "PA": pa, "ISO": iso, "OBP": obp,} )

def calculate_average(d,stat):
  count, add = 0, 0
  for p in d:
    for y in d[p]: 
      if not isinstance(y,(int, long)):
        continue
      if d[p][y]["PA"] >= 50 and d[p][y][stat] != -999 and d[p][y][stat] != '-999':
        add += d[p][y][stat]
        count += 1
  return float(add)/float(count)

def plotXY(x, y, title, xlbl, ylbl, x_3decimals, y_3decimals):
  #fig, ax = plt.subplots()
  plt.scatter(x,y)
  plt.xlabel(xlbl)
  plt.ylabel(ylbl)
  plt.title(title) 
  if x_3decimals:
    xx, locs = plt.xticks()
    ll = ['%.3f'% a for a in xx]
    plt.xticks(xx,ll)
  if y_3decimals:
    yy, locs = plt.yticks()
    ly = ['%.3f'% a for a in yy]
    plt.yticks(yy,ly)
  plt.savefig('img/'+ylbl+'vs'+xlbl+'.png')
  #plt.show()
  plt.close()

def get_plot_data_lists(stat_dictionary):
  plot_data = {}
  for player in stat_dictionary:
    for year in stat_dictionary[player]: 
      if not isinstance(year,(int, long)):
        continue
      if stat_dictionary[player][year]["PA"] >= 50:
        for key in stat_dictionary[player][year]:
          try:
            int(stat_dictionary[player][year][key])
          except:
            continue
          if key not in plot_data:
            plot_data[key] = []
          if stat_dictionary[player][year][key] == -999:
            plot_data[key].append(-1)
          else: 
            plot_data[key].append(stat_dictionary[player][year][key])
  return plot_data

def plot_all_2D_correlations(plot_data):
  # This takes a long time to run, but produces (>400) 2D plots for correlations between all stats
  for key in plot_data:
    for key2 in plot_data:
      if key != key2:
        plotXY(plot_data[key],plot_data[key2],key2+" vs "+key, key, key2, False, False)

