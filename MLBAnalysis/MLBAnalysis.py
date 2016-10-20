import numpy as np
import csv
import matplotlib.pyplot as plt

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

def calculate_processed_stats(d):
  for p in d:
    for y in d[p]:
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

if __name__ == "__main__":
  avg = list()
  iso = list()
  plot_data = {}
  stat_dictionary = get_mlb_data_from_csv()
  calculate_processed_stats(stat_dictionary)
  for player in stat_dictionary:
    for year in stat_dictionary[player]:
      if stat_dictionary[player][year]["PA"] >= 50:
        avg.append(stat_dictionary[player][year]["AVG"])
        iso.append(stat_dictionary[player][year]["ISO"])
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
  print "Avg Avg: " + str(calculate_average(stat_dictionary,"AVG"))
  
# This takes a long time to run, but produces (>400) 2D plots for correlations between all stats
  for key in plot_data:
    for key2 in plot_data:
      if key != key2:
        plotXY(plot_data[key],plot_data[key2],key2+" vs "+key, key, key2, False, False)
  
