# Merge two Squad datasets

import pandas as pd
import re
import sys, getopt
import glob
    
def main(argv):
    year=1992
    path = "./"
    try:
        opts, args = getopt.getopt(argv,"hy:p:",["year=","path="])
    except getopt.GetoptError:
        print('FBref_join_year_squad.py -y <year> -p <path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('FBref_join_year_squad.py -y <year> -p <path>')
            sys.exit()
        elif opt in ("-y", "--year"):
            year = int(arg)
        elif opt in ("-p", "--path"):
            path = arg
    
    f_gk = glob.glob(path + "/{0}-{1}*Stats_gk_squad.csv".format(year,year+1))
    f = glob.glob(path + "/{0}-{1}*Stats_squad.csv".format(year,year+1))
    
    if len(f_gk) != 1:
        print("Invalid input, matching input Squad GK files:")
        print(f_gk)
        sys.exit(2)
    if len(f) != 1:
        print("Invalid input, matching input Squad files:")
        print(f)
        sys.exit(2)
    
    df_gk_squad= pd.read_csv(f_gk[0])
    df_squad= pd.read_csv(f[0])
    df_gk_squad = df_gk_squad.add_suffix("_gk")
    df_year = df_squad.set_index('squad').join(df_gk_squad.set_index('squad_gk'))
    df_year = df_year.drop("Unnamed: 0",axis=1)
    df_year = df_year.drop("Unnamed: 0_gk",axis=1)
    df_year["season"] = int(year)
    df_year['minutes_gk'] = df_year['minutes_gk'].apply(lambda x:int(x.replace(',', '')))
    
    output_name = "./Squad_{0}".format(year)
        
    df_year.to_csv(output_name+".csv")
    


if __name__ == "__main__":
   main(sys.argv[1:])
   