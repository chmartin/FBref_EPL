# Merge two Squad datasets

import pandas as pd
import re
import sys, getopt
import glob

def easy_split(list):
    newList = []
    for item in list:
        newList.append(item.split(' ')[0])
    return newList
    
def main(argv):
    year=1992
    path = "./"
    try:
        opts, args = getopt.getopt(argv,"hy:p:",["year=","path="])
    except getopt.GetoptError:
        print('FBref_join_year_player.py -y <year> -p <path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('FBref_join_year_player.py -y <year> -p <path>')
            sys.exit()
        elif opt in ("-y", "--year"):
            year = int(arg)
        elif opt in ("-p", "--path"):
            path = arg
    
    f_gk = glob.glob(path + "/{0}-{1}*Stats_gk_players.csv".format(year,year+1))
    f = glob.glob(path + "/{0}-{1}*Stats_players.csv".format(year,year+1))
    
    if len(f_gk) != 1:
        print("Invalid input, matching input Player GK files:")
        print(f_gk)
        sys.exit(2)
    if len(f) != 1:
        print("Invalid input, matching input Player files:")
        print(f)
        sys.exit(2)
    
    df_gk_player= pd.read_csv(f_gk[0])
    df_player= pd.read_csv(f[0])
    df_gk_player['minutes'] = df_gk_player['minutes'].apply(lambda x: int(str(x).replace(',','')))
    df_player['minutes'] = df_player['minutes'].apply(lambda x: int(str(x).replace(',','')))
    df_one_year = pd.merge(df_gk_player,df_player,on=['player','squad','nationality','position','age'],suffixes=['_gk','_pl'],how='outer')
    df_one_year = df_one_year.drop("Unnamed: 0_pl",axis=1)
    df_one_year = df_one_year.drop("Unnamed: 0_gk",axis=1)
    df_one_year['nationality'] = df_one_year['nationality'].apply(lambda x: str(x).split(','))
    df_one_year['nationality'] = df_one_year['nationality'].apply(lambda x: easy_split(x))
    df_one_year['nationality'] = df_one_year['nationality'].apply(lambda x: ",".join(x))
    df_one_year["season"] = int(year)
    
    output_name = "./Players_{0}".format(year)
        
    df_one_year.to_csv(output_name+".csv")
    


if __name__ == "__main__":
   main(sys.argv[1:])
   