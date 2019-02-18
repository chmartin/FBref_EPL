#scrape FBRef.com for team and player data
# Based upon: https://medium.com/@smehta/scrape-and-create-your-own-beautiful-dataset-from-sports-reference-com-using-beautifulsoup-python-c26d6920684e
# and usefull input from: https://github.com/BenKite/baseball_data/blob/master/baseballReferenceScrape.py

#TO DO: get table column names from html

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys, getopt
import csv

def scrapeURL(url):
    res = requests.get(url)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    team_table = all_tables[0]
    player_table = all_tables[1]
    
    #Parse player_table
    pre_df_player = dict()
    features_wanted_player = {"player","nationality","position","squad","age","games","games_starts","games_subs","minutes","minutes_per_game","goals","assists","pens_made","pens_att","fouls","cards_yellow","cards_red","shots_on_target","goals_per90","goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","shots_on_target_per90","fouls_per90","cards_per90"}
    rows_player = player_table.find_all('tr')
    for row in rows_player:
        if(row.find('th',{"scope":"row"}) != None):
        
            for f in features_wanted_player:
                cell = row.find("td",{"data-stat": f})
                a = cell.text.strip().encode()
                text=a.decode("utf-8")
                if f in pre_df_player:
                    pre_df_player[f].append(text)
                else:
                    pre_df_player[f] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)
    
    #Parse team_table
    pre_df_squad = dict()
    #Note: features does not contain squad name, it requires special treatment
    features_wanted_squad = {"players_used","games","goals","assists","pens_made","pens_att","fouls","cards_yellow","cards_red","shots_on_target","goals_perG","goals_assists_perG","goals_pens_perG","goals_assists_pens_perG","shots_on_target_perG","fouls_perG","cards_perG"}
    rows_squad = team_table.find_all('tr')
    for row in rows_squad:
        if(row.find('th',{"scope":"row"}) != None):
            name = row.find('th',{"data-stat":"squad"}).text.strip().encode().decode("utf-8")
            if 'squad' in pre_df_squad:
                pre_df_squad['squad'].append(name)
            else:
                pre_df_squad['squad'] = [name]
            for f in features_wanted_squad:
                cell = row.find("td",{"data-stat": f})
                a = cell.text.strip().encode()
                text=a.decode("utf-8")
                if f in pre_df_squad:
                    pre_df_squad[f].append(text)
                else:
                    pre_df_squad[f] = [text]
    df_squad = pd.DataFrame.from_dict(pre_df_squad)
    
    return df_player, df_squad
    
    
def main(argv):
    urls = pd.DataFrame()
    
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print('FBref_scrape.py -f <url_csv_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('FBref_scrape.py -f <url_csv_file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            urls = pd.read_csv(arg,delimiter=',')
    
    for url in urls:
        print(url)
        df_player, df_squad = scrapeURL(url)
        
        k = url.rfind("/")
        output_name = url[k+1:]
        df_player.to_csv(output_name+"_players.csv")
        df_squad.to_csv(output_name+"_squad.csv")
    


if __name__ == "__main__":
   main(sys.argv[1:])
   