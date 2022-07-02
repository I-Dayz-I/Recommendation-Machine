import numpy as np
import pandas as pd
import sqlalchemy
import psycopg2
import sqlite3
import os
import Getting_all_data


def Create_Usefull_DS():
    #Getting Script Paths
    parentFolderPath = os.path.realpath(__file__) + '\..\..'
    
    #Loading User Data
    #all_users = pd.read_csv(parentFolderPath + '\Dataset\distinct_users_from_search_table_real_map.csv',sep=",",error_bad_lines=False, encoding='latin-1')
    # print(all_users)
    
    #Loading Tweets Dataset
    all_tweets = pd.read_csv(parentFolderPath + '\Dataset\link_status_search_with_ordering_real.csv',sep=",",error_bad_lines=False, encoding='latin-1')
    # print(all_tweets_link)
    
    #Loading User Followers Graph
    #engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/aplication')
    



    
Create_Usefull_DS()