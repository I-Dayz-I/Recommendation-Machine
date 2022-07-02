import numpy as np
import pandas as pd
import sqlalchemy
import psycopg2
import sqlite3
import os


def Create_Usefull_DS():
    #Getting Script Paths
    parentFolderPath = os.path.realpath(__file__) + '\..\..'
    
    #Loading User Data
    #all_users = pd.read_csv(parentFolderPath + '\Dataset\distinct_users_from_search_table_real_map.csv',sep=",",error_bad_lines=False, encoding='latin-1')
    # print(all_users)
    
    #Loading Tweets Dataset
    #all_tweets_link = pd.read_csv(parentFolderPath + '\Dataset\link_status_search_with_ordering_real.csv',sep=",",error_bad_lines=False, encoding='latin-1')
    # print(all_tweets_link)
    
    #Loading User Followers Graph
    #engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/aplication')
    

    
    conn.commit()
    # sql_query = pd.read_sql_query ('''
    #                            SELECT
    #                            *
    #                            FROM active_follower_real
    #                            ''', conn)

    # df = pd.DataFrame(sql_query, columns = ['user_id', 'follower_id'])
    # print (df)
    # all_users_link = pd.read_sql_table(parentFolderPath + '\Dataset\active_follower_real.sql',conn)
    # print(all_users_link)



def Getting_Tweets_Text():
    return


def Creating_Following_Table():
    return


def SQL_to_PD():
    conn = sqlite3.connect('active_follower_real')
    c = conn.cursor()
    c.execute(''' 
              DROP TABLE IF EXISTS `active_follower_real`;
              
              CREATE TABLE `active_follower_real` (
             `user_id` int(11) NOT NULL,
  `follower_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`follower_id`),
  KEY `NewIndex1` (`user_id`),
  KEY `NewIndex2` (`follower_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
              
              
              ''')
    
    
    
Create_Usefull_DS()