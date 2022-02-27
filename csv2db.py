''' 
### PURPOSE ###
This program takes a CSV file containing data on therapists and inserts the info into a database.

### Database format ###
CREATE TABLE Therapist_Info(
    Name TEXT NOT NULL,                 # name of therapist
    Description TEXT NOT NULL,          # description of therapist
    Phone_Number TEXT NOT NULL,         # contact info of therapist
    Accepted_Insurance TEXT NOT NULL,   # accepted insurance
    Cost TEXT NOT NULL,                 # expected cost of a session
    Url Text PRIMARY KEY NOT NULL       # url to more details about therapist
);
'''

import sqlite3

import csv
import sys
import os
import argparse


def connect2DB(dbFile):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(dbFile)
    return conn

def createDB(dbFile):
    """ create a database connection to a SQLite database """
    try:
        conn = connect2DB(dbFile)
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS Therapist_Info(
                        Name TEXT NOT NULL,              
                        Description TEXT NOT NULL,         
                        Phone_Number TEXT NOT NULL,         
                        Accepted_Insurance TEXT NOT NULL,   
                        Cost TEXT NOT NULL,                
                        Url Text PRIMARY KEY NOT NULL       
                    );
        ''')
        conn.commit()
        print("User table created successfully")
    except Error as e:
        print(e)
    finally:
        conn.close()

def parseCSV_add2DB(csvFile, dbFile):
    """ parse CSV file and add therapist info to SQLite database """
    try:
        conn = connect2DB(dbFile)
        cur = conn.cursor()
        
        insertStatement = "INSERT INTO Therapist_Info (Name, Description, Phone_Number, Accepted_Insurance, Cost, Url) VALUES (?,?,?,?,?,?)"

        # parse CSV file
        with open(csvFile) as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)    # skip first row w/ column labels

            for row in reader:
                # add therapist info to database
                cur.execute(insertStatement, (row[0], row[1], row[2], row[3], row[4], row[5]))
        
        conn.commit()
        print("CSV info added to therapists.db successfully")
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        conn.close()
            

def main(args):
    # creates database file if it does not already exist
    createDB(args.dbFile)
    # parse CSV file and add therapist info into database file
    parseCSV_add2DB(args.csvFile, args.dbFile)
    

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbFile', type=str, default='therapists.db', help='database file path')
    parser.add_argument('--csvFile', type=str, help='csv file path', required=True)
    args = parser.parse_args()  # retrieve arguments

    main(args)
